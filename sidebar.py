import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("""
            <div style='padding: 0 0 16px 0;'>
                <div style='font-size: 18px; font-weight: 700; letter-spacing: -0.3px;'>🏢 Aker Companies</div>
                <div style='font-size: 11px; color: #6366f1; margin-top: 5px; font-weight: 600; letter-spacing: 0.4px;'>PROPERTY INSIGHTS HUB</div>
            </div>
            <hr style='margin: 0 0 16px 0;'>
            <div style='font-size: 11px; color: #6b7280; letter-spacing: 0.8px; margin-bottom: 12px;'>CONTACT</div>
            <div style='margin-bottom: 10px;'>
                <div style='font-size: 12px; color: #6b7280; margin-bottom: 4px;'>📧 Email</div>
                <a href='mailto:jind3091@mylaurier.ca' style='font-size: 13px; color: #6366f1; text-decoration: none;'>jind3091@mylaurier.ca</a>
            </div>
            <div style='margin-bottom: 10px;'>
                <div style='font-size: 12px; color: #6b7280; margin-bottom: 4px;'>💼 LinkedIn</div>
                <a href='https://www.linkedin.com/in/rahuljindal-cs/' target='_blank' style='font-size: 13px; color: #6366f1; text-decoration: none;'>rahuljindal-cs</a>
            </div>
            <div style='margin-bottom: 10px;'>
                <div style='font-size: 12px; color: #6b7280; margin-bottom: 4px;'>🐙 GitHub</div>
                <a href='https://github.com/RahulJindal2006' target='_blank' style='font-size: 13px; color: #6366f1; text-decoration: none;'>RahulJindal2006</a>
            </div>
            <div style='margin-bottom: 20px;'>
                <div style='font-size: 12px; color: #6b7280; margin-bottom: 4px;'>🏢 Aker Companies</div>
                <a href='https://akercompanies.com/' target='_blank' style='font-size: 13px; color: #6366f1; text-decoration: none;'>akercompanies.com</a>
            </div>
            <hr style='margin: 0 0 12px 0;'>
            <div style='font-size: 11px; color: #6b7280; line-height: 1.6;'>
                💡 Something not quite right? Visit the <strong>Report an Issue</strong> tab and let us know - every piece of feedback is reviewed and taken seriously.
            </div>
        """, unsafe_allow_html=True)

def render_css():
    st.markdown("""
        <style>
        /* Hide deploy button and menu */
        [data-testid="stToolbar"] {visibility: hidden;}
        [data-testid="stDecoration"] {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Sidebar nav links - ALL CAPS */
        [data-testid="stSidebarNav"] a span {
            text-transform: uppercase !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
        }
        
        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }

        /* Purple accent top border */
        .stApp::before {
            content: '';
            display: block;
            position: fixed;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, #6366f1, #8b5cf6, #a78bfa);
            z-index: 999999;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(128,128,128,0.2);
            padding-top: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)