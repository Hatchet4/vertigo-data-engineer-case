# Part 2 — dbt on BigQuery

## 1) Prereqs
- BigQuery dataset `raw` with `user_daily_metrics` (as per case columns).
- BigQuery dataset for models, e.g. `analytics`.
- `pip install dbt-bigquery` and `gcloud auth application-default login`.

Create `~/.dbt/profiles.yml`:
```yaml
vertigo_profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: <GCP_PROJECT_ID>
      dataset: analytics
      threads: 4
      location: EU
