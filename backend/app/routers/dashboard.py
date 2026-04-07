from fastapi import APIRouter
import pandas as pd
from app.database import query_df

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.get("/dashboard")
async def get_dashboard():
    df_summary = query_df("SELECT * FROM property_summary WHERE Total_Units > 0")
    df_charges = query_df("SELECT * FROM lease_charges")
    df_summary_groups = query_df("SELECT * FROM summary_groups")
    df_charge_codes = query_df("SELECT * FROM charge_code_summary")

    avg_occ = query_df(
        "SELECT ROUND(AVG(Pct_Occ), 2) as v FROM property_summary WHERE Pct_Occ > 0 AND Total_Units > 0"
    ).iloc[0, 0]

    # Aggregate by property
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

    # KPIs
    total_units = int(df_props['Total_Units'].sum())
    total_vacant = int((df_props['Vacant_Rented'] + df_props['Vacant_Unrented']).sum())
    total_residents = int(df_charges[
        (df_charges['Charge_Code'] == 'RENT') &
        (df_charges['Move_Out'].isna() | (df_charges['Move_Out'] == ''))
    ]['Resident_ID'].nunique())

    # Occupancy chart data
    df_occ = df_props.sort_values('Pct_Occ', ascending=True)
    occupancy_data = [
        {"property": row['Property_Name'], "occupancy": round(row['Pct_Occ'], 1)}
        for _, row in df_occ.iterrows()
    ]

    # Vacancy chart data
    df_vac = df_props.copy()
    df_vac['Total_Vacant'] = df_vac['Vacant_Rented'] + df_vac['Vacant_Unrented']
    df_vac = df_vac[df_vac['Total_Vacant'] > 0].sort_values('Total_Vacant', ascending=False)
    vacancy_bar_data = [
        {
            "property": row['Property_Name'],
            "vacant_rented": int(row['Vacant_Rented']),
            "vacant_unrented": int(row['Vacant_Unrented'])
        }
        for _, row in df_vac.iterrows()
    ]

    # Vacancy pie data
    occ_total = int(df_props['Occ_No_Notice'].sum())
    vac_rented = int(df_props['Vacant_Rented'].sum())
    vac_unrented = int(df_props['Vacant_Unrented'].sum())
    notice = int(df_summary['Notice_Rented'].sum() + df_summary['Notice_Unrented'].sum())
    vacancy_pie_data = [
        {"name": "Occupied", "value": occ_total},
        {"name": "Vacant (Rented)", "value": vac_rented},
        {"name": "Vacant (Unrented)", "value": vac_unrented},
        {"name": "Notice Given", "value": notice}
    ]

    # Rent chart data
    df_rent = df_props.sort_values('Avg_Rent', ascending=False)
    rent_data = [
        {"property": row['Property_Name'], "avg_rent": round(row['Avg_Rent'], 0)}
        for _, row in df_rent.iterrows()
    ]

    # Revenue by charge code
    df_cc = df_charge_codes.groupby('Charge_Code')['Amount'].sum().reset_index()
    df_cc_other = df_cc[df_cc['Charge_Code'] != 'RENT'].sort_values('Amount', ascending=False)
    df_cc_positive = df_cc_other[df_cc_other['Amount'] > 0].sort_values('Amount', ascending=False)
    df_cc_negative = df_cc_other[df_cc_other['Amount'] < 0].sort_values('Amount', ascending=False)
    total_rent = float(df_cc[df_cc['Charge_Code'] == 'RENT']['Amount'].sum())
    total_other_positive = float(df_cc_positive['Amount'].sum())
    total_concessions = float(df_cc_negative['Amount'].sum())

    revenue_positive = [
        {"charge_code": row['Charge_Code'], "amount": round(row['Amount'], 2)}
        for _, row in df_cc_positive.iterrows()
    ]
    revenue_negative = [
        {"charge_code": row['Charge_Code'], "amount": round(row['Amount'], 2)}
        for _, row in df_cc_negative.iterrows()
    ]

    # Future applicants
    df_future = df_summary_groups[
        df_summary_groups['Resident_Type'] == 'Future Residents/Applicants'
    ].groupby('Property_Name')['Num_Units'].sum().reset_index()
    df_future = df_future[df_future['Num_Units'] > 0].sort_values('Num_Units', ascending=False)
    pipeline_data = [
        {"property": row['Property_Name'], "applicants": int(row['Num_Units'])}
        for _, row in df_future.iterrows()
    ]

    # Deposits
    df_deps = df_summary_groups[
        df_summary_groups['Resident_Type'] == 'Current/Notice/Vacant Residents'
    ].groupby('Property_Name').agg({
        'Security_Deposit': 'sum',
        'Other_Deposits': 'sum'
    }).reset_index()
    df_deps = df_deps[df_deps['Security_Deposit'] > 0].sort_values('Security_Deposit', ascending=False)
    deposits_data = [
        {
            "property": row['Property_Name'],
            "security_deposit": round(row['Security_Deposit'], 2),
            "other_deposits": round(row['Other_Deposits'], 2)
        }
        for _, row in df_deps.iterrows()
    ]

    # Lease expirations (next 90 days)
    df_leases = df_charges[df_charges['Charge_Code'] == 'RENT'].copy()
    df_leases['Lease_Expiration'] = pd.to_datetime(df_leases['Lease_Expiration'], errors='coerce')
    today = pd.Timestamp.today()
    df_exp = df_leases[
        (df_leases['Lease_Expiration'] >= today) &
        (df_leases['Lease_Expiration'] <= today + pd.Timedelta(days=90))
    ].sort_values('Lease_Expiration')
    lease_expirations = [
        {
            "name": row['Name'],
            "unit": row['Unit'],
            "expiration": row['Lease_Expiration'].strftime('%b %d, %Y'),
            "property": row['Source_Property_Name']
        }
        for _, row in df_exp.iterrows()
    ]

    # Outstanding balances
    df_bal = df_charges[
        (df_charges['Charge_Code'] == 'RENT') &
        (df_charges['Balance'] > 0)
    ].sort_values('Balance', ascending=False)
    outstanding_balances = [
        {
            "name": row['Name'],
            "unit": row['Unit'],
            "balance": round(row['Balance'], 2),
            "property": row['Source_Property_Name']
        }
        for _, row in df_bal.iterrows()
    ]

    return {
        "kpis": {
            "total_units": total_units,
            "avg_occupancy": float(avg_occ),
            "total_vacant": total_vacant,
            "total_residents": total_residents
        },
        "occupancy": occupancy_data,
        "vacancy_bar": vacancy_bar_data,
        "vacancy_pie": vacancy_pie_data,
        "rent": rent_data,
        "revenue": {
            "total_rent": total_rent,
            "total_other": total_other_positive,
            "total_concessions": total_concessions,
            "positive": revenue_positive,
            "negative": revenue_negative
        },
        "pipeline": pipeline_data,
        "deposits": deposits_data,
        "lease_expirations": lease_expirations,
        "outstanding_balances": outstanding_balances
    }
