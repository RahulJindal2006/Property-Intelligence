import pandas as pd
import os
import glob
import sqlite3
import re

FOLDER_1 = 'Rent_Roll_With_Lease_Charges'
FOLDER_2 = 'Unit_Availability'

def extract_clean_id(address_string):
    """Extracts the ID from 'Name (ID)' or 'Name ID'."""
    if pd.isna(address_string):
        return "Unknown"
    text = str(address_string).strip()
    match = re.search(r'\((.*?)\)', text)
    if match:
        return match.group(1).strip()
    return text.split()[-1].strip()

def clean_rent_roll(file_path):
    df_raw = pd.read_excel(file_path, header=None, engine='openpyxl')

    # 1. Metadata
    raw_address = df_raw.iloc[1, 0]
    as_of_date = str(df_raw.iloc[2, 0]).replace('As Of = ', '')
    prop_id = extract_clean_id(raw_address)

    # 2. Extract Table (Rows 5 to 'Summary Groups')
    summary_idx = df_raw[df_raw.iloc[:, 0] == "Summary Groups"].index
    end_row = summary_idx[0] if len(summary_idx) > 0 else len(df_raw)
    df = df_raw.iloc[4:end_row].copy()

    # 3. Name Columns
    df.columns = [
        'Unit', 'Unit_Type', 'Sq_Ft', 'Resident_ID', 'Name',
        'Market_Rent', 'Charge_Code', 'Amount', 'Resident_Deposit',
        'Other_Deposit', 'Move_In', 'Lease_Expiration', 'Move_Out', 'Balance'
    ]

    # 4. Forward Fill
    identity_cols = ['Unit', 'Unit_Type', 'Sq_Ft', 'Resident_ID', 'Name']
    df[identity_cols] = df[identity_cols].ffill()

    # 5. Filter for actual data rows
    df = df.dropna(subset=['Charge_Code'])
    df = df[df['Charge_Code'].astype(str).str.upper() != 'TOTAL']

    # 6. Junk Removal
    headers_to_skip = [
        'Unit', 'Unit Type',
        'Current/Notice/Vacant Residents',
        'Future Residents/Applicants'
    ]
    df = df[~df['Unit'].isin(headers_to_skip)]

    # 7. Polish Numbers
    num_cols = ['Sq_Ft', 'Market_Rent', 'Amount', 'Balance']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # 8. Add Foreign Keys
    prop_name_str = str(raw_address).strip()
    name_map = {
        'Fifty-Five Riverwalk Place': '55 Riverwalk Place'
    }
    for old, new in name_map.items():
        if old.lower() in prop_name_str.lower():
            prop_name_str = new

    df['Property_ID'] = prop_id
    df['Source_Property_Name'] = prop_name_str
    df['Report_Date'] = as_of_date

    print(f"✅ Processed {prop_id}: {len(df)} charge rows found.")
    return df

def extract_summary_groups(file_path):
    """Extracts the Summary Groups and Charge Code sections from a rent roll Excel file."""
    df_raw = pd.read_excel(file_path, header=None, engine='openpyxl')

    raw_address = df_raw.iloc[1, 0]
    as_of_date = str(df_raw.iloc[2, 0]).replace('As Of = ', '')
    prop_id = extract_clean_id(raw_address)
    prop_name = str(raw_address).strip()
    # Remove the ID in parentheses e.g. "The Halden (126r)" -> "The Halden"
    prop_name = re.sub(r'\s*\(.*?\)\s*$', '', prop_name).strip()

    if 'fifty-five' in prop_name.lower():
        prop_name = '55 Riverwalk Place'

    # Find Summary Groups start
    summary_idx = df_raw[df_raw.iloc[:, 0] == "Summary Groups"].index
    if len(summary_idx) == 0:
        return None, None

    start_row = summary_idx[0] + 2  # skip header and subheader rows

    # Find charge code summary start
    charge_idx = df_raw[df_raw.iloc[:, 0].astype(str).str.strip() == "Summary of Charges by Charge Code"].index
    if len(charge_idx) == 0:
        end_row = start_row + 10
        charge_start = None
    else:
        end_row = charge_idx[0]
        charge_start = charge_idx[0] + 3  # skip header, subheader, and column label rows

    # --- Extract Summary Groups table ---
    df_summary = df_raw.iloc[start_row:end_row, [0, 5, 6, 7, 8, 9, 10, 11, 12, 13]].copy()
    df_summary.columns = [
        'Resident_Type', 'Sq_Ft', 'Market_Rent', 'Lease_Charges',
        'Security_Deposit', 'Other_Deposits', 'Num_Units',
        'Pct_Unit_Occupancy', 'Pct_Sqft_Occupied', 'Balance'
    ]
    df_summary = df_summary.dropna(subset=['Resident_Type'])
    df_summary['Resident_Type'] = df_summary['Resident_Type'].astype(str).str.strip()
    valid_types = [
        'Current/Notice/Vacant Residents',
        'Future Residents/Applicants',
        'Occupied Units',
        'Total Non Rev Units',
        'Total Vacant Units'
    ]
    df_summary = df_summary[df_summary['Resident_Type'].isin(valid_types)]

    # Add metadata
    df_summary['Property_ID'] = prop_id
    df_summary['Property_Name'] = prop_name
    df_summary['Report_Date'] = as_of_date

    # Polish numbers
    num_cols = ['Sq_Ft', 'Market_Rent', 'Lease_Charges', 'Security_Deposit',
                'Other_Deposits', 'Num_Units', 'Pct_Unit_Occupancy',
                'Pct_Sqft_Occupied', 'Balance']
    for col in num_cols:
        df_summary[col] = pd.to_numeric(
            df_summary[col].astype(str).str.replace(',', ''), errors='coerce'
        ).fillna(0)

    # --- Extract Charge Code Summary ---
    df_charges = None
    if charge_start is not None:
        total_idx = df_raw.iloc[charge_start:][df_raw.iloc[charge_start:, 0] == 'Total'].index
        charge_end = total_idx[0] if len(total_idx) > 0 else charge_start + 20

        df_charges = df_raw.iloc[charge_start:charge_end, [0, 3]].copy()
        df_charges.columns = ['Charge_Code', 'Amount']
        df_charges = df_charges.dropna(subset=['Charge_Code'])
        df_charges = df_charges[~df_charges['Charge_Code'].isin(['Charge Code', 'Total'])]
        df_charges['Amount'] = pd.to_numeric(df_charges['Amount'], errors='coerce').fillna(0)

        # Add metadata
        df_charges['Property_ID'] = prop_id
        df_charges['Property_Name'] = prop_name
        df_charges['Report_Date'] = as_of_date

    print(f"✅ Summary Groups extracted for {prop_id}")
    return df_summary, df_charges

