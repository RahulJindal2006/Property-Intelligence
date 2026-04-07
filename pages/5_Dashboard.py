import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from sidebar import render_sidebar, render_css

st.set_page_config(page_title="Dashboard", page_icon="photos/logo.jpeg")
render_css()
render_sidebar()

current_dir = Path(__file__)
root_dir = Path(__file__).parent.parent
db_path = f"{root_dir}/PropertyManagement.db"

conn = sqlite3.connect(db_path)
df_summary = pd.read_sql_query("SELECT * FROM property_summary WHERE Total_Units > 0", conn)
df_charges = pd.read_sql_query("SELECT * FROM lease_charges", conn)
df_summary_groups = pd.read_sql_query("SELECT * FROM summary_groups", conn)
df_charge_codes = pd.read_sql_query("SELECT * FROM charge_code_summary", conn)
avg_occ = pd.read_sql_query(
    "SELECT ROUND(AVG(Pct_Occ), 2) as Avg_Occupancy FROM property_summary WHERE Pct_Occ > 0 AND Total_Units > 0",
    conn
).iloc[0, 0]
conn.close()

df_props = df_summary.groupby('Property_Name').agg({
    'Total_Units': 'sum',
    'Occ_No_Notice': 'sum',
    'Vacant_Rented': 'sum',
    'Vacant_Unrented': 'sum',
    'Available': 'sum',
    'Pct_Occ': 'mean',
    'Pct_Leased': 'mean',
    'Avg_Rent': 'mean'
}).reset_index()

total_units = int(df_props['Total_Units'].sum())
total_vacant = int((df_props['Vacant_Rented'] + df_props['Vacant_Unrented']).sum())
total_residents = df_charges[
    (df_charges['Charge_Code'] == 'RENT') &
    (df_charges['Move_Out'].isna() | (df_charges['Move_Out'] == ''))
]['Resident_ID'].nunique()

# Theme
PURPLE        = '#6366f1'
PURPLE_LIGHT  = '#a5b4fc'
PURPLE_DARK   = '#4338ca'
GREEN         = '#22c55e'
RED           = '#ef4444'
AMBER         = '#f59e0b'
BG            = 'rgba(0,0,0,0)'
CARD_BG       = 'rgba(99,102,241,0.05)'
BORDER        = 'rgba(99,102,241,0.15)'
FONT_COLOR    = '#e2e8f0'
MUTED         = '#6b7280'
GRID_COLOR    = 'rgba(255,255,255,0.06)'

def base_layout(title="", height=420):
    return dict(
        title=dict(text=title, font=dict(size=15, color=FONT_COLOR, family='sans-serif'), x=0, pad=dict(b=10)),
        paper_bgcolor=CARD_BG,
        plot_bgcolor=BG,
        font=dict(color=FONT_COLOR, family='sans-serif', size=12),
        margin=dict(l=24, r=24, t=56, b=24),
        height=height,
        xaxis=dict(gridcolor=GRID_COLOR, showgrid=True, zeroline=False, linecolor=BORDER),
        yaxis=dict(gridcolor=GRID_COLOR, showgrid=True, zeroline=False, linecolor=BORDER),
        bargap=0.28,
        hoverlabel=dict(
            bgcolor='#1e1e2e',
            bordercolor=PURPLE,
            font=dict(color=FONT_COLOR, size=13)
        )
    )

