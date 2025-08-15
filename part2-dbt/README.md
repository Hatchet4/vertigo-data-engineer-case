# Part 2 — dbt on BigQuery

## 1) Prereqs
- BigQuery dataset `raw` with `user_daily_metrics` (as per case columns).
- BigQuery dataset for model `analytics`.
- For running on google shell: `pip install --user dbt-bigquery` and export PATH=$PATH:~/.local/bin.

## 2) How to run on Google Shell
- Run dbt build 
- Run dbt run --full-refresh --select daily_metrics for not inccremental run

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

## 2) How to run on google shell
