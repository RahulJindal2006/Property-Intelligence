import os
import yaml
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from app.config import OPENAI_API_KEY, PROMPTS_DIR
from app.services.sql_execution import execute_sqlite_query
from app.models.chat import ChatRequest, ChatResponse

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

with open(f"{PROMPTS_DIR}/sql_prompt.yaml", "r") as f:
    prompt_data = yaml.safe_load(f)
prompt_template = PromptTemplate(
    input_variables=prompt_data["input_variables"],
    template=prompt_data["template"],
)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")


def build_conversation_context(history) -> str:
    if not history:
        return ""
    recent = history[-3:]
    context = "Previous conversation for context only - do not repeat these answers:\n"
    for exchange in recent:
        context += f"User asked: {exchange.question}\nYou answered: {exchange.answer}\n"
    context += "\nNow answer this NEW question independently:\n"
    return context


def process_message(request: ChatRequest) -> ChatResponse:
    message = request.message
    conversation_context = build_conversation_context(request.conversation_history)

    classification_prompt = f"""You are a property management AI assistant that is friendly but professional.
    {conversation_context}
    Determine if the following input is:
    A) A data question that requires a SQL query (about properties, residents, occupancy, rent, leases, etc.)
    B) A conversational message (greetings, small talk, general questions not about the data)
    Input: "{message}"
    Reply with only "DATA" or "CHAT" nothing else."""

    intent = llm.invoke(classification_prompt).content.strip()

    if intent == "DATA":
        final_prompt = prompt_template.format(input=message)
        contextual_sql_prompt = f"{conversation_context}{final_prompt}" if conversation_context else final_prompt
        query_text = llm.invoke(contextual_sql_prompt).content.strip()
        output = execute_sqlite_query(query_text)

        if isinstance(output, str):
            if "Sorry" in output:
                return ChatResponse(
                    intent="DATA",
                    answer=output,
                    error="blocked"
                )
            return ChatResponse(
                intent="DATA",
                answer=output,
                sql_query=query_text,
                error="query_error"
            )

        if output is None or output.empty:
            return ChatResponse(
                intent="DATA",
                answer="I had trouble finding that data. Could you try rephrasing your question?",
                sql_query=query_text
            )

        summary_prompt = f"""You are a friendly but professional property management AI assistant.
        {conversation_context}
        The user just asked: "{message}"
        The SQL result for THIS specific question was: {output.to_string()}
        Respond in 1-2 natural friendly sentences summarizing ONLY what THIS data shows.
        Do not reference or repeat previous answers.
        Do not make assumptions beyond what the data shows.
        Do not mention SQL or technical details."""

        human_response = llm.invoke(summary_prompt).content.strip()

        data = output.replace({float('nan'): None}).to_dict(orient='records')

        return ChatResponse(
            intent="DATA",
            answer=human_response,
            sql_query=query_text,
            data=data
        )
    else:
        chat_prompt = f"""You are a property management AI assistant. You are warm, friendly and professional.
        You are connected to a SQLite database called PropertyManagement.db with two tables:
        - lease_charges: contains resident, unit, rent and lease information
        - property_summary: contains occupancy, vacancy and leasing statistics per property
        {conversation_context}
        Always respond in a friendly, warm tone. If someone asks for a joke or something fun,
        go ahead and do it, then warmly remind them that your main purpose is helping with
        property management insights. Never respond with just a "?" or incomplete sentences.
        Keep responses to 2-3 sentences max.
        Respond to this message: {message}"""

        chat_response = llm.invoke(chat_prompt).content.strip()

        return ChatResponse(
            intent="CHAT",
            answer=chat_response
        )