st.markdown(f"""
    <style>
    .block-container {{ padding-top: 2rem; padding-bottom: 2rem; padding-left: 3rem; padding-right: 3rem; }}
    .dash-hero {{
        padding: 10px 0 28px 0;
        border-bottom: 1px solid rgba(128,128,128,0.15);
        margin-bottom: 36px;
    }}
    .dash-label {{
        font-size: 11px; font-weight: 700; color: {PURPLE};
        letter-spacing: 1.4px; margin-bottom: 6px;
    }}
    .dash-title {{ font-size: 32px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 6px; }}
    .dash-sub {{ font-size: 14px; color: {MUTED}; }}
    .section-label {{
        font-size: 11px; font-weight: 700; color: {PURPLE};
        letter-spacing: 1.2px; margin-bottom: 8px; margin-top: 44px;
    }}
    .section-title {{ font-size: 22px; font-weight: 800; margin-bottom: 4px; letter-spacing: -0.3px; }}
    .section-sub {{ font-size: 13px; color: {MUTED}; margin-bottom: 20px; }}
    .kpi-row {{ display: flex; gap: 16px; margin-bottom: 8px; }}
    .kpi-card {{
        flex: 1;
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 20px 24px;
        text-align: center;
    }}
    .kpi-label {{ font-size: 12px; color: {MUTED}; font-weight: 600; letter-spacing: 0.4px; margin-bottom: 8px; }}
    .kpi-value {{ font-size: 32px; font-weight: 800; color: {FONT_COLOR}; letter-spacing: -0.5px; }}
    .kpi-sub {{ font-size: 12px; color: {MUTED}; margin-top: 4px; }}
    [data-testid="stMetric"] {{ display: none; }}
    </style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
    <div class='dash-hero'>
        <div class='dash-label'>AKER INTELLIGENCE</div>
        <div class='dash-title'>Property Insights Dashboard</div>
        <div class='dash-sub'>Live portfolio metrics pulled directly from the property management database.</div>
    </div>
""", unsafe_allow_html=True)

