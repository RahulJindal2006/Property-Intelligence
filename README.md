# Property Intelligence

A full-stack AI platform that transforms raw Excel rent roll files into a structured database and lets you query property management data using plain English. Built as a replica of a real-world software engineering workflow.

![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)
![GPT-3.5](https://img.shields.io/badge/GPT--3.5-Turbo-412991?logo=openai)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-1C3C3C)

## Overview 

In a previous software engineering role, I was regularly handed raw Excel rent roll files and tasked with extracting data, building structured databases, generating reports, and creating AI-powered SQL chatbots. This project recreates that entire end-to-end workflow from scratch.

**Key stats:** 25 properties | 9,100+ lease records | 4 database tables | 50 source Excel files

## Features

- **Natural Language SQL** - Ask questions in plain English. The AI translates your words into SQL queries and returns human-readable answers.
- **Interactive Dashboards** - Explore occupancy trends, revenue breakdowns, vacancy analysis, lease expirations, outstanding balances, and more through interactive charts.
- **SQL Safety Layer** - Every generated query is validated against a blocklist of destructive keywords (`DROP`, `DELETE`, `UPDATE`, etc.) before execution.
- **Issue Reporting** - Built-in feedback system to report incorrect AI responses with severity levels.
- **Conversation Context** - The chat maintains a rolling 3-message history for contextual follow-up questions.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS 4, Recharts |
| Backend | FastAPI, Python, Uvicorn |
| AI/LLM | OpenAI GPT-3.5 Turbo, LangChain |
| Database | SQLite |
| ETL | Pandas, openpyxl |
| Legacy UI | Streamlit (original prototype) |

## Architecture

```
Property Intelligence
├── frontend/          # Next.js 16 app
│   └── src/
│       ├── app/       # Pages: chat, dashboard, schema, issues, about, properties
│       └── components/# Reusable UI components
├── backend/           # FastAPI REST API
│   └── app/
│       ├── routers/   # chat, dashboard, properties, schema, issues
│       ├── services/  # LLM processing, SQL execution
│       ├── models/    # Pydantic request/response models
│       └── prompts/   # YAML prompt templates
├── script.py          # ETL pipeline (Excel → CSV → SQLite)
├── 1_home.py          # Streamlit app (legacy prototype)
└── pages/             # Streamlit multi-page app (legacy)
```

## Data Pipeline

The ETL pipeline (`script.py`) processes raw Excel files through four stages:

1. **Extract** - Reads 50 raw Excel rent roll files from `Rent_Roll_With_Lease_Charges/` and `Unit_Availability/` directories.
2. **Transform** - Cleans, normalizes, and structures the data. Extracts property metadata, forward-fills identity columns, removes junk rows, and standardizes property names.
3. **Load** - Writes cleaned data to intermediate CSVs, then loads into 4 SQLite tables:
   - `lease_charges` - Resident, unit, rent, and lease information
   - `property_summary` - Occupancy, vacancy, and leasing statistics per property
   - `summary_groups` - Aggregated resident type breakdowns per property
   - `charge_code_summary` - Revenue breakdown by charge code
4. **Query** - The AI chat converts plain English into SQL and returns insights.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Send a message, receive AI response with optional SQL/data |
| `GET` | `/api/dashboard` | Full dashboard data (KPIs, charts, tables) |
| `GET` | `/api/properties` | Property listings with photos |
| `GET` | `/api/schema` | Database schema and table info |
| `GET` | `/api/issues` | Reported issues |
| `GET` | `/api/health` | Health check |

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- An OpenAI API key

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/property-intelligence.git
cd property-intelligence
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:

```env
OPENAI_API_KEY=your-api-key-here
ADMIN_PASSWORD=your-admin-password
```

Start the backend server:

```bash
uvicorn app.main:app --reload --port 8000
```

### 3. Set up the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000` and the API at `http://localhost:8000`.

### 4. Run the ETL pipeline (optional)

If you have raw Excel files and want to rebuild the database:

```bash
# From the project root
python script.py
```

This will process all Excel files, generate intermediate CSVs, and populate `PropertyManagement.db`.

## Example Questions

- "How many vacant units do we have?"
- "Which properties have the lowest occupancy?"
- "Show me residents with a balance"
- "What is our average rent?"
- "Which leases expire in 90 days?"
- "How many total residents do we have?"

## License

This project is for demonstration and portfolio purposes.

## Author

**Rahul Jindal** - CS/BBA @ Wilfrid Laurier University
