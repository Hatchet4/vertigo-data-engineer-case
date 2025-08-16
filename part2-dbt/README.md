# Part 2 — dbt on BigQuery

# Vertigo Games – Part 2 Data Pipeline & Analytics

# 📌 Overview
This repository contains the **Part 2 solution** for the Vertigo Games Data Engineer case.  
The objective was to design and implement a modern data pipeline that ingests raw user metrics, transforms them into analytical tables, and enables visualization.

---

# Approach

1. Data Ingestion
- Several CSV/GZIP files containing **daily user metrics** were imported into **BigQuery**.
- A single raw table was created:
  - **`raw.user_daily_metrics`**
- The table was **partitioned** by `event_date` and **clustered** by `(country, platform)` for cost efficiency and faster queries.

2. Transformations with dbt
- dbt was used to build a modular, testable transformation layer.
- Core model:
  - **`daily_metrics.sql`** (incremental model)
    - Aggregates raw user-level data into daily country/platform KPIs.
    - Uses `config(materialized='incremental', unique_key='event_date_country_platform')` for efficient incremental builds.
    - Ensures robustness with `SAFE_DIVIDE` for ratio calculations.
- Tests:
  - Non-null constraints on key fields (`event_date`, `country`, `platform`).
  - Uniqueness test on `event_date_country_platform`.

3. Key Metrics
The model produces the following metrics:
- **DAU** – distinct active users per day
- **ARPDAU** – average revenue per daily active user
- **Revenue split** – `total_iap_revenue` and `total_ad_revenue`
- **Engagement** – matches started per DAU
- **Performance** – win ratio, defeat ratio
- **Reliability** – server error per DAU

4. Visualization
- Python + Plotly was used to build prototype visualizations (since Looker Studio wasn’t an option).
- Example plots:
  - DAU trend over time by platform
  - ARPDAU by country
  - Revenue split (ads vs IAP)
  - Win ratio vs defeat ratio heatmap

---

# Assumptions
- **Late-arriving data**: To capture backfills, incremental models include a **2-day overlap window**:
  ```sql
  WHERE event_date >= (
    SELECT COALESCE(DATE_SUB(MAX(event_date), INTERVAL 2 DAY), DATE('1970-01-01'))
    FROM {{ this }}
  )



## 1) Prereqs
- BigQuery dataset `raw` with `user_daily_metrics` (as per case columns).
- BigQuery dataset for model `analytics`.
- For running on google shell: `pip install --user dbt-bigquery` and export PATH=$PATH:~/.local/bin.

## 2) How to run on Google Shell
- Run dbt build 
- Run dbt run --full-refresh --select daily_metrics for a full run (not incremental run) 
- Run python viz.py for dashboard if it doesnt exist
- Download and open daily_metrics_dashboard.html for checking the dashboard
- daily_metrics file has the sample data 

You might need to create a ~/.dbt folder and add this profiles.yml to it
Create `~/.dbt/profiles.yml`:
```yaml
vertigo_profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: winter-accord-469013-d5
      dataset: analytics
      threads: 4
      location: europe-west1 


