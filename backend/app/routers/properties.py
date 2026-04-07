from fastapi import APIRouter
from app.database import query_df

router = APIRouter(prefix="/api", tags=["properties"])


@router.get("/properties/overview")
async def get_overview():
    conn_queries = {
        "total_props": "SELECT COUNT(DISTINCT Property_Name) as c FROM property_summary WHERE Total_Units > 0",
        "total_units": "SELECT SUM(Total_Units) as c FROM property_summary WHERE Total_Units > 0",
        "avg_occ": "SELECT ROUND(AVG(Pct_Occ), 2) as c FROM property_summary WHERE Pct_Occ > 0 AND Total_Units > 0",
        "total_vacant": "SELECT SUM(Vacant_Rented + Vacant_Unrented) as c FROM property_summary WHERE Total_Units > 0",
        "total_future": "SELECT SUM(Num_Units) as c FROM summary_groups WHERE Resident_Type = 'Future Residents/Applicants'",
        "total_deposits": "SELECT ROUND(SUM(Security_Deposit), 2) as c FROM summary_groups WHERE Resident_Type = 'Current/Notice/Vacant Residents'"
    }

    metrics = {}
    for key, sql in conn_queries.items():
        val = query_df(sql).iloc[0, 0]
        metrics[key] = float(val) if val is not None else 0

    # All properties table
    df = query_df("""
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
    """)
    properties_table = df.to_dict(orient='records')

    # Revenue by charge code
    df_charges = query_df("""
        SELECT
            Charge_Code,
            ROUND(SUM(Amount), 2) as Total_Revenue,
            COUNT(DISTINCT Property_ID) as Properties
        FROM charge_code_summary
        GROUP BY Charge_Code
        ORDER BY Total_Revenue DESC
    """)
    charge_codes_table = df_charges.to_dict(orient='records')

    # Security deposits by property
    df_deposits = query_df("""
        SELECT
            Property_Name,
            ROUND(SUM(Security_Deposit), 2) as Total_Security_Deposit,
            ROUND(SUM(Other_Deposits), 2) as Total_Other_Deposits,
            ROUND(SUM(Security_Deposit + Other_Deposits), 2) as Total_Deposits
        FROM summary_groups
        WHERE Resident_Type = 'Current/Notice/Vacant Residents'
        GROUP BY Property_Name
        ORDER BY Total_Security_Deposit DESC
    """)
    deposits_table = df_deposits.to_dict(orient='records')

    return {
        "metrics": metrics,
        "properties_table": properties_table,
        "charge_codes_table": charge_codes_table,
        "deposits_table": deposits_table
    }
