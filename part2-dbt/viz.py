PROJECT_ID = "winter-accord-469013-d5"
DATASET    = "analytics"
TABLE      = "daily_metrics"
DAYS       = 600  # lookback window

from google.cloud import bigquery
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
from datetime import date

client = bigquery.Client(project=PROJECT_ID)

sql = f"""
SELECT
  event_date,
  country,
  platform,
  dau,
  total_iap_revenue,
  total_ad_revenue,
  arpdau,
  matches_started,
  match_per_dau,
  win_ratio,
  defeat_ratio,
  server_error_per_dau
FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
WHERE event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL {DAYS} DAY)
ORDER BY event_date, country, platform
"""
df = client.query(sql).to_dataframe()
if df.empty:
    raise SystemExit("Query returned 0 rows. Increase DAYS or check table path.")

for col in ["country", "platform"]:
    if col in df.columns:
        df[col] = df[col].fillna("UNKNOWN").replace("", "UNKNOWN")

df_dau = df.groupby("event_date", as_index=False)["dau"].sum()
fig_dau = px.line(df_dau, x="event_date", y="dau",
                  title=f"Daily Active Users (Last {DAYS} Days)")
fig_dau.update_layout(xaxis_title="Date", yaxis_title="DAU")

df_rev = df.groupby("event_date", as_index=False)[["total_iap_revenue","total_ad_revenue"]].sum()
fig_rev = make_subplots(specs=[[{"secondary_y": True}]])
fig_rev.add_trace(go.Scatter(x=df_rev["event_date"], y=df_rev["total_iap_revenue"],
                             mode="lines", name="IAP Revenue"), secondary_y=False)
fig_rev.add_trace(go.Scatter(x=df_rev["event_date"], y=df_rev["total_ad_revenue"],
                             mode="lines", name="Ad Revenue"), secondary_y=True)
fig_rev.update_layout(title_text=f"Revenue Over Time (Last {DAYS} Days)")
fig_rev.update_xaxes(title_text="Date")
fig_rev.update_yaxes(title_text="IAP Revenue", secondary_y=False)
fig_rev.update_yaxes(title_text="Ad Revenue", secondary_y=True)

agg_cols = ["dau","arpdau","matches_started","match_per_dau","win_ratio","server_error_per_dau"]
df_cmp = df.groupby(["platform","country"], as_index=False)[agg_cols].mean()
fig_cmp = px.bar(
    df_cmp.sort_values("dau", ascending=False),
    x="platform", y="dau", color="country", barmode="group",
    title=f"Avg DAU by Platform & Country (Last {DAYS} Days)"
)

df_arpdau = df.groupby("event_date", as_index=False)["arpdau"].mean()
fig_arpdau = px.line(df_arpdau, x="event_date", y="arpdau",
                     title=f"ARPDAU (Mean) Over Time (Last {DAYS} Days)")
fig_arpdau.update_layout(xaxis_title="Date", yaxis_title="ARPDAU")

divs = []
for figure in [fig_dau, fig_rev, fig_cmp, fig_arpdau]:
    divs.append(pio.to_html(figure, include_plotlyjs=False, full_html=False))

html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Daily Metrics Dashboard</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 20px; }}
    h1 {{ margin-bottom: 0; }}
    .subtitle {{ color: #666; margin-top: 4px; margin-bottom: 24px; }}
    .card {{ margin: 20px 0; padding: 10px; border: 1px solid #eee; border-radius: 8px; }}
  </style>
</head>
<body>
  <h1>Daily Metrics Dashboard</h1>
  <div class="subtitle">Source: {PROJECT_ID}.{DATASET}.{TABLE} — Generated on {date.today().isoformat()}</div>

  <div class="card">{divs[0]}</div>
  <div class="card">{divs[1]}</div>
  <div class="card">{divs[2]}</div>
  <div class="card">{divs[3]}</div>
</body>
</html>
"""

out_path = "daily_metrics_dashboard.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Exported: {out_path}")
