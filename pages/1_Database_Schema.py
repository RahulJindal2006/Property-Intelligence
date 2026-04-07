import streamlit as st
from sidebar import render_sidebar, render_css

st.set_page_config(page_title="Database Schema", page_icon="photos/logo.jpeg")

render_css()
render_sidebar()

st.markdown("""
    <style>
    .schema-hero {
        padding: 10px 0 32px 0;
        border-bottom: 1px solid rgba(128,128,128,0.15);
        margin-bottom: 36px;
    }
    .schema-hero-title {
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 6px;
    }
    .schema-hero-sub {
        font-size: 14px;
        color: #6b7280;
        line-height: 1.6;
    }
    .schema-stats {
        display: flex;
        gap: 16px;
        margin-bottom: 36px;
    }
    .schema-stat-card {
        background: rgba(99,102,241,0.06);
        border: 1px solid rgba(99,102,241,0.15);
        border-radius: 12px;
        padding: 16px 24px;
        flex: 1;
        text-align: center;
    }
    .schema-stat-number {
        font-size: 26px;
        font-weight: 800;
        color: #a5b4fc;
        margin-bottom: 4px;
    }
    .schema-stat-label {
        font-size: 12px;
        color: #6b7280;
        font-weight: 600;
        letter-spacing: 0.4px;
    }
    .table-section-label {
        font-size: 11px;
        font-weight: 700;
        color: #6366f1;
        letter-spacing: 1.2px;
        margin-bottom: 8px;
    }
    .table-title {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 6px;
        letter-spacing: -0.3px;
    }
    .table-desc {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 20px;
        line-height: 1.6;
    }
    .field-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 10px;
        margin-bottom: 32px;
    }
    .field-card {
        background: rgba(99,102,241,0.04);
        border: 1px solid rgba(99,102,241,0.12);
        border-radius: 10px;
        padding: 12px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .field-name {
        font-size: 13px;
        font-weight: 700;
        font-family: 'Courier New', monospace;
        color: #e2e8f0;
    }
    .field-type {
        font-size: 11px;
        font-weight: 600;
        color: #6366f1;
        background: rgba(99,102,241,0.1);
        border-radius: 4px;
        padding: 2px 8px;
    }
    .field-note {
        font-size: 11px;
        color: #9ca3af;
        margin-top: 3px;
    }
    </style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
    <div class='schema-hero'>
        <div class='schema-hero-title'>Database Schema</div>
        <div class='schema-hero-sub'>
            Four SQLite tables power the Property Management AI Assistant.
            Every question you ask is translated into a query against one or more of these tables.
        </div>
    </div>
""", unsafe_allow_html=True)

