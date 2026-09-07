\# Validation Report – Lab 02



\## Dataset

\- File: `data/raw/prices.csv`

\- Original rows: 1010



\## Rules Checked and Results



| Rule                        | Rows that failed | Action taken                          |

|----------------------------|------------------|---------------------------------------|

| rule\_positive\_price        | 53               | Rejected (dropped)                    |

| rule\_duplicate\_rows        | 10               | Rejected (kept first occurrence)      |

| rule\_duplicate\_ids         | 16               | Rejected (kept first occurrence)      |

| rule\_valid\_date            | 26               | Rejected                              |

| rule\_missing\_market        | 175              | Imputed with value "Unknown"          |

| rule\_known\_commodity       | 0                | Normalized casing to "Maize"/"Beans"  |



\## Final Result

\- Rows after cleaning: 905

\- Rows removed: 105

\- Output file: `data/processed/prices\_clean.parquet`



\## Notes

\- All decisions were logged.

\- The original raw file was never modified.