# KPI Cards
st.markdown(f"""
    <div class='kpi-row'>
        <div class='kpi-card'>
            <div class='kpi-label'>TOTAL UNITS</div>
            <div class='kpi-value'>{total_units:,}</div>
            <div class='kpi-sub'>Across all properties</div>
        </div>
        <div class='kpi-card'>
            <div class='kpi-label'>AVG OCCUPANCY</div>
            <div class='kpi-value' style='color:{PURPLE_LIGHT}'>{avg_occ}%</div>
            <div class='kpi-sub'>Portfolio average</div>
        </div>
        <div class='kpi-card'>
            <div class='kpi-label'>TOTAL VACANT</div>
            <div class='kpi-value' style='color:{RED}'>{total_vacant:,}</div>
            <div class='kpi-sub'>Units available to lease</div>
        </div>
        <div class='kpi-card'>
            <div class='kpi-label'>TOTAL RESIDENTS</div>
            <div class='kpi-value' style='color:{GREEN}'>{total_residents:,}</div>
            <div class='kpi-sub'>Active lease holders</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.divider()

# --- Occupancy by Property ---
st.markdown("<div class='section-label'>OCCUPANCY</div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Occupancy Rate by Property</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Sorted from lowest to highest - red indicates properties needing attention.</div>", unsafe_allow_html=True)

df_occ = df_props.sort_values('Pct_Occ', ascending=True)

def occ_color(val):
    if val < 90:
        return RED
    elif val < 95:
        return AMBER
    else:
        return PURPLE

colors = [occ_color(v) for v in df_occ['Pct_Occ']]

fig_occ = go.Figure(go.Bar(
    x=df_occ['Pct_Occ'],
    y=df_occ['Property_Name'],
    orientation='h',
    marker=dict(color=colors, opacity=0.9, line=dict(width=0)),
    text=df_occ['Pct_Occ'].round(1).astype(str) + '%',
    textposition='outside',
    textfont=dict(color=FONT_COLOR, size=11),
    hovertemplate='<b>%{y}</b><br>Occupancy: %{x:.1f}%<extra></extra>'
))
layout = base_layout(height=520)
layout.update(dict(
    xaxis=dict(range=[0, 112], gridcolor=GRID_COLOR, showgrid=True, zeroline=False, ticksuffix='%'),
    yaxis=dict(gridcolor=GRID_COLOR, showgrid=False, zeroline=False),
))
fig_occ.update_layout(layout)
st.plotly_chart(fig_occ, use_container_width=True)

# --- Vacancy + Pie ---
st.markdown("<div class='section-label'>VACANCY</div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Vacancy Analysis</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Properties with vacant units and overall portfolio unit breakdown.</div>", unsafe_allow_html=True)

df_vac = df_props.copy()
df_vac['Total_Vacant'] = df_vac['Vacant_Rented'] + df_vac['Vacant_Unrented']
df_vac = df_vac[df_vac['Total_Vacant'] > 0].sort_values('Total_Vacant', ascending=False)

col_v1, col_v2 = st.columns([1.4, 1])

with col_v1:
    fig_vac = go.Figure()
    fig_vac.add_trace(go.Bar(
        name='Vacant (Rented)',
        x=df_vac['Property_Name'],
        y=df_vac['Vacant_Rented'],
        marker=dict(color=GREEN, opacity=0.85, line=dict(width=0)),
        hovertemplate='<b>%{x}</b><br>Vacant Rented: %{y}<extra></extra>'
    ))
    fig_vac.add_trace(go.Bar(
        name='Vacant (Unrented)',
        x=df_vac['Property_Name'],
        y=df_vac['Vacant_Unrented'],
        marker=dict(color=RED, opacity=0.85, line=dict(width=0)),
        hovertemplate='<b>%{x}</b><br>Vacant Unrented: %{y}<extra></extra>'
    ))
    layout2 = base_layout(height=420)
    layout2.update(dict(
        barmode='stack',
        xaxis=dict(tickangle=-35, gridcolor=GRID_COLOR, showgrid=False, zeroline=False),
        yaxis=dict(gridcolor=GRID_COLOR, showgrid=True, zeroline=False),
        legend=dict(font=dict(color=FONT_COLOR), bgcolor='rgba(0,0,0,0)', orientation='h', y=1.1)
    ))
    fig_vac.update_layout(layout2)
    st.plotly_chart(fig_vac, use_container_width=True)

with col_v2:
    occ_total    = int(df_props['Occ_No_Notice'].sum())
    vac_rented   = int(df_props['Vacant_Rented'].sum())
    vac_unrented = int(df_props['Vacant_Unrented'].sum())
    notice       = int(df_summary['Notice_Rented'].sum() + df_summary['Notice_Unrented'].sum())

    fig_pie = go.Figure(go.Pie(
        labels=['Occupied', 'Vacant (Rented)', 'Vacant (Unrented)', 'Notice Given'],
        values=[occ_total, vac_rented, vac_unrented, notice],
        hole=0.55,
        marker=dict(
            colors=[PURPLE, GREEN, RED, AMBER],
            line=dict(color='#0f0f1a', width=2)
        ),
        textfont=dict(color=FONT_COLOR, size=12),
        hovertemplate='%{label}<br>%{value} units (%{percent})<extra></extra>',
        textinfo='percent'
    ))
    fig_pie.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=BG,
        font=dict(color=FONT_COLOR, family='sans-serif'),
        margin=dict(l=16, r=16, t=40, b=16),
        height=420,
        legend=dict(
            font=dict(color=FONT_COLOR, size=12),
            bgcolor='rgba(0,0,0,0)',
            orientation='v',
            x=0, y=-0.15
        ),
        annotations=[dict(
            text=f'<b>{occ_total:,}</b><br><span style="font-size:11px">Occupied</span>',
            x=0.5, y=0.5, font=dict(size=16, color=FONT_COLOR),
            showarrow=False
        )]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- Rent ---
st.markdown("<div class='section-label'>RENT</div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Average Rent by Property</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Average monthly rent across all unit types per property.</div>", unsafe_allow_html=True)

df_rent = df_props.sort_values('Avg_Rent', ascending=False)
fig_rent = go.Figure(go.Bar(
    x=df_rent['Property_Name'],
    y=df_rent['Avg_Rent'],
    marker=dict(
        color=df_rent['Avg_Rent'],
        colorscale=[[0, PURPLE_DARK], [1, PURPLE_LIGHT]],
        showscale=False,
        opacity=0.9,
        line=dict(width=0)
    ),
    text=df_rent['Avg_Rent'].round(0).astype(int).apply(lambda x: f'${x:,}'),
    textposition='outside',
    textfont=dict(color=FONT_COLOR, size=11),
    hovertemplate='<b>%{x}</b><br>Avg Rent: $%{y:,.0f}<extra></extra>'
))
layout3 = base_layout(height=420)
layout3.update(dict(
    xaxis=dict(tickangle=-35, gridcolor=GRID_COLOR, showgrid=False, zeroline=False),
    yaxis=dict(gridcolor=GRID_COLOR, showgrid=True, zeroline=False, tickprefix='$')
))
fig_rent.update_layout(layout3)
st.plotly_chart(fig_rent, use_container_width=True)

# --- Revenue by Charge Code ---
st.markdown("<div class='section-label'>REVENUE</div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Revenue by Charge Code</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Total revenue collected per charge type. Rent shown separately - secondary charges and concessions shown below.</div>", unsafe_allow_html=True)

df_cc = df_charge_codes.groupby('Charge_Code')['Amount'].sum().reset_index()

# Split rent vs everything else
df_cc_other = df_cc[df_cc['Charge_Code'] != 'RENT'].sort_values('Amount', ascending=False)
df_cc_positive = df_cc_other[df_cc_other['Amount'] > 0]
df_cc_negative = df_cc_other[df_cc_other['Amount'] < 0]
total_rent = df_cc[df_cc['Charge_Code'] == 'RENT']['Amount'].sum()
total_other_positive = df_cc_positive['Amount'].sum()
total_concessions = df_cc_negative['Amount'].sum()

# Top KPI row
st.markdown(f"""
    <div class='kpi-row' style='margin-bottom: 24px;'>
        <div class='kpi-card'>
            <div class='kpi-label'>TOTAL RENT REVENUE</div>
            <div class='kpi-value' style='color:{GREEN}; font-size:26px;'>${total_rent:,.0f}</div>
            <div class='kpi-sub'>From RENT charge code</div>
        </div>
        <div class='kpi-card'>
            <div class='kpi-label'>OTHER REVENUE</div>
            <div class='kpi-value' style='color:{PURPLE_LIGHT}; font-size:26px;'>${total_other_positive:,.0f}</div>
            <div class='kpi-sub'>Parking, amenity, pet fees, etc.</div>
        </div>
        <div class='kpi-card'>
            <div class='kpi-label'>TOTAL CONCESSIONS</div>
            <div class='kpi-value' style='color:{RED}; font-size:26px;'>${total_concessions:,.0f}</div>
            <div class='kpi-sub'>Discounts and credits given</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Two columns - positive charges | negative concessions
# Secondary revenue - vertical bar
st.markdown(f"<div style='font-size:13px; color:{MUTED}; margin-bottom:10px;'>Secondary Revenue Sources</div>", unsafe_allow_html=True)
df_cc_positive_sorted = df_cc_positive.sort_values('Amount', ascending=False)
fig_pos = go.Figure(go.Bar(
    x=df_cc_positive_sorted['Charge_Code'],
    y=df_cc_positive_sorted['Amount'],
    marker=dict(
        color=df_cc_positive_sorted['Amount'],
        colorscale=[[0, PURPLE_DARK], [1, PURPLE_LIGHT]],
        showscale=False,
        opacity=0.9,
        line=dict(width=0)
    ),
    text=df_cc_positive_sorted['Amount'].apply(lambda x: f'${x:,.0f}'),
    textposition='outside',
    textfont=dict(color=FONT_COLOR, size=11),
    hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
))
layout_pos = base_layout(height=420)
layout_pos.update(dict(
    xaxis=dict(tickangle=-35, gridcolor=GRID_COLOR, showgrid=False, zeroline=False),
    yaxis=dict(gridcolor=GRID_COLOR, showgrid=True, zeroline=False,
               tickprefix='$', range=[0, df_cc_positive_sorted['Amount'].max() * 1.25]),
))
fig_pos.update_layout(layout_pos)
st.plotly_chart(fig_pos, use_container_width=True)

# Concessions - horizontal with fixed margins
st.markdown(f"<div style='font-size:13px; color:{MUTED}; margin-bottom:10px;'>Concessions & Credits</div>", unsafe_allow_html=True)
df_cc_negative_sorted = df_cc_negative.sort_values('Amount', ascending=False)
fig_neg = go.Figure(go.Bar(
    x=df_cc_negative_sorted['Charge_Code'],
    y=df_cc_negative_sorted['Amount'],
    marker=dict(color=RED, opacity=0.8, line=dict(width=0)),
    text=df_cc_negative_sorted['Amount'].apply(lambda x: f'${x:,.0f}'),
    textposition='outside',
    textfont=dict(color=FONT_COLOR, size=11),
    hovertemplate='<b>%{x}</b><br>Concession: $%{y:,.0f}<extra></extra>'
))
layout_neg = base_layout(height=420)
layout_neg.update(dict(
    xaxis=dict(tickangle=-35, gridcolor=GRID_COLOR, showgrid=False, zeroline=False),
    yaxis=dict(
        gridcolor=GRID_COLOR, showgrid=True, zeroline=True,
        zerolinecolor=BORDER, zerolinewidth=1, tickprefix='$',
        range=[df_cc_negative_sorted['Amount'].min() * 1.3, 0]
    ),
))
fig_neg.update_layout(layout_neg)
st.plotly_chart(fig_neg, use_container_width=True)

# --- Future Applicants ---
st.markdown("<div class='section-label'>PIPELINE</div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Future Applicants by Property</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Number of future residents and applicants waiting to move in per property.</div>", unsafe_allow_html=True)

df_future = df_summary_groups[
    df_summary_groups['Resident_Type'] == 'Future Residents/Applicants'
].groupby('Property_Name')['Num_Units'].sum().reset_index()
df_future = df_future[df_future['Num_Units'] > 0].sort_values('Num_Units', ascending=False)

fig_future = go.Figure(go.Bar(
    x=df_future['Property_Name'],
    y=df_future['Num_Units'],
    marker=dict(
        color=df_future['Num_Units'],
        colorscale=[[0, PURPLE_DARK], [1, PURPLE_LIGHT]],
        showscale=False,
        opacity=0.9,
        line=dict(width=0)
    ),
    text=df_future['Num_Units'].astype(int),
    textposition='outside',
    textfont=dict(color=FONT_COLOR, size=11),
    hovertemplate='<b>%{x}</b><br>Future Applicants: %{y}<extra></extra>'
))
layout_future = base_layout(height=420)
layout_future.update(dict(
    xaxis=dict(tickangle=-35, gridcolor=GRID_COLOR, showgrid=False, zeroline=False),
    yaxis=dict(gridcolor=GRID_COLOR, showgrid=True, zeroline=False),
))
fig_future.update_layout(layout_future)
st.plotly_chart(fig_future, use_container_width=True)

# --- Security Deposits ---
st.markdown("<div class='section-label'>DEPOSITS</div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Security Deposits by Property</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Total security deposits held per property for current and notice residents.</div>", unsafe_allow_html=True)

df_deps = df_summary_groups[
    df_summary_groups['Resident_Type'] == 'Current/Notice/Vacant Residents'
].groupby('Property_Name').agg({
    'Security_Deposit': 'sum',
    'Other_Deposits': 'sum'
}).reset_index()
df_deps = df_deps[df_deps['Security_Deposit'] > 0].sort_values('Security_Deposit', ascending=False)

fig_deps = go.Figure()
fig_deps.add_trace(go.Bar(
    name='Security Deposit',
    x=df_deps['Property_Name'],
    y=df_deps['Security_Deposit'],
    marker=dict(color=PURPLE, opacity=0.85, line=dict(width=0)),
    hovertemplate='<b>%{x}</b><br>Security Deposit: $%{y:,.0f}<extra></extra>'
))
fig_deps.add_trace(go.Bar(
    name='Other Deposits',
    x=df_deps['Property_Name'],
    y=df_deps['Other_Deposits'],
    marker=dict(color=PURPLE_LIGHT, opacity=0.85, line=dict(width=0)),
    hovertemplate='<b>%{x}</b><br>Other Deposits: $%{y:,.0f}<extra></extra>'
))
layout_deps = base_layout(height=420)
layout_deps.update(dict(
    barmode='stack',
    xaxis=dict(tickangle=-35, gridcolor=GRID_COLOR, showgrid=False, zeroline=False),
    yaxis=dict(gridcolor=GRID_COLOR, showgrid=True, zeroline=False, tickprefix='$'),
    legend=dict(font=dict(color=FONT_COLOR), bgcolor='rgba(0,0,0,0)', orientation='h', y=1.1)
))
fig_deps.update_layout(layout_deps)
st.plotly_chart(fig_deps, use_container_width=True)

# --- Lease Expirations ---
st.markdown("<div class='section-label'>LEASE EXPIRATIONS</div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Upcoming Expirations - Next 90 Days</div>", unsafe_allow_html=True)

df_leases = df_charges[df_charges['Charge_Code'] == 'RENT'].copy()
df_leases['Lease_Expiration'] = pd.to_datetime(df_leases['Lease_Expiration'], errors='coerce')
today = pd.Timestamp.today()
df_exp = df_leases[
    (df_leases['Lease_Expiration'] >= today) &
    (df_leases['Lease_Expiration'] <= today + pd.Timedelta(days=90))
].copy()
df_exp = df_exp.sort_values('Lease_Expiration')

st.markdown(f"<div class='section-sub'>{len(df_exp)} lease{'s' if len(df_exp) != 1 else ''} expiring in the next 90 days</div>", unsafe_allow_html=True)

if not df_exp.empty:
    df_exp_display = df_exp[['Name', 'Unit', 'Lease_Expiration', 'Source_Property_Name']].copy()
    df_exp_display['Lease_Expiration'] = df_exp_display['Lease_Expiration'].dt.strftime('%b %d, %Y')
    df_exp_display = df_exp_display.rename(columns={
        'Name': 'Resident', 'Lease_Expiration': 'Expires On', 'Source_Property_Name': 'Property'
    })
    df_exp_display = df_exp_display.reset_index(drop=True)
    df_exp_display.index = df_exp_display.index + 1
    st.dataframe(df_exp_display, use_container_width=True)

# --- Outstanding Balances ---
st.markdown("<div class='section-label'>OUTSTANDING BALANCES</div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Residents with a Balance Owing</div>", unsafe_allow_html=True)

df_bal = df_charges[
    (df_charges['Charge_Code'] == 'RENT') &
    (df_charges['Balance'] > 0)
].copy()
df_bal = df_bal.sort_values('Balance', ascending=False)

st.markdown(f"<div class='section-sub'>{len(df_bal)} resident{'s' if len(df_bal) != 1 else ''} with an outstanding balance</div>", unsafe_allow_html=True)

if not df_bal.empty:
    df_bal_display = df_bal[['Name', 'Unit', 'Balance', 'Source_Property_Name']].copy()
    df_bal_display['Balance'] = df_bal_display['Balance'].apply(lambda x: f'${x:,.2f}')
    df_bal_display = df_bal_display.rename(columns={
        'Name': 'Resident', 'Balance': 'Balance Owing', 'Source_Property_Name': 'Property'
    })
    df_bal_display = df_bal_display.reset_index(drop=True)
    df_bal_display.index = df_bal_display.index + 1
    st.dataframe(df_bal_display, use_container_width=True)