# Stats bar
st.markdown("""
    <div class='schema-stats'>
        <div class='schema-stat-card'>
            <div class='schema-stat-number'>4</div>
            <div class='schema-stat-label'>TABLES</div>
        </div>
        <div class='schema-stat-card'>
            <div class='schema-stat-number'>53</div>
            <div class='schema-stat-label'>TOTAL COLUMNS</div>
        </div>
        <div class='schema-stat-card'>
            <div class='schema-stat-number'>16</div>
            <div class='schema-stat-label'>PROPERTIES</div>
        </div>
        <div class='schema-stat-card'>
            <div class='schema-stat-number'>SQLite</div>
            <div class='schema-stat-label'>DATABASE ENGINE</div>
        </div>
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs(["  LEASE_CHARGES  ", "  PROPERTY_SUMMARY  ", "  SUMMARY_GROUPS  ", "  CHARGE_CODE_SUMMARY  "])

with tabs[0]:
    st.markdown("""
        <div class='table-section-label'>TABLE 1 OF 4</div>
        <div class='table-title'>LEASE_CHARGES</div>
        <div class='table-desc'>
            The core resident-level table. Each row represents a single charge line for a resident -
            including rent, amenity fees, and parking. Resident identity columns are forward-filled
            across multiple charge rows per unit.
        </div>
        <div class='field-grid'>
            <div class='field-card'><div><div class='field-name'>Unit</div><div class='field-note'>Unit number within the property</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Unit_Type</div><div class='field-note'>e.g. 1BR, 2BR, Studio</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Sq_Ft</div><div class='field-note'>Square footage of the unit</div></div><span class='field-type'>INTEGER</span></div>
            <div class='field-card'><div><div class='field-name'>Resident_ID</div><div class='field-note'>Unique resident identifier</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Name</div><div class='field-note'>Resident name (e.g. Resident 42)</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Market_Rent</div><div class='field-note'>Listed market rent for the unit</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Charge_Code</div><div class='field-note'>RENT, AMENITY, PARKING, PETFEEM, etc.</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Amount</div><div class='field-note'>Charge amount for this line</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Resident_Deposit</div><div class='field-note'>Security deposit held</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Other_Deposit</div><div class='field-note'>Additional deposits (e.g. pet)</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Move_In</div><div class='field-note'>Lease start date (YYYY-MM-DD)</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Lease_Expiration</div><div class='field-note'>Lease end date (YYYY-MM-DD)</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Move_Out</div><div class='field-note'>Move-out date if applicable</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Balance</div><div class='field-note'>Outstanding balance owed</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Property_ID</div><div class='field-note'>Short code e.g. 126r, 144r</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Source_Property_Name</div><div class='field-note'>Full property name</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Report_Date</div><div class='field-note'>Date the report was generated</div></div><span class='field-type'>TEXT</span></div>
        </div>
    """, unsafe_allow_html=True)
    st.code("""SELECT * FROM lease_charges WHERE Charge_Code = 'RENT' LIMIT 5;""", language="sql")

with tabs[1]:
    st.markdown("""
        <div class='table-section-label'>TABLE 2 OF 4</div>
        <div class='table-title'>PROPERTY_SUMMARY</div>
        <div class='table-desc'>
            Property-level occupancy and leasing statistics. Each row represents one building or
            property group. Used for portfolio-wide metrics like occupancy rates, vacancy counts,
            and leasing trends. Always filter <code>Total_Units &gt; 0</code> to exclude placeholder rows.
        </div>
        <div class='field-grid'>
            <div class='field-card'><div><div class='field-name'>Property_ID</div><div class='field-note'>Short code e.g. 126r, 153a</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Property_Name</div><div class='field-note'>Full display name of property</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Avg_Sq_Ft</div><div class='field-note'>Average unit square footage</div></div><span class='field-type'>INTEGER</span></div>
            <div class='field-card'><div><div class='field-name'>Avg_Rent</div><div class='field-note'>Average rent across units</div></div><span class='field-type'>INTEGER</span></div>
            <div class='field-card'><div><div class='field-name'>Total_Units</div><div class='field-note'>Total unit count (filter &gt; 0)</div></div><span class='field-type'>INTEGER</span></div>
            <div class='field-card'><div><div class='field-name'>Occ_No_Notice</div><div class='field-note'>Occupied, no notice to vacate</div></div><span class='field-type'>INTEGER</span></div>
            <div class='field-card'><div><div class='field-name'>Vacant_Rented</div><div class='field-note'>Vacant but already rented</div></div><span class='field-type'>INTEGER</span></div>
            <div class='field-card'><div><div class='field-name'>Vacant_Unrented</div><div class='field-note'>Vacant and not yet rented</div></div><span class='field-type'>INTEGER</span></div>
            <div class='field-card'><div><div class='field-name'>Notice_Rented</div><div class='field-note'>Notice given, replacement rented</div></div><span class='field-type'>INTEGER</span></div>
            <div class='field-card'><div><div class='field-name'>Notice_Unrented</div><div class='field-note'>Notice given, not yet rented</div></div><span class='field-type'>INTEGER</span></div>
            <div class='field-card'><div><div class='field-name'>Available</div><div class='field-note'>Total available units</div></div><span class='field-type'>INTEGER</span></div>
            <div class='field-card'><div><div class='field-name'>Model</div><div class='field-note'>Model/show units</div></div><span class='field-type'>INTEGER</span></div>
            <div class='field-card'><div><div class='field-name'>Down</div><div class='field-note'>Units taken offline</div></div><span class='field-type'>INTEGER</span></div>
            <div class='field-card'><div><div class='field-name'>Admin</div><div class='field-note'>Admin/employee units</div></div><span class='field-type'>INTEGER</span></div>
            <div class='field-card'><div><div class='field-name'>Pct_Occ</div><div class='field-note'>Occupancy % (primary metric)</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Pct_Occ_NonRev</div><div class='field-note'>Occupancy % excl. non-revenue</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Pct_Leased</div><div class='field-note'>Leased % including notices</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Pct_Trend</div><div class='field-note'>Trending occupancy indicator</div></div><span class='field-type'>REAL</span></div>
        </div>
    """, unsafe_allow_html=True)
    st.code("""SELECT Property_Name, Total_Units, Pct_Occ, Pct_Leased FROM property_summary WHERE Total_Units > 0 ORDER BY Pct_Occ DESC;""", language="sql")

with tabs[2]:
    st.markdown("""
        <div class='table-section-label'>TABLE 3 OF 4</div>
        <div class='table-title'>SUMMARY_GROUPS</div>
        <div class='table-desc'>
            Aggregated statistics broken down by resident type per property. Each row represents 
            one resident category (Current/Notice/Vacant, Future Applicants, Occupied Units, etc.) 
            for a given property. Useful for pipeline analysis, deposit totals, and occupancy breakdowns.
        </div>
        <div class='field-grid'>
            <div class='field-card'><div><div class='field-name'>Resident_Type</div><div class='field-note'>Current/Notice/Vacant, Future Residents, Occupied Units, etc.</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Sq_Ft</div><div class='field-note'>Total square footage for this group</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Market_Rent</div><div class='field-note'>Total market rent for this group</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Lease_Charges</div><div class='field-note'>Total lease charges billed</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Security_Deposit</div><div class='field-note'>Total security deposits held</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Other_Deposits</div><div class='field-note'>Total other deposits held</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Num_Units</div><div class='field-note'>Number of units in this group</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Pct_Unit_Occupancy</div><div class='field-note'>% of units occupied in this group</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Pct_Sqft_Occupied</div><div class='field-note'>% of sq ft occupied in this group</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Balance</div><div class='field-note'>Total outstanding balance for group</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Property_ID</div><div class='field-note'>Short code e.g. 126r, 144r</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Property_Name</div><div class='field-note'>Full display name of property</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Report_Date</div><div class='field-note'>Date the report was generated</div></div><span class='field-type'>TEXT</span></div>
        </div>
    """, unsafe_allow_html=True)
    st.code("""SELECT Property_Name, Resident_Type, Num_Units, Security_Deposit FROM summary_groups WHERE Resident_Type = 'Future Residents/Applicants' ORDER BY Num_Units DESC;""", language="sql")

with tabs[3]:
    st.markdown("""
        <div class='table-section-label'>TABLE 4 OF 4</div>
        <div class='table-title'>CHARGE_CODE_SUMMARY</div>
        <div class='table-desc'>
            Property-level revenue breakdown by charge code. Each row represents the total amount 
            collected for one charge type at one property - including RENT, PARKING, AMENITY, 
            PETFEEM, TRASH, STORAGE, and many more. Useful for revenue analysis across charge types.
        </div>
        <div class='field-grid'>
            <div class='field-card'><div><div class='field-name'>Charge_Code</div><div class='field-note'>e.g. RENT, PARKING, PETFEEM, TRASH, STORAGE</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Amount</div><div class='field-note'>Total revenue for this charge code at this property</div></div><span class='field-type'>REAL</span></div>
            <div class='field-card'><div><div class='field-name'>Property_ID</div><div class='field-note'>Short code e.g. 126r, 144r</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Property_Name</div><div class='field-note'>Full display name of property</div></div><span class='field-type'>TEXT</span></div>
            <div class='field-card'><div><div class='field-name'>Report_Date</div><div class='field-note'>Date the report was generated</div></div><span class='field-type'>TEXT</span></div>
        </div>
    """, unsafe_allow_html=True)
    st.code("""SELECT Charge_Code, SUM(Amount) as Total_Revenue FROM charge_code_summary GROUP BY Charge_Code ORDER BY Total_Revenue DESC;""", language="sql")