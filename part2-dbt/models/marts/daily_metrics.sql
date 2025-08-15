{{ config(
    materialized='incremental',
    unique_key='event_date_country_platform'
) }}

with base as (
  select
    event_date,
    country,
    platform,
    user_id,
    coalesce(match_start_count, 0)     as match_start_count,
    coalesce(match_end_count, 0)       as match_end_count,
    coalesce(victory_count, 0)         as victory_count,
    coalesce(defeat_count, 0)          as defeat_count,
    coalesce(server_connection_error, 0) as server_connection_error,
    coalesce(iap_revenue, 0.0)         as iap_revenue,
    coalesce(ad_revenue,  0.0)         as ad_revenue
  from {{ source('raw', 'user_daily_metrics') }}
  {% if is_incremental() %}
    -- Process only new days when running incrementally
    where event_date >= (select coalesce(date_sub(max(event_date), interval 2 day), date('1970-01-01')) from {{ this }})
  {% endif %}
)

select
  event_date,
  country,
  platform,
  -- grain key for merge
  concat(cast(event_date as string), '::', country, '::', platform) as event_date_country_platform,

  count(distinct user_id)                                      as dau,
  sum(iap_revenue)                                             as total_iap_revenue,
  sum(ad_revenue)                                              as total_ad_revenue,
  safe_divide(sum(iap_revenue) + sum(ad_revenue), count(distinct user_id)) as arpdau,

  sum(match_start_count)                                       as matches_started,
  safe_divide(sum(match_start_count), count(distinct user_id)) as match_per_dau,

  safe_divide(sum(victory_count), nullif(sum(match_end_count),0)) as win_ratio,
  safe_divide(sum(defeat_count),  nullif(sum(match_end_count),0)) as defeat_ratio,

  safe_divide(sum(server_connection_error), count(distinct user_id)) as server_error_per_dau
from base
group by 1,2,3,4
