import pandas as pd
import glob
import os

print("==================================================")
print("             DATA INGESTION PIPELINE              ")
print("==================================================")

datasets = {}
csv_files = glob.glob("data/raw/*.csv")

if not csv_files:
    print("No CSV files found in data/raw/. Please fetch live NAVs or add raw datasets.")
else:
    print(f"Found {len(csv_files)} CSV files in data/raw/.\n")

report_lines = [
    "# Data Quality & Ingestion Summary Report",
    "",
    "## Overview",
    f"- Total raw datasets detected: {len(csv_files)}",
    f"- Ingestion directory: `data/raw/`",
    "",
    "## Dataset Profiles",
    "",
    "| Dataset Name | Rows | Columns | Missing Values | Duplicate Rows | Notes / Anomalies |",
    "|---|---|---|---|---|---|"
]

for path in csv_files:
    name = os.path.basename(path).replace(".csv", "")
    try:
        df = pd.read_csv(path)
        datasets[name] = df
        
        print(f"\n===== {name} =====")
        print("Shape:", df.shape)
        print("Data Types:\n", df.dtypes)
        print("\nHead:\n", df.head(3))
        
        missing_count = df.isnull().sum().sum()
        dup_count = df.duplicated().sum()
        print("\nMissing values per column:\n", df.isnull().sum())
        print(f"Duplicate rows: {dup_count}")
        
        # Anomaly checks
        anomalies = []
        if missing_count > 0:
            anomalies.append(f"{missing_count} missing values")
        if dup_count > 0:
            anomalies.append(f"{dup_count} duplicate rows")
        if "date" in df.columns:
            # Check date format (flags string/text representations of dates)
            if not pd.api.types.is_datetime64_any_dtype(df["date"]):
                anomalies.append("Date stored as text/string (non-datetime format)")
        
        anomaly_str = "; ".join(anomalies) if anomalies else "Clean (No anomalies detected)"
        report_lines.append(f"| `{name}` | {df.shape[0]} | {df.shape[1]} | {missing_count} | {dup_count} | {anomaly_str} |")
        
    except Exception as e:
        print(f"Error loading {path}: {e}")
        report_lines.append(f"| `{name}` | Error | Error | - | - | Load failed: {e} |")

# Step 6: Explore Fund Master (if present)
print("\n==================================================")
print("            STEP 6: FUND MASTER EXPLORATION        ")
print("==================================================")

# Search for fund master key (exact or case-insensitive)
fund_master_key = next((k for k in datasets if "fund_master" in k.lower() or "master" in k.lower()), None)

if fund_master_key:
    fm = datasets[fund_master_key]
    print(f"Discovered Fund Master dataset: '{fund_master_key}'")
    print("Columns:", fm.columns.tolist())
    
    report_lines.extend([
        "",
        "## Fund Master Exploration",
        f"- Target Dataset: `{fund_master_key}`",
        f"- Columns: {', '.join([f'`{c}`' for c in fm.columns])}"
    ])
    
    for col in ["fund_house", "category", "sub_category", "risk_grade"]:
        if col in fm.columns:
            uniques = fm[col].dropna().unique()
            print(f"\nUnique values for '{col}' ({len(uniques)} unique):")
            print(uniques[:15])
            report_lines.append(f"- **{col}** ({len(uniques)} unique): {', '.join(map(str, uniques[:10]))}{' ...' if len(uniques) > 10 else ''}")
        else:
            print(f"Column '{col}' not found in fund master.")
else:
    print("Fund master dataset ('fund_master.csv') not yet present in data/raw/.")
    report_lines.extend([
        "",
        "## Fund Master Exploration",
        "- `fund_master.csv` was not detected in `data/raw/`. Place the file into `data/raw/` to view unique fund houses, categories, and risk grades."
    ])

# Step 7: Validate AMFI Codes (if fund_master and nav_history present)
print("\n==================================================")
print("            STEP 7: AMFI CODE VALIDATION          ")
print("==================================================")

nav_history_key = next((k for k in datasets if "nav_history" in k.lower() or "nav" in k.lower() and k != fund_master_key), None)

if fund_master_key and nav_history_key:
    fm = datasets[fund_master_key]
    nav = datasets[nav_history_key]
    
    # Identify code column in fm
    fm_code_col = next((c for c in fm.columns if "code" in c.lower() or "amfi" in c.lower() or "scheme" in c.lower()), None)
    nav_code_col = next((c for c in nav.columns if "code" in c.lower() or "amfi" in c.lower() or "scheme" in c.lower()), None)
    
    if fm_code_col and nav_code_col:
        fm_codes = set(fm[fm_code_col].dropna().astype(str))
        nav_codes = set(nav[nav_code_col].dropna().astype(str))
        missing = fm_codes - nav_codes
        print(f"Comparing '{fund_master_key}.{fm_code_col}' with '{nav_history_key}.{nav_code_col}'")
        print("Total codes in fund master:", len(fm_codes))
        print("Total codes in NAV history:", len(nav_codes))
        print("Codes in fund master missing from NAV history count:", len(missing))
        if missing:
            print("Missing sample:", list(missing)[:10])
            
        report_lines.extend([
            "",
            "## AMFI Code Validation",
            f"- Fund Master Code Column: `{fm_code_col}` ({len(fm_codes)} unique)",
            f"- NAV Dataset Code Column: `{nav_code_col}` ({len(nav_codes)} unique)",
            f"- Codes missing from NAV dataset: **{len(missing)}**",
            f"- Missing sample: `{', '.join(list(missing)[:10])}`" if missing else "- All AMFI codes from fund master are present in NAV dataset."
        ])
    else:
        print(f"Could not automatically identify AMFI code columns (fm: {fm_code_col}, nav: {nav_code_col})")
else:
    print("AMFI code cross-validation requires both fund_master and nav_history datasets.")
    report_lines.extend([
        "",
        "## AMFI Code Validation",
        "- Cross-validation pending presence of both `fund_master.csv` and `nav_history.csv`."
    ])

# Save reports/data_quality_summary.md
os.makedirs("reports", exist_ok=True)
report_path = "reports/data_quality_summary.md"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines) + "\n")

print(f"\nData quality summary saved to: {report_path}")
print("Data ingestion script completed successfully.")
