# %%
import pandas as pd
data = pd.read_csv('lightcast_data.csv')

# %%
company_series = (
    data["COMPANY_NAME"]
    .dropna()
    .astype(str)
    .str.strip()
)

company_series = company_series[company_series.ne("") & company_series.ne("nan")]

# 1) Show total unique companies
unique_companies = company_series.unique()
print("Total unique COMPANY_NAME values:", len(unique_companies))

# 2) Show the top 50 companies by number of postings (recommended for picking 3)
top_companies = company_series.value_counts().head(50)
print("\nTop 50 companies by postings:\n")
print(top_companies)

# 3) (Optional) print ALL unique company names (can be very long!)
# for name in sorted(unique_companies):
#     print(name)

# %%
# 2) Typecast datetime columns
date_cols = ["POSTED", "EXPIRED", "LAST_UPDATED_DATE"]
for col in date_cols:
    if col in data.columns:
        data[col] = pd.to_datetime(data[col], errors="coerce")

# 3) Typecast numeric columns
num_cols = ["SALARY_FROM", "SALARY_TO", "MIN_YEARS_EXPERIENCE"]
for col in num_cols:
    if col in data.columns:
        # clean symbols like $, commas, text; keep digits/dot/minus
        cleaned = (
            data[col]
            .astype(str)
            .str.replace(r"[^0-9.\-]", "", regex=True)
            .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
        )
        data[col] = pd.to_numeric(cleaned, errors="coerce")

# 4) Fill missing values (NO inplace on column slice -> avoids FutureWarning)
fill_map = {
    "SALARY_FROM": 0,
    "SALARY_TO": 0,
    "MIN_YEARS_EXPERIENCE": 0
}
existing_fill_map = {k: v for k, v in fill_map.items() if k in data.columns}
data = data.fillna(existing_fill_map)


# %%
import os 
# Make sure the output folder exists
os.makedirs("_output", exist_ok=True)

# Save cleaned data
data.to_csv("_output/lightcast_cleaned.csv", index=False)

print("Saved to: _output/lightcast_cleaned.csv")


# %%
import matplotlib.pyplot as plt

# 1) Group by STATE_NAME and count jobs
state_counts = (
    data.groupby("STATE_NAME")
        .size()
        .sort_values(ascending=False)
)

# (Optional) limit to top N states so the chart is readable
top_n = 20
state_counts_plot = state_counts.head(top_n)

# 2) Plot using Matplotlib (no fixed colors)
plt.figure(figsize=(12, 6))
plt.bar(state_counts_plot.index.astype(str), state_counts_plot.values)
plt.xticks(rotation=75, ha="right")
plt.xlabel("State")
plt.ylabel("Number of Jobs")
plt.title(f"Job Count by State (Top {top_n})")
plt.tight_layout()
plt.savefig("_output/q1_job_count_by_state.png", dpi=300, bbox_inches="tight")
plt.show()

# %%

industry = "Retail Trade" 

# 1) Filter for the industry (handles extra spaces / missing)
industry_data = data[data["NAICS2_NAME"].astype(str).str.strip().eq(industry)].copy()

# 2) Group by state and count jobs
state_counts = (
    industry_data.groupby("STATE_NAME")
        .size()
        .sort_values(ascending=False)
)

# (Optional) limit to top N states for readability
top_n = 20
state_counts_plot = state_counts.head(top_n)

# 3) Plot bar chart
plt.figure(figsize=(12, 6))
plt.bar(state_counts_plot.index.astype(str), state_counts_plot.values)
plt.xticks(rotation=75, ha="right")
plt.xlabel("State")
plt.ylabel("Number of Jobs")
plt.title(f"Job Count by State — {industry} (Top {top_n})")
plt.tight_layout()
plt.savefig("_output/q2_job_count_by_state_retail_trade.png", dpi=300, bbox_inches="tight")
plt.show()