def clean_unit_availability(file_path):
    df_raw = pd.read_excel(file_path, header=None, engine='openpyxl')
    as_of_date = str(df_raw.iloc[2, 0]).replace('As Of = ', '')

    df = df_raw.iloc[5:].copy()
    df.columns = [
        'Property_ID', 'Property_Name', 'Avg_Sq_Ft', 'Avg_Rent', 'Total_Units',
        'Occ_No_Notice', 'Vacant_Rented', 'Vacant_Unrented',
        'Notice_Rented', 'Notice_Unrented', 'Available', 'Model',
        'Down', 'Admin', 'Pct_Occ', 'Pct_Occ_NonRev', 'Pct_Leased', 'Pct_Trend'
    ]

    df = df.dropna(subset=['Property_ID'])
    df = df[df['Property_ID'] != 'Property']
    df['Property_ID'] = df['Property_ID'].astype(str).str.strip()

    # Standardize property names
    df['Property_Name'] = df['Property_Name'].astype(str).str.replace(
        'Fifty-Five Riverwalk Pl...', '55 Riverwalk Place', regex=False
    )

    return df

def load_to_database():
    conn = sqlite3.connect('PropertyManagement.db')

    if os.path.exists('master_rent_roll.csv'):
        df = pd.read_csv('master_rent_roll.csv')
        date_cols = ['Move_In', 'Lease_Expiration', 'Move_Out']
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')
        df.to_sql('lease_charges', conn, if_exists='replace', index=False)
        print("✅ lease_charges loaded!")

    if os.path.exists('master_availability.csv'):
        pd.read_csv('master_availability.csv').to_sql('property_summary', conn, if_exists='replace', index=False)
        print("✅ property_summary loaded!")

    if os.path.exists('master_summary_groups.csv'):
        pd.read_csv('master_summary_groups.csv').to_sql('summary_groups', conn, if_exists='replace', index=False)
        print("✅ summary_groups loaded!")

    if os.path.exists('master_charge_summary.csv'):
        pd.read_csv('master_charge_summary.csv').to_sql('charge_code_summary', conn, if_exists='replace', index=False)
        print("✅ charge_code_summary loaded!")

    conn.close()
    print("✨ Database 'PropertyManagement.db' refreshed!")

if __name__ == "__main__":
    rr_files = glob.glob(os.path.join(FOLDER_1, "*.xlsx"))
    av_files = glob.glob(os.path.join(FOLDER_2, "*.xlsx"))

    if rr_files:
        all_rent_rolls = []
        all_summary_groups = []
        all_charge_summaries = []

        for f in rr_files:
            try:
                rr = clean_rent_roll(f)
                all_rent_rolls.append(rr)

                sg, cs = extract_summary_groups(f)
                if sg is not None:
                    all_summary_groups.append(sg)
                if cs is not None:
                    all_charge_summaries.append(cs)
            except Exception as e:
                print(f"⚠️ Skipping {f}: {e}")

        if all_rent_rolls:
            pd.concat(all_rent_rolls).to_csv('master_rent_roll.csv', index=False)
            print(f"✅ master_rent_roll.csv saved!")

        if all_summary_groups:
            pd.concat(all_summary_groups).to_csv('master_summary_groups.csv', index=False)
            print(f"✅ master_summary_groups.csv saved!")

        if all_charge_summaries:
            pd.concat(all_charge_summaries).to_csv('master_charge_summary.csv', index=False)
            print(f"✅ master_charge_summary.csv saved!")

    if av_files:
        try:
            pd.concat([clean_unit_availability(f) for f in av_files]).to_csv('master_availability.csv', index=False)
            print(f"✅ master_availability.csv saved!")
        except Exception as e:
            print(f"⚠️ Skipping availability file: {e}")

    load_to_database()