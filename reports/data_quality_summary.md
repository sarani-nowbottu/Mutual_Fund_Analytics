# Data Quality & Ingestion Summary Report

## Overview
- Total raw datasets detected: 6
- Ingestion directory: `data/raw/`

## Dataset Profiles

| Dataset Name | Rows | Columns | Missing Values | Duplicate Rows | Notes / Anomalies |
|---|---|---|---|---|---|
| `live_nav_125497` | 3182 | 3 | 0 | 0 | Date stored as text/string (non-datetime format) |
| `nav_Axis_Bluechip` | 3655 | 3 | 0 | 0 | Date stored as text/string (non-datetime format) |
| `nav_ICICI_Bluechip` | 3398 | 3 | 0 | 0 | Date stored as text/string (non-datetime format) |
| `nav_Kotak_Bluechip` | 3392 | 3 | 0 | 0 | Date stored as text/string (non-datetime format) |
| `nav_Nippon_Large_Cap` | 3389 | 3 | 0 | 0 | Date stored as text/string (non-datetime format) |
| `nav_SBI_Bluechip` | 3326 | 3 | 0 | 0 | Date stored as text/string (non-datetime format) |

## Fund Master Exploration
- `fund_master.csv` was not detected in `data/raw/`. Place the file into `data/raw/` to view unique fund houses, categories, and risk grades.

## AMFI Code Validation
- Cross-validation pending presence of both `fund_master.csv` and `nav_history.csv`.
