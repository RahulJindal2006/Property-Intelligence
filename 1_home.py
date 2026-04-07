import os
import base64
import streamlit as st
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    from app_secrets import OPENAI_API_KEY

from sql_execution import execute_sqlite_query
from langchain_openai import ChatOpenAI
from langchain_core.prompts import load_prompt
from pathlib import Path
import pandas as pd
from datetime import datetime
from sidebar import render_sidebar, render_css

def save_issue_report(file_path, question, what_went_wrong, severity):
    try:
        new_issue = pd.DataFrame([{
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Question': question,
            'What_Went_Wrong': what_went_wrong,
            'Severity': severity
        }])
        if os.path.exists(file_path):
            existing = pd.read_csv(file_path)
            updated = pd.concat([existing, new_issue], ignore_index=True)
        else:
            updated = new_issue
        updated.to_csv(file_path, index=False)
        return "success"
    except:
        return "error"

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

current_dir = Path(__file__)
root_dir = Path(__file__).parent

st.set_page_config(
    page_title="Property Management Assistant",
    page_icon="photos/logo.jpeg",
    layout="wide"
)

render_css()
render_sidebar()

st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    .header-container {
        display: flex;
        align-items: center;
        gap: 18px;
        padding: 10px 0 6px 0;
        border-bottom: 1px solid rgba(128,128,128,0.2);
        margin-bottom: 2rem;
    }
    .header-title {
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .header-tagline {
        font-size: 14px;
        color: #6b7280;
        margin-top: 2px;
    }
    .welcome-banner {
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 24px;
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 16px;
    }
    .welcome-banner-content {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .welcome-banner-icon { font-size: 28px; }
    .welcome-banner-title { font-size: 16px; font-weight: 700; margin-bottom: 3px; }
    .welcome-banner-text { font-size: 13px; color: #6b7280; line-height: 1.5; }
    .examples-label {
        font-size: 12px;
        font-weight: 600;
        color: #6b7280;
        letter-spacing: 0.6px;
        margin-bottom: 10px;
        margin-top: 20px;
    }
    .stButton > button {
        border-radius: 20px !important;
        padding: 6px 14px !important;
        font-size: 13px !important;
        border: 1px solid rgba(99,102,241,0.25) !important;
        color: #6366f1 !important;
        background: rgba(99,102,241,0.06) !important;
        transition: all 0.2s !important;
        white-space: normal !important;
        height: auto !important;
        text-align: left !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: rgba(99,102,241,0.15) !important;
        border-color: #6366f1 !important;
        color: #6366f1 !important;
    }
    .stDownloadButton > button {
        border-radius: 20px !important;
        padding: 6px 14px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        border: 1px solid rgba(99,102,241,0.25) !important;
        color: #6366f1 !important;
        background: rgba(99,102,241,0.06) !important;
        transition: all 0.2s !important;
        white-space: nowrap !important;
        height: auto !important;
        text-align: center !important;
        width: 100% !important;
    }
    .stDownloadButton > button:hover {
        background: rgba(99,102,241,0.15) !important;
        border-color: #6366f1 !important;
        color: #6366f1 !important;
    }
    .user-message-row {
        display: flex;
        justify-content: flex-end;
        margin: 12px 0;
    }
    .user-message {
        background: #6366f1;
        color: white;
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px;
        max-width: 70%;
        font-size: 15px;
        line-height: 1.6;
    }
    .ai-message-row {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        gap: 12px;
        margin: 12px 0;
    }
    .ai-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        object-fit: cover;
        flex-shrink: 0;
        margin-top: 2px;
    }
    .ai-message {
        background: rgba(99,102,241,0.06);
        border: 1px solid rgba(99,102,241,0.15);
        border-radius: 18px 18px 18px 4px;
        padding: 12px 18px;
        max-width: 70%;
        font-size: 15px;
        line-height: 1.6;
    }
    .ai-message-warning {
        background: rgba(239,68,68,0.06);
        border: 1px solid rgba(239,68,68,0.2);
        border-radius: 18px 18px 18px 4px;
        padding: 12px 18px;
        max-width: 70%;
        font-size: 15px;
        line-height: 1.6;
        color: #ef4444;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(128,128,128,0.2);
        padding-bottom: 0;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 20px;
        font-weight: 500;
        font-size: 14px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #6366f1 !important;
        color: white !important;
    }
    .ai-disclaimer {
        text-align: center;
        font-size: 12px;
        color: #6b7280;
        padding: 16px 12px 4px 12px;
        border-top: 1px solid rgba(128,128,128,0.1);
        margin-top: 16px;
    }
    hr {
        border-color: rgba(128,128,128,0.15) !important;
        margin: 1.5rem 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""
if "example_prompt" not in st.session_state:
    st.session_state.example_prompt = ""
if "intent" not in st.session_state:
    st.session_state.intent = None
if "show_issue_form" not in st.session_state:
    st.session_state.show_issue_form = False
if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Load logo
with open(f"{root_dir}/photos/logo.jpeg", "rb") as img_file:
    logo_b64 = base64.b64encode(img_file.read()).decode()

# Header
st.markdown(f"""
    <div class='header-container'>
        <img src='data:image/jpeg;base64,{logo_b64}' style='width:70px; height:70px; border-radius:10px; object-fit:cover;'>
        <div>
            <div class='header-title'>Property Management AI Assistant</div>
            <div class='header-tagline'>Ask anything about your properties, residents, occupancy and more</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Welcome banner
if st.session_state.show_welcome:
    col_banner, col_close = st.columns([11, 1])
    with col_banner:
        st.markdown("""
            <div class='welcome-banner'>
                <div class='welcome-banner-content'>
                    <div class='welcome-banner-icon'>👋</div>
                    <div>
                        <div class='welcome-banner-title'>Welcome to your Property Management AI</div>
                        <div class='welcome-banner-text'>
                            Ask questions in plain English and get instant answers from your property database.
                            No SQL knowledge needed - just type what you want to know!
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col_close:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✕", key="close_welcome"):
            st.session_state.show_welcome = False
            st.rerun()

# Example questions
st.markdown("<div class='examples-label'>TRY ASKING</div>", unsafe_allow_html=True)
example_questions = [
    "How many vacant units do we have?",
    "Which properties have the lowest occupancy?",
    "Show me residents with a balance",
    "What is our average rent?",
    "Which leases expire in 90 days?",
    "How many total residents do we have?"
]
cols = st.columns(3)
for i, question in enumerate(example_questions):
    with cols[i % 3]:
        if st.button(question, key=f"example_{i}"):
            st.session_state.example_prompt = question
            st.session_state.last_prompt = ""
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
tabs = st.tabs(["  💬 Conversation  ", "  🚨 Report an Issue  "])

prompt_template = load_prompt(f"{root_dir}/prompts/sql_prompt.yaml")
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# Handle input
example_val = st.session_state.get("example_prompt", "")
if example_val:
    st.session_state.example_prompt = ""
prompt = st.chat_input("Ask anything about your properties...") or example_val

if prompt and prompt != st.session_state.last_prompt:
    st.session_state.last_prompt = prompt
    st.session_state.show_issue_form = False
    final_prompt = prompt_template.format(input=prompt)

    conversation_context = ""
    if st.session_state.conversation_history:
        recent = st.session_state.conversation_history[-3:]
        conversation_context = "Previous conversation for context only - do not repeat these answers:\n"
        for exchange in recent:
            conversation_context += f"User asked: {exchange['question']}\nYou answered: {exchange['answer']}\n"
        conversation_context += "\nNow answer this NEW question independently:\n"

    with st.spinner("🤔 Thinking..."):
        classification_prompt = f"""You are a property management AI assistant that is friendly but professional.
        {conversation_context}
        Determine if the following input is:
        A) A data question that requires a SQL query (about properties, residents, occupancy, rent, leases, etc.)
        B) A conversational message (greetings, small talk, general questions not about the data)
        Input: "{prompt}"
        Reply with only "DATA" or "CHAT" nothing else."""

        intent = llm.invoke(classification_prompt).content.strip()
        st.session_state.intent = intent

        if intent == "DATA":
            contextual_sql_prompt = f"{conversation_context}{final_prompt}" if conversation_context else final_prompt
            query_text = llm.invoke(contextual_sql_prompt).content.strip()
            output = execute_sqlite_query(query_text)

            if isinstance(output, str) and "⚠️" in output:
                st.session_state.conversation_history.append({
                    "question": prompt, "answer": "blocked", "query": None, "dataframe": None
                })
            elif output is None or (hasattr(output, 'empty') and output.empty):
                human_response = "I had trouble finding that data. Could you try rephrasing your question?"
                st.session_state.conversation_history.append({
                    "question": prompt, "answer": human_response, "query": query_text, "dataframe": None
                })
            else:
                summary_prompt = f"""You are a friendly but professional property management AI assistant.
                {conversation_context}
                The user just asked: "{prompt}"
                The SQL result for THIS specific question was: {output}
                Respond in 1-2 natural friendly sentences summarizing ONLY what THIS data shows.
                Do not reference or repeat previous answers.
                Do not make assumptions beyond what the data shows.
                Do not mention SQL or technical details."""
                human_response = llm.invoke(summary_prompt).content.strip()
                st.session_state.conversation_history.append({
                    "question": prompt, "answer": human_response, "query": query_text, "dataframe": output
                })
        else:
            chat_prompt = f"""You are a property management AI assistant named Aker. You are warm, friendly and professional.
            You are connected to a SQLite database called PropertyManagement.db with two tables:
            - lease_charges: contains resident, unit, rent and lease information
            - property_summary: contains occupancy, vacancy and leasing statistics per property
            {conversation_context}
            Always respond in a friendly, warm tone. If someone asks for a joke or something fun,
            go ahead and do it, then warmly remind them that your main purpose is helping with
            property management insights. Never respond with just a "?" or incomplete sentences.
            Keep responses to 2-3 sentences max.
            Respond to this message: {prompt}"""
            chat_response = llm.invoke(chat_prompt).content.strip()
            st.session_state.conversation_history.append({
                "question": prompt, "answer": chat_response, "query": None, "dataframe": None
            })

# Conversation tab
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)

    # Reset + Download buttons
    if st.session_state.conversation_history:
        _, btn_col1, btn_col2, _ = st.columns([2, 1, 1, 2])
        with btn_col1:
            if st.button("Reset Chat", key="reset_convo", use_container_width=True):
                st.session_state.conversation_history = []
                st.session_state.last_prompt = ""
                st.rerun()
        with btn_col2:
            convo_text = ""
            for exchange in st.session_state.conversation_history:
                convo_text += f"You: {exchange['question']}\n"
                convo_text += f"AI: {exchange['answer']}\n"
                if exchange.get('query'):
                    convo_text += f"SQL: {exchange['query']}\n"
                convo_text += "\n"
            st.download_button(
                label="Download",
                data=convo_text,
                file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key="download_convo",
                use_container_width=True
            )
        st.markdown("<br>", unsafe_allow_html=True)

    for idx, exchange in enumerate(st.session_state.conversation_history):
        st.markdown(f"""
            <div class='user-message-row'>
                <div class='user-message'>{exchange['question']}</div>
            </div>
        """, unsafe_allow_html=True)

        if exchange['answer'] == "blocked":
            st.markdown(f"""
                <div class='ai-message-row'>
                    <img src='data:image/jpeg;base64,{logo_b64}' class='ai-avatar'>
                    <div class='ai-message-warning'>⚠️ Sorry, I can only retrieve data and cannot modify the database.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='ai-message-row'>
                    <img src='data:image/jpeg;base64,{logo_b64}' class='ai-avatar'>
                    <div class='ai-message'>{exchange['answer']}</div>
                </div>
            """, unsafe_allow_html=True)

            if exchange.get('dataframe') is not None:
                try:
                    df = exchange['dataframe']
                    if hasattr(df, 'index'):
                        df = df.reset_index(drop=True)
                        df.index = df.index + 1
                    st.dataframe(df, use_container_width=True)
                except Exception:
                    pass

            if exchange.get('query'):
                query_key = f"show_sql_{idx}"
                if query_key not in st.session_state:
                    st.session_state[query_key] = False
                if st.button("🔍 Show SQL Query", key=f"sql_btn_{idx}"):
                    st.session_state[query_key] = not st.session_state[query_key]
                if st.session_state[query_key]:
                    st.code(exchange["query"], language="sql")
                    st.markdown(f"""
                        <a href="data:text/plain;charset=utf-8,{exchange['query']}"
                           download="query.sql"
                           style="
                               display: inline-block;
                               margin-top: 8px;
                               padding: 5px 14px;
                               font-size: 11px;
                               font-weight: 600;
                               letter-spacing: 0.4px;
                               color: #a5b4fc;
                               background: rgba(99,102,241,0.08);
                               border: 1px solid rgba(99,102,241,0.25);
                               border-radius: 6px;
                               text-decoration: none;
                           ">
                            Download SQL Query
                        </a>
                    """, unsafe_allow_html=True)

    st.markdown("""
        <div id='scroll-anchor'></div>
        <script>
            var anchor = document.getElementById('scroll-anchor');
            if (anchor) { anchor.scrollIntoView({ behavior: 'smooth' }); }
        </script>
    """, unsafe_allow_html=True)

# Report an Issue tab
with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.conversation_history:
        latest = st.session_state.conversation_history[-1]
        if latest.get('answer') != "blocked":
            st.subheader("Report an Issue")
            st.markdown("<br>", unsafe_allow_html=True)
            what_went_wrong = st.text_area("What went wrong with this response?", height=120)
            severity = st.selectbox("Severity Level", ["Low", "Medium", "High"])
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Submit Report"):
                if what_went_wrong:
                    file_path = f"{root_dir}/issues.csv"
                    status = save_issue_report(
                        file_path=file_path,
                        question=st.session_state.last_prompt,
                        what_went_wrong=what_went_wrong,
                        severity=severity
                    )
                    if status == "success":
                        st.success("✅ Issue reported successfully! Thank you for the feedback.")
                    else:
                        st.error("Something went wrong saving your report. Please try again.")
                else:
                    st.warning("Please describe what went wrong before submitting.")
    else:
        st.info("Ask a question first before reporting an issue.")

# Disclaimer - always at the very bottom
st.markdown("""
    <div class='ai-disclaimer'>
        AI responses may occasionally be inaccurate. If something doesn't look right, please use the
        <strong>Report an Issue</strong> tab to let us know.
    </div>
""", unsafe_allow_html=True)