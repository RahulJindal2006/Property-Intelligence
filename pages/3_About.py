import streamlit as st
import base64
from pathlib import Path
from sidebar import render_sidebar, render_css

st.set_page_config(page_title="About", page_icon="photos/logo.jpeg")
render_css()
render_sidebar()

current_dir = Path(__file__)
root_dir = Path(__file__).parent.parent

# Load profile photo
with open(f"{root_dir}/photos/Profile.png", "rb") as img_file:
    profile_b64 = base64.b64encode(img_file.read()).decode()

# Load logo
with open(f"{root_dir}/photos/logo.jpeg", "rb") as img_file:
    logo_b64 = base64.b64encode(img_file.read()).decode()

st.markdown("""
    <style>
    .about-hero {
        display: flex;
        align-items: center;
        gap: 32px;
        padding: 32px 0 40px 0;
        border-bottom: 1px solid rgba(128,128,128,0.15);
        margin-bottom: 40px;
    }
    .about-photo {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #6366f1;
        flex-shrink: 0;
    }
    .about-name {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .about-title {
        font-size: 14px;
        color: #6366f1;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }
    .about-bio {
        font-size: 14px;
        color: #9ca3af;
        line-height: 1.7;
        max-width: 600px;
    }
    .about-links {
        display: flex;
        gap: 12px;
        margin-top: 14px;
        flex-wrap: wrap;
    }
    .about-link {
        font-size: 12px;
        font-weight: 600;
        color: #6366f1;
        text-decoration: none;
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 20px;
        padding: 5px 14px;
        transition: all 0.2s;
    }
    .about-link:hover {
        background: rgba(99,102,241,0.1);
    }
    .section-label {
        font-size: 13px;
        font-weight: 700;
        color: #6366f1;
        letter-spacing: 1.2px;
        margin-bottom: 16px;
        margin-top: 40px;
    }
    .section-title {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 12px;
        letter-spacing: -0.3px;
    }
    .section-text {
        font-size: 14px;
        color: #9ca3af;
        line-height: 1.8;
        margin-bottom: 24px;
    }
    .cards-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-bottom: 40px;
    }
    .card {
        background: rgba(99,102,241,0.06);
        border: 1px solid rgba(99,102,241,0.15);
        border-radius: 14px;
        padding: 20px;
    }
    .card-icon {
        font-size: 24px;
        margin-bottom: 10px;
    }
    .card-title {
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .card-text {
        font-size: 13px;
        color: #9ca3af;
        line-height: 1.6;
    }
    .aker-section {
        display: flex;
        align-items: center;
        gap: 20px;
        background: rgba(99,102,241,0.06);
        border: 1px solid rgba(99,102,241,0.15);
        border-radius: 16px;
        padding: 24px 28px;
        margin: 40px 0;
    }
    .aker-logo {
        width: 60px;
        height: 60px;
        border-radius: 10px;
        object-fit: cover;
        flex-shrink: 0;
    }
    .aker-title {
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .aker-text {
        font-size: 13px;
        color: #9ca3af;
        line-height: 1.7;
    }
    .tech-stack {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 40px;
    }
    .tech-tag {
        font-size: 12px;
        font-weight: 600;
        color: #a5b4fc;
        background: rgba(99,102,241,0.1);
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: 20px;
        padding: 5px 14px;
    }
    .divider {
        border: none;
        border-top: 1px solid rgba(128,128,128,0.15);
        margin: 32px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Hero section
st.markdown(f"""
    <div class='about-hero'>
        <img src='data:image/png;base64,{profile_b64}' class='about-photo'>
        <div>
            <div class='about-name'>Rahul Jindal</div>
            <div class='about-title'>CS/BBA STUDENT · WILFRID LAURIER UNIVERSITY</div>
            <div class='about-bio'>
                I'm a Computer Science & Business Administration student at Wilfrid Laurier University with hands-on experience 
                building web applications, AI-powered tools, and data platforms. I built this Property Management AI Assistant 
                for Aker Companies to demonstrate how natural language and LLMs can replace complex SQL workflows and make 
                data instantly accessible to any team member - no technical knowledge required.
            </div>
            <div class='about-links'>
                <a class='about-link' href='https://www.linkedin.com/in/rahuljindal-cs/' target='_blank'>💼 LinkedIn</a>
                <a class='about-link' href='https://github.com/RahulJindal2006' target='_blank'>🐙 GitHub</a>
                <a class='about-link' href='mailto:jind3091@mylaurier.ca'>📧 Email</a>
                <a class='about-link' href='https://www.akercompanies.com/' target='_blank'>💡 Aker-Companies</a>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# About Aker section
st.markdown(f"""
    <div class='section-label'>WHY AKER</div>
    <div class='aker-section'>
        <img src='data:image/jpeg;base64,{logo_b64}' class='aker-logo'>
        <div>
            <div class='aker-title'>Built specifically for Aker Companies</div>
            <div class='aker-text'>
                Aker is a vertically integrated real estate platform that invests in residential communities at the intersection 
                of urban and outdoor environments - managing over $2B in multifamily and mixed-use properties and connecting 
                12,000+ residents across the U.S. This tool was built to support Aker's operations team by turning raw property 
                data into instant, plain-English insights - no SQL, no spreadsheets, no waiting on reports.
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# How it works
st.markdown("<div class='section-label'>HOW IT WORKS</div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>From question to answer in seconds</div>", unsafe_allow_html=True)
st.markdown("<div class='section-text'>Type any question in plain English. The AI classifies your intent, generates the correct SQL query, runs it against the live database, and returns a human-readable summary - all in one seamless flow.</div>", unsafe_allow_html=True)

st.markdown("""
    <div class='cards-grid'>
        <div class='card'>
            <div class='card-icon'>🧠</div>
            <div class='card-title'>Intent Classification</div>
            <div class='card-text'>The AI first determines whether your message is a data question or casual conversation before generating any SQL.</div>
        </div>
        <div class='card'>
            <div class='card-icon'>⚡</div>
            <div class='card-title'>SQL Generation</div>
            <div class='card-text'>A prompt-engineered LangChain template converts natural language into precise SQLite queries with built-in safety rules.</div>
        </div>
        <div class='card'>
            <div class='card-icon'>🛡️</div>
            <div class='card-title'>Safety Layer</div>
            <div class='card-text'>All destructive operations (DROP, DELETE, UPDATE) are blocked at the execution layer before any query reaches the database.</div>
        </div>
        <div class='card'>
            <div class='card-icon'>📊</div>
            <div class='card-title'>Live Data Tables</div>
            <div class='card-text'>Results are returned as interactive dataframes alongside a plain-English summary of what the data shows.</div>
        </div>
        <div class='card'>
            <div class='card-icon'>🔍</div>
            <div class='card-title'>SQL Transparency</div>
            <div class='card-text'>Every data response includes a toggleable SQL query view so technical users can verify exactly what was run.</div>
        </div>
        <div class='card'>
            <div class='card-icon'>🚨</div>
            <div class='card-title'>Issue Reporting</div>
            <div class='card-text'>Users can flag incorrect responses with severity levels. Reports are stored and reviewed via a password-protected admin panel.</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Tech stack
st.markdown("<div class='section-label'>TECH STACK</div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Built with</div>", unsafe_allow_html=True)
st.markdown("""
    <div class='tech-stack'>
        <span class='tech-tag'>Python</span>
        <span class='tech-tag'>Streamlit</span>
        <span class='tech-tag'>LangChain</span>
        <span class='tech-tag'>OpenAI GPT-3.5</span>
        <span class='tech-tag'>SQLite</span>
        <span class='tech-tag'>Pandas</span>
        <span class='tech-tag'>openpyxl</span>
        <span class='tech-tag'>Prompt Engineering</span>
        <span class='tech-tag'>NL to SQL</span>
        <span class='tech-tag'>ETL Pipeline</span>
    </div>
""", unsafe_allow_html=True)

# Data pipeline
st.markdown("<div class='section-label'>DATA PIPELINE</div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>How the data gets in</div>", unsafe_allow_html=True)
st.markdown("""
    <div class='section-text'>
        Raw Excel reports from Aker's property management system are processed by a custom ETL pipeline (<code>script.py</code>)
        that cleans, standardizes, and loads data into four SQLite tables - <code>lease_charges</code>, <code>property_summary</code>,
        <code>summary_groups</code>, and <code>charge_code_summary</code>. The pipeline handles forward-filling, date normalization,
        property ID extraction, placeholder row filtering, and charge code aggregation automatically. Each table serves a distinct purpose:
        <code>lease_charges</code> stores resident-level data, <code>property_summary</code> tracks portfolio-wide occupancy metrics,
        <code>summary_groups</code> captures resident type breakdowns and deposit totals, and <code>charge_code_summary</code> aggregates
        revenue by charge type per property.
    </div>
""", unsafe_allow_html=True)