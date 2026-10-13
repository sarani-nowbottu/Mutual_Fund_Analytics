# Data Quality & Ingestion Summary Report

## Overview
- Total raw datasets detected: 16
- Ingestion directory: `data/raw/`

## Dataset Profiles

| Dataset Name | Rows | Columns | Missing Values | Duplicate Rows | Notes / Anomalies |
|---|---|---|---|---|---|
| `aum_by_fund_house` | 90 | 5 | 0 | 0 | `date` stored as text/string |
| `benchmark_indices` | 8050 | 3 | 0 | 0 | `date` stored as text/string |
| `category_inflows` | 144 | 3 | 0 | 0 | Clean (No anomalies detected) |
| `fund_master` | 40 | 15 | 0 | 0 | `launch_date` stored as text/string |
| `industry_folio_count` | 21 | 6 | 0 | 0 | Clean (No anomalies detected) |
| `investor_transactions` | 32778 | 13 | 0 | 0 | `transaction_date` stored as text/string |
| `live_nav_125497` | 3182 | 3 | 0 | 0 | `date` stored as text/string |
| `monthly_sip_inflows` | 48 | 6 | 12 | 0 | 12 missing values |
| `nav_Axis_Bluechip` | 3655 | 3 | 0 | 0 | `date` stored as text/string |
| `nav_ICICI_Bluechip` | 3398 | 3 | 0 | 0 | `date` stored as text/string |
| `nav_Kotak_Bluechip` | 3392 | 3 | 0 | 0 | `date` stored as text/string |
| `nav_Nippon_Large_Cap` | 3389 | 3 | 0 | 0 | `date` stored as text/string |
| `nav_SBI_Bluechip` | 3326 | 3 | 0 | 0 | `date` stored as text/string |
| `nav_history` | 46000 | 3 | 0 | 0 | `date` stored as text/string |
| `portfolio_holdings` | 322 | 8 | 0 | 0 | Clean (No anomalies detected) |
| `scheme_performance` | 40 | 19 | 0 | 0 | Clean (No anomalies detected) |

## Fund Master Exploration
- Target Dataset: `fund_master` (40 schemes, 15 columns)
- Columns: `amfi_code`, `fund_house`, `scheme_name`, `category`, `sub_category`, `plan`, `launch_date`, `benchmark`, `expense_ratio_pct`, `exit_load_pct`, `min_sip_amount`, `min_lumpsum_amount`, `fund_manager`, `risk_category`, `sebi_category_code`

- **fund_house** (10 unique): SBI Mutual Fund, HDFC Mutual Fund, ICICI Prudential MF, Nippon India MF, Kotak Mahindra MF, Axis Mutual Fund, Aditya Birla Sun Life MF, UTI Mutual Fund, Mirae Asset MF, DSP Mutual Fund
- **category** (2 unique): Equity, Debt
- **sub_category** (12 unique): Large Cap, Small Cap, Gilt, Mid Cap, Short Duration, Value, Liquid, Index/ETF, Flexi Cap, Index, Large & Mid Cap, ELSS
- **risk_category** (5 unique): Moderate, Very High, Low, High, Moderately High

### AMFI Scheme Code Structure
- **AMFI Code**: Unique 6-digit numeric identifier assigned by the Association of Mutual Funds in India (e.g., 119551, 120503).
- Total unique schemes registered: **40**

## AMFI Code Validation
- Fund Master Schemes: **40** (`amfi_code`)
- NAV History Schemes: **40** (`amfi_code`)
- Schemes missing from NAV history: **0**
- Result: All codes from fund_master exist in nav_history (100% match).

## Data Quality Summary
- **Files Ingested**: Successfully profiled all 10 core CSV datasets plus 6 live API NAV datasets in `data/raw/`.
- **Completeness**: AMFI codes in `fund_master` (40 schemes) have 100% coverage in `nav_history` with 0 missing schemes.
- **Data Types**: Date columns across raw CSV files (`date`, `launch_date`, `transaction_date`) are currently stored as string objects and should be converted to datetime objects during preprocessing.
- **Integrity**: No corrupted records or unparseable rows detected across datasets.
