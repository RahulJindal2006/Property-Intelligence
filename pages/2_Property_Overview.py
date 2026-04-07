import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
from sidebar import render_sidebar, render_css

st.set_page_config(page_title="Property Overview", page_icon="photos/logo.jpeg")
render_css()
render_sidebar()

st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background: rgba(99,102,241,0.1);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 12px;
        padding: 16px 20px;
    }
    .section-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 6px;
        margin-top: 8px;
    }
    .section-sub {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 16px;
    }
    </style>
""", unsafe_allow_html=True)

root_dir = Path(__file__).parent.parent
db_path = f"{root_dir}/PropertyManagement.db"
conn = sqlite3.connect(db_path)

# --- Metrics ---
total_props = pd.read_sql_query(
    "SELECT COUNT(DISTINCT Property_Name) as c FROM property_summary WHERE Total_Units > 0", conn).iloc[0,0]
total_units = pd.read_sql_query(
    "SELECT SUM(Total_Units) as c FROM property_summary WHERE Total_Units > 0", conn).iloc[0,0]
avg_occ = pd.read_sql_query(
    "SELECT ROUND(AVG(Pct_Occ), 2) as c FROM property_summary WHERE Pct_Occ > 0 AND Total_Units > 0", conn).iloc[0,0]
total_vacant = pd.read_sql_query(
    "SELECT SUM(Vacant_Rented + Vacant_Unrented) as c FROM property_summary WHERE Total_Units > 0", conn).iloc[0,0]
total_future = pd.read_sql_query(
    "SELECT SUM(Num_Units) as c FROM summary_groups WHERE Resident_Type = 'Future Residents/Applicants'", conn).iloc[0,0]
total_deposits = pd.read_sql_query(
    "SELECT ROUND(SUM(Security_Deposit), 2) as c FROM summary_groups WHERE Resident_Type = 'Current/Notice/Vacant Residents'", conn).iloc[0,0]

conn.close()


st.title("Property Overview")
st.write("A live summary of all your properties pulled directly from the database.")

# Row 1 - Core metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Properties", int(total_props))
with col2:
    st.metric("Total Units", int(total_units))
with col3:
    st.metric("Avg Occupancy", f"{avg_occ}%")

st.markdown("<br>", unsafe_allow_html=True)

# Row 2 - New metrics
col4, col5, col6 = st.columns(3)
with col4:
    st.metric("Total Vacant Units", int(total_vacant))
with col5:
    st.metric("Future Applicants", int(total_future) if total_future else 0)
with col6:
    formatted_deposits = f"${total_deposits:,.0f}" if total_deposits else "$0"
    st.metric("Total Security Deposits", formatted_deposits)

st.divider()

# --- All Properties Table ---
conn2 = sqlite3.connect(db_path)

st.markdown("<div class='section-title'>All Properties</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Sorted by occupancy. Grouped by property name across buildings.</div>", unsafe_allow_html=True)

df = pd.read_sql_query("""
    SELECT 
        Property_Name,
        SUM(Total_Units) as Total_Units,
        SUM(Occ_No_Notice) as Occupied,
        SUM(Vacant_Rented) as Vacant_Rented,
        SUM(Vacant_Unrented) as Vacant_Unrented,
        SUM(Available) as Available_Units,
        ROUND(AVG(Pct_Occ), 2) as Occupancy_Pct,
        ROUND(AVG(Pct_Leased), 2) as Leased_Pct,
        ROUND(AVG(Pct_Trend), 2) as Trend_Pct
    FROM property_summary
    WHERE Total_Units > 0
    GROUP BY Property_Name
    ORDER BY Occupancy_Pct DESC
""", conn2)

df = df.rename(columns={
    'Property_Name': 'Property',
    'Total_Units': 'Total Units',
    'Vacant_Rented': 'Vacant (Rented)',
    'Vacant_Unrented': 'Vacant (Unrented)',
    'Available_Units': 'Available Units',
    'Occupancy_Pct': 'Occupancy %',
    'Leased_Pct': 'Leased %',
    'Trend_Pct': 'Trend %'
})
df = df.reset_index(drop=True)
df.index = df.index + 1
st.dataframe(df, use_container_width=True)

st.divider()

# --- Revenue by Charge Code ---
st.markdown("<div class='section-title'>Revenue by Charge Code</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Total revenue collected per charge type across all properties.</div>", unsafe_allow_html=True)

df_charges = pd.read_sql_query("""
    SELECT 
        Charge_Code,
        ROUND(SUM(Amount), 2) as Total_Revenue,
        COUNT(DISTINCT Property_ID) as Properties
    FROM charge_code_summary
    GROUP BY Charge_Code
    ORDER BY Total_Revenue DESC
