from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["schema"])

SCHEMA_DATA = {
    "stats": {
        "tables": 4,
        "total_columns": 53,
        "properties": 16,
        "engine": "SQLite"
    },
    "tables": [
        {
            "name": "lease_charges",
            "label": "TABLE 1 OF 4",
            "description": "The core resident-level table. Each row represents a single charge line for a resident - including rent, amenity fees, and parking. Resident identity columns are forward-filled across multiple charge rows per unit.",
            "example_query": "SELECT * FROM lease_charges WHERE Charge_Code = 'RENT' LIMIT 5;",
            "fields": [
                {"name": "Unit", "type": "TEXT", "note": "Unit number within the property"},
                {"name": "Unit_Type", "type": "TEXT", "note": "e.g. 1BR, 2BR, Studio"},
                {"name": "Sq_Ft", "type": "INTEGER", "note": "Square footage of the unit"},
                {"name": "Resident_ID", "type": "TEXT", "note": "Unique resident identifier"},
                {"name": "Name", "type": "TEXT", "note": "Resident name (e.g. Resident 42)"},
                {"name": "Market_Rent", "type": "REAL", "note": "Listed market rent for the unit"},
                {"name": "Charge_Code", "type": "TEXT", "note": "RENT, AMENITY, PARKING, PETFEEM, etc."},
                {"name": "Amount", "type": "REAL", "note": "Charge amount for this line"},
                {"name": "Resident_Deposit", "type": "REAL", "note": "Security deposit held"},
                {"name": "Other_Deposit", "type": "REAL", "note": "Additional deposits (e.g. pet)"},
                {"name": "Move_In", "type": "TEXT", "note": "Lease start date (YYYY-MM-DD)"},
                {"name": "Lease_Expiration", "type": "TEXT", "note": "Lease end date (YYYY-MM-DD)"},
                {"name": "Move_Out", "type": "TEXT", "note": "Move-out date if applicable"},
                {"name": "Balance", "type": "REAL", "note": "Outstanding balance owed"},
                {"name": "Property_ID", "type": "TEXT", "note": "Short code e.g. 126r, 144r"},
                {"name": "Source_Property_Name", "type": "TEXT", "note": "Full property name"},
                {"name": "Report_Date", "type": "TEXT", "note": "Date the report was generated"}
            ]
        },
        {
            "name": "property_summary",
            "label": "TABLE 2 OF 4",
            "description": "Property-level occupancy and leasing statistics. Each row represents one building or property group. Used for portfolio-wide metrics like occupancy rates, vacancy counts, and leasing trends. Always filter Total_Units > 0 to exclude placeholder rows.",
            "example_query": "SELECT Property_Name, Total_Units, Pct_Occ, Pct_Leased FROM property_summary WHERE Total_Units > 0 ORDER BY Pct_Occ DESC;",
            "fields": [
                {"name": "Property_ID", "type": "TEXT", "note": "Short code e.g. 126r, 153a"},
                {"name": "Property_Name", "type": "TEXT", "note": "Full display name of property"},
                {"name": "Avg_Sq_Ft", "type": "INTEGER", "note": "Average unit square footage"},
                {"name": "Avg_Rent", "type": "INTEGER", "note": "Average rent across units"},
                {"name": "Total_Units", "type": "INTEGER", "note": "Total unit count (filter > 0)"},
                {"name": "Occ_No_Notice", "type": "INTEGER", "note": "Occupied, no notice to vacate"},
                {"name": "Vacant_Rented", "type": "INTEGER", "note": "Vacant but already rented"},
                {"name": "Vacant_Unrented", "type": "INTEGER", "note": "Vacant and not yet rented"},
                {"name": "Notice_Rented", "type": "INTEGER", "note": "Notice given, replacement rented"},
                {"name": "Notice_Unrented", "type": "INTEGER", "note": "Notice given, not yet rented"},
                {"name": "Available", "type": "INTEGER", "note": "Total available units"},
                {"name": "Model", "type": "INTEGER", "note": "Model/show units"},
                {"name": "Down", "type": "INTEGER", "note": "Units taken offline"},
                {"name": "Admin", "type": "INTEGER", "note": "Admin/employee units"},
                {"name": "Pct_Occ", "type": "REAL", "note": "Occupancy % (primary metric)"},
                {"name": "Pct_Occ_NonRev", "type": "REAL", "note": "Occupancy % excl. non-revenue"},
                {"name": "Pct_Leased", "type": "REAL", "note": "Leased % including notices"},
                {"name": "Pct_Trend", "type": "REAL", "note": "Trending occupancy indicator"}
            ]
        },
        {
            "name": "summary_groups",
            "label": "TABLE 3 OF 4",
            "description": "Aggregated statistics broken down by resident type per property. Each row represents one resident category (Current/Notice/Vacant, Future Applicants, Occupied Units, etc.) for a given property. Useful for pipeline analysis, deposit totals, and occupancy breakdowns.",
            "example_query": "SELECT Property_Name, Resident_Type, Num_Units, Security_Deposit FROM summary_groups WHERE Resident_Type = 'Future Residents/Applicants' ORDER BY Num_Units DESC;",
            "fields": [
                {"name": "Resident_Type", "type": "TEXT", "note": "Current/Notice/Vacant, Future Residents, Occupied Units, etc."},
                {"name": "Sq_Ft", "type": "REAL", "note": "Total square footage for this group"},
                {"name": "Market_Rent", "type": "REAL", "note": "Total market rent for this group"},
                {"name": "Lease_Charges", "type": "REAL", "note": "Total lease charges billed"},
                {"name": "Security_Deposit", "type": "REAL", "note": "Total security deposits held"},
                {"name": "Other_Deposits", "type": "REAL", "note": "Total other deposits held"},
                {"name": "Num_Units", "type": "REAL", "note": "Number of units in this group"},
                {"name": "Pct_Unit_Occupancy", "type": "REAL", "note": "% of units occupied in this group"},
                {"name": "Pct_Sqft_Occupied", "type": "REAL", "note": "% of sq ft occupied in this group"},
                {"name": "Balance", "type": "REAL", "note": "Total outstanding balance for group"},
                {"name": "Property_ID", "type": "TEXT", "note": "Short code e.g. 126r, 144r"},
                {"name": "Property_Name", "type": "TEXT", "note": "Full display name of property"},
                {"name": "Report_Date", "type": "TEXT", "note": "Date the report was generated"}
            ]
        },
        {
            "name": "charge_code_summary",
            "label": "TABLE 4 OF 4",
            "description": "Property-level revenue breakdown by charge code. Each row represents the total amount collected for one charge type at one property - including RENT, PARKING, AMENITY, PETFEEM, TRASH, STORAGE, and many more. Useful for revenue analysis across charge types.",
            "example_query": "SELECT Charge_Code, SUM(Amount) as Total_Revenue FROM charge_code_summary GROUP BY Charge_Code ORDER BY Total_Revenue DESC;",
            "fields": [
                {"name": "Charge_Code", "type": "TEXT", "note": "e.g. RENT, PARKING, PETFEEM, TRASH, STORAGE"},
                {"name": "Amount", "type": "REAL", "note": "Total revenue for this charge code at this property"},
                {"name": "Property_ID", "type": "TEXT", "note": "Short code e.g. 126r, 144r"},
                {"name": "Property_Name", "type": "TEXT", "note": "Full display name of property"},
                {"name": "Report_Date", "type": "TEXT", "note": "Date the report was generated"}
            ]
        }
    ]
}


@router.get("/schema")
async def get_schema():
    return SCHEMA_DATA
