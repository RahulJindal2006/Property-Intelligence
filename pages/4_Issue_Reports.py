import streamlit as st
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
from sidebar import render_sidebar, render_css

st.set_page_config(page_title="Issue Reports", page_icon="photos/logo.jpeg")
render_css()
render_sidebar()

current_dir = Path(__file__)
root_dir = Path(__file__).parent.parent
issues_file = f"{root_dir}/issues.csv"
resolved_file = f"{root_dir}/resolved_issues.csv"

# Password protection
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.markdown("""
        <style>
        .stTextInput div[data-testid="InputInstructions"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l, col, col_r = st.columns([1, 2, 1])
    with col:
        st.markdown("""
            <div style='
                background: rgba(99,102,241,0.06);
                border: 1px solid rgba(99,102,241,0.2);
                border-radius: 16px;
                padding: 48px 40px 40px 40px;
                text-align: center;
                margin-bottom: 24px;
            '>
                <div style='font-size: 32px; margin-bottom: 14px;'>🔒</div>
                <div style='font-size: 24px; font-weight: 800; margin-bottom: 8px;'>Admin Access Required</div>
                <div style='font-size: 13px; color: #6b7280; line-height: 1.6;'>
                    This page is restricted to authorized Aker administrators only.
                </div>
            </div>
        """, unsafe_allow_html=True)
        password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter admin password")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        clicked = st.button("Login", use_container_width=True)
        if clicked or password:
            if password == "Aker":
                st.session_state.admin_authenticated = True
                st.rerun()
            elif clicked:
                st.error("Incorrect password. Access denied.")
    st.stop()

st.markdown("""
    <style>
    .stTextInput div[data-testid="InputInstructions"] {
        display: none !important;
    }
    .ir-hero {
        padding: 10px 0 28px 0;
        border-bottom: 1px solid rgba(128,128,128,0.15);
        margin-bottom: 32px;
    }
    .ir-hero-title { font-size: 32px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 6px; }
    .ir-hero-sub { font-size: 14px; color: #6b7280; }
    .ir-section-label {
        font-size: 11px; font-weight: 700; color: #6366f1;
        letter-spacing: 1.2px; margin-bottom: 12px; margin-top: 36px;
    }
    .ir-section-title { font-size: 20px; font-weight: 800; margin-bottom: 16px; }
    .issue-card {
        background: rgba(99,102,241,0.04);
        border: 1px solid rgba(99,102,241,0.15);
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 12px;
    }
    .issue-card-high { border-left: 4px solid #ef4444; }
    .issue-card-medium { border-left: 4px solid #f59e0b; }
    .issue-card-low { border-left: 4px solid #6366f1; }
    .issue-meta {
        display: flex; align-items: center; gap: 10px;
        margin-bottom: 8px; flex-wrap: wrap;
    }
    .severity-badge {
        font-size: 11px; font-weight: 700; letter-spacing: 0.5px;
        border-radius: 20px; padding: 3px 10px;
    }
    .badge-high { background: rgba(239,68,68,0.12); color: #ef4444; }
    .badge-medium { background: rgba(245,158,11,0.12); color: #f59e0b; }
    .badge-low { background: rgba(99,102,241,0.12); color: #a5b4fc; }
    .issue-date { font-size: 12px; color: #6b7280; }
    .issue-question { font-size: 15px; font-weight: 700; margin-bottom: 4px; }
    .issue-desc { font-size: 13px; color: #9ca3af; }
    .resolved-card {
        background: rgba(34,197,94,0.03);
        border: 1px solid rgba(34,197,94,0.15);
        border-left: 4px solid #22c55e;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 12px;
        opacity: 0.75;
    }
    .resolved-badge {
        font-size: 11px; font-weight: 700; letter-spacing: 0.5px;
        border-radius: 20px; padding: 3px 10px;
        background: rgba(34,197,94,0.12); color: #22c55e;
    }
    .stButton > button {
        border-radius: 20px !important;
        padding: 6px 16px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        border: 1px solid rgba(99,102,241,0.35) !important;
        color: #a5b4fc !important;
        background: rgba(99,102,241,0.08) !important;
        letter-spacing: 0.3px !important;
    }
    .stButton > button:hover {
        background: rgba(99,102,241,0.18) !important;
        border-color: #6366f1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
    <div class='ir-hero'>
        <div class='ir-hero-title'>Issue Reports</div>
        <div class='ir-hero-sub'>All issues reported by users of the Property Management AI Assistant.</div>
    </div>
""", unsafe_allow_html=True)

if os.path.exists(issues_file):
    df_raw = pd.read_csv(issues_file)
    df_raw['Timestamp'] = pd.to_datetime(df_raw['Timestamp'])

    # Load resolved issues
    if os.path.exists(resolved_file):
        df_resolved = pd.read_csv(resolved_file)
        df_resolved['Timestamp'] = pd.to_datetime(df_resolved['Timestamp'])
    else:
        df_resolved = pd.DataFrame(columns=df_raw.columns)

    # Filter out resolved using Timestamp + Question as unique key
    if not df_resolved.empty and 'Question' in df_resolved.columns:
        resolved_keys = set(
            zip(df_resolved['Timestamp'].astype(str), df_resolved['Question'])
        )
        df_open = df_raw[
            ~df_raw.apply(lambda r: (str(r['Timestamp']), r['Question']) in resolved_keys, axis=1)
        ].copy()
    else:
        df_open = df_raw.copy()

    # Summary metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Issues", len(df_raw))
    with col2:
        st.metric("Open", len(df_open))
    with col3:
        st.metric("High Severity", len(df_open[df_open['Severity'] == 'High']))
    with col4:
        st.metric("Medium Severity", len(df_open[df_open['Severity'] == 'Medium']))
    with col5:
        st.metric("Low Severity", len(df_open[df_open['Severity'] == 'Low']))

    st.divider()

    # Filter
    severity_filter = st.selectbox("Filter by Severity", ["All", "High", "Medium", "Low"])
    df_display = df_open.copy()
    if severity_filter != "All":
        df_display = df_display[df_display['Severity'] == severity_filter]

    # Open issues
    st.markdown("<div class='ir-section-label'>OPEN ISSUES</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='ir-section-title'>{len(df_display)} Issue{'s' if len(df_display) != 1 else ''} Need Attention</div>", unsafe_allow_html=True)

    if df_display.empty:
        st.info("No open issues matching this filter.")
    else:
        for i, row in df_display.iterrows():
            severity = row.get('Severity', 'Low')
            badge_class = f"badge-{severity.lower()}"
            card_class = f"issue-card issue-card-{severity.lower()}"
            date_str = row['Timestamp'].strftime('%b %d, %Y at %I:%M %p')

            st.markdown(f"""
                <div class='{card_class}'>
                    <div class='issue-meta'>
                        <span class='severity-badge {badge_class}'>{severity.upper()}</span>
                        <span class='issue-date'>{date_str}</span>
                    </div>
                    <div class='issue-question'>{row['Question']}</div>
                    <div class='issue-desc'>{row['What_Went_Wrong']}</div>
                </div>
            """, unsafe_allow_html=True)

            btn_col1, btn_col2, _ = st.columns([1.2, 1.2, 5])
            with btn_col1:
                if st.button("Mark Resolved", key=f"resolve_{i}"):
                    resolved_row = pd.DataFrame([{
                        'Timestamp': row['Timestamp'],
                        'Question': row['Question'],
                        'What_Went_Wrong': row['What_Went_Wrong'],
                        'Severity': row['Severity'],
                        'Resolved_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }])
                    if os.path.exists(resolved_file):
                        existing = pd.read_csv(resolved_file)
                        pd.concat([existing, resolved_row], ignore_index=True).to_csv(resolved_file, index=False)
                    else:
                        resolved_row.to_csv(resolved_file, index=False)
                    st.success("Marked as resolved!")
                    st.rerun()
            with btn_col2:
                if st.button("Run Prompt", key=f"run_{i}"):
                    st.session_state.example_prompt = row['Question']
                    st.session_state.last_prompt = ""
                    st.switch_page("1_home.py")

    # Resolved issues section
    if not df_resolved.empty:
        st.markdown("<div class='ir-section-label'>RESOLVED ISSUES</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='ir-section-title'>{len(df_resolved)} Resolved</div>", unsafe_allow_html=True)

        for i, row in df_resolved.iterrows():
            resolved_at = row.get('Resolved_At', 'Unknown')
            date_str = row['Timestamp'].strftime('%b %d, %Y at %I:%M %p')
            st.markdown(f"""
                <div class='resolved-card'>
                    <div class='issue-meta'>
                        <span class='resolved-badge'>RESOLVED</span>
                        <span class='issue-date'>Reported: {date_str}</span>
                        <span class='issue-date'>· Resolved: {resolved_at}</span>
                    </div>
                    <div class='issue-question'>{row['Question']}</div>
                    <div class='issue-desc'>{row['What_Went_Wrong']}</div>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    csv = df_raw.to_csv(index=False)
    st.download_button(
        label="Download All Issues as CSV",
        data=csv,
        file_name="issue_reports.csv",
        mime="text/csv"
    )

else:
    st.info("No issues have been reported yet.")

if st.button("Logout"):
    st.session_state.admin_authenticated = False
    st.rerun()