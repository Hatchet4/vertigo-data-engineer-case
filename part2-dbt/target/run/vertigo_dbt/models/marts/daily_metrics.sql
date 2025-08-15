
  
    

    create or replace table `winter-accord-469013-d5`.`analytics`.`daily_metrics`
      
    partition by event_date
    cluster by country, platform

    
    OPTIONS()
    as (
      

WITH base AS (
  SELECT
    event_date,
    country,
    platform,
    user_id,
    COALESCE(match_start_count, 0)       AS match_start_count,
    COALESCE(match_end_count, 0)         AS match_end_count,
    COALESCE(victory_count, 0)           AS victory_count,
    COALESCE(defeat_count, 0)            AS defeat_count,
    COALESCE(server_connection_error, 0) AS server_connection_error,
    COALESCE(iap_revenue, 0.0)           AS iap_revenue,
    COALESCE(ad_revenue,  0.0)           AS ad_revenue
  FROM `winter-accord-469013-d5`.`raw`.`user_daily_metrics`
  
)

SELECT
  event_date,
  COALESCE(NULLIF(TRIM(country),   ""), "∅") AS country,
  COALESCE(NULLIF(TRIM(platform),  ""), "∅") AS platform,

  CONCAT(
    CAST(event_date AS STRING), '::',
    COALESCE(NULLIF(TRIM(country),  ""), "∅"), '::',
    COALESCE(NULLIF(TRIM(platform), ""), "∅")
  ) AS event_date_country_platform,

  COUNT(DISTINCT user_id)                                            AS dau,
  SUM(iap_revenue)                                                   AS total_iap_revenue,
  SUM(ad_revenue)                                                    AS total_ad_revenue,
  SAFE_DIVIDE(SUM(iap_revenue) + SUM(ad_revenue), COUNT(DISTINCT user_id)) AS arpdau,

  SUM(match_start_count)                                             AS matches_started,
  SAFE_DIVIDE(SUM(match_start_count), COUNT(DISTINCT user_id))       AS match_per_dau,

  SAFE_DIVIDE(SUM(victory_count), NULLIF(SUM(match_end_count), 0))   AS win_ratio,
  SAFE_DIVIDE(SUM(defeat_count),  NULLIF(SUM(match_end_count), 0))   AS defeat_ratio,

  SAFE_DIVIDE(SUM(server_connection_error), COUNT(DISTINCT user_id)) AS server_error_per_dau
FROM base
GROUP BY 1,2,3,4
    );
  