""", conn2)

df_charges = df_charges.rename(columns={
    'Charge_Code': 'Charge Code',
    'Total_Revenue': 'Total Revenue ($)',
    'Properties': 'Properties'
})
df_charges['Total Revenue ($)'] = df_charges['Total Revenue ($)'].apply(lambda x: f"${x:,.2f}")
df_charges = df_charges.reset_index(drop=True)
df_charges.index = df_charges.index + 1
st.dataframe(df_charges, use_container_width=True)

st.divider()

# --- Security Deposits by Property ---
st.markdown("<div class='section-title'>Security Deposits by Property</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Total security deposits held per property for current and notice residents.</div>", unsafe_allow_html=True)

df_deposits = pd.read_sql_query("""
    SELECT 
        Property_Name,
        ROUND(SUM(Security_Deposit), 2) as Total_Security_Deposit,
        ROUND(SUM(Other_Deposits), 2) as Total_Other_Deposits,
        ROUND(SUM(Security_Deposit + Other_Deposits), 2) as Total_Deposits
    FROM summary_groups
    WHERE Resident_Type = 'Current/Notice/Vacant Residents'
    GROUP BY Property_Name
    ORDER BY Total_Security_Deposit DESC
""", conn2)

df_deposits = df_deposits.rename(columns={
    'Property_Name': 'Property',
    'Total_Security_Deposit': 'Security Deposit ($)',
    'Total_Other_Deposits': 'Other Deposits ($)',
    'Total_Deposits': 'Total Deposits ($)'
})
for col in ['Security Deposit ($)', 'Other Deposits ($)', 'Total Deposits ($)']:
    df_deposits[col] = df_deposits[col].apply(lambda x: f"${x:,.2f}")
df_deposits = df_deposits.reset_index(drop=True)
df_deposits.index = df_deposits.index + 1
st.dataframe(df_deposits, use_container_width=True)

conn2.close()

st.divider()

st.markdown("<div class='section-title'>Charge Code Reference</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Definitions for all charge codes used across properties.</div>", unsafe_allow_html=True)

charge_codes = {
    "Revenue Charges": [
        ("RENT", "Standard monthly rent charge for the unit"),
        ("RENTAFF", "Affordable housing rent - reduced rate for income-qualified residents"),
        ("RENTRETL", "Retail unit rent - charged for commercial/retail spaces"),
        ("RNTPROF", "Professional or corporate rent rate"),
        ("RENTHAP", "Housing assistance program rent - subsidized rent rate"),
        ("MTM", "Month-to-month premium - extra charge for residents on a month-to-month lease"),
    ],
    "Amenity & Unit Charges": [
        ("AMENITY", "Monthly amenity fee for access to shared building amenities"),
        ("PARKING", "Monthly parking space charge"),
        ("GARAGE", "Monthly garage unit charge"),
        ("STORAGE", "Monthly storage unit charge"),
        ("BIKE", "Monthly bike storage charge"),
        ("W/D", "Washer/dryer unit charge"),
        ("HOMEPCKG", "Home package bundle - includes multiple amenities or services"),
    ],
    "Utility & Fee Charges": [
        ("PETFEEM", "Monthly pet fee for residents with pets"),
        ("PETFEE", "One-time or alternative pet fee"),
        ("TRASH", "Monthly trash/waste removal fee"),
        ("WATER", "Monthly water utility charge"),
        ("UTILCOM", "Common area utility charge"),
        ("SDFEE", "Same-day or service delivery fee"),
        ("SALESTX", "Sales tax applied to applicable charges"),
        ("CAMEST", "Common area maintenance estimate charge"),
        ("CAMINSR", "Common area maintenance insurance charge"),
        ("RETXEST", "Real estate tax estimate charge passed through to resident"),
    ],
    "Subsidies & Credits": [
        ("SUBSIDY", "Government or program subsidy applied to resident account"),
        ("SEC8CRD", "Section 8 housing voucher credit - government housing assistance"),
    ],
    "Concessions (Negative Charges)": [
        ("CONRENT", "Rent concession - discount applied to monthly rent (e.g. first month free)"),
        ("CONPARK", "Parking concession - free or discounted parking offered as incentive"),
        ("CONGAR", "Garage concession - free or discounted garage unit"),
        ("CONSTOR", "Storage concession - free or discounted storage unit"),
        ("CONPETM", "Pet fee concession - waived or reduced pet fee"),
        ("CONAMEN", "Amenity concession - waived or discounted amenity fee"),
        ("CONEMP", "Employee concession - discounted rent for property staff living on-site"),
    ],
}

for category, codes in charge_codes.items():
    st.markdown(f"""
        <div style='margin-top: 28px; margin-bottom: 12px;'>
            <div style='font-size: 11px; font-weight: 700; color: #6366f1; letter-spacing: 1.2px; margin-bottom: 8px;'>{category.upper()}</div>
        </div>
    """, unsafe_allow_html=True)

    for code, description in codes:
        st.markdown(f"""
            <div style='
                background: rgba(99,102,241,0.04);
                border: 1px solid rgba(99,102,241,0.12);
                border-radius: 10px;
                padding: 12px 16px;
                margin-bottom: 8px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 16px;
            '>
                <div style='font-size: 13px; font-weight: 700; font-family: monospace; color: #e2e8f0; min-width: 100px;'>{code}</div>
                <div style='font-size: 13px; color: #9ca3af; flex: 1;'>{description}</div>
            </div>
        """, unsafe_allow_html=True)