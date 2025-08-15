-- back compat for old kwarg name
  
  
        
            
	    
	    
            
        
    

    

    merge into `winter-accord-469013-d5`.`analytics`.`daily_metrics` as DBT_INTERNAL_DEST
        using (
        select
        * from `winter-accord-469013-d5`.`analytics`.`daily_metrics__dbt_tmp`
        ) as DBT_INTERNAL_SOURCE
        on ((DBT_INTERNAL_SOURCE.event_date_country_platform = DBT_INTERNAL_DEST.event_date_country_platform))

    
    when matched then update set
        `event_date` = DBT_INTERNAL_SOURCE.`event_date`,`country` = DBT_INTERNAL_SOURCE.`country`,`platform` = DBT_INTERNAL_SOURCE.`platform`,`event_date_country_platform` = DBT_INTERNAL_SOURCE.`event_date_country_platform`,`dau` = DBT_INTERNAL_SOURCE.`dau`,`total_iap_revenue` = DBT_INTERNAL_SOURCE.`total_iap_revenue`,`total_ad_revenue` = DBT_INTERNAL_SOURCE.`total_ad_revenue`,`arpdau` = DBT_INTERNAL_SOURCE.`arpdau`,`matches_started` = DBT_INTERNAL_SOURCE.`matches_started`,`match_per_dau` = DBT_INTERNAL_SOURCE.`match_per_dau`,`win_ratio` = DBT_INTERNAL_SOURCE.`win_ratio`,`defeat_ratio` = DBT_INTERNAL_SOURCE.`defeat_ratio`,`server_error_per_dau` = DBT_INTERNAL_SOURCE.`server_error_per_dau`
    

    when not matched then insert
        (`event_date`, `country`, `platform`, `event_date_country_platform`, `dau`, `total_iap_revenue`, `total_ad_revenue`, `arpdau`, `matches_started`, `match_per_dau`, `win_ratio`, `defeat_ratio`, `server_error_per_dau`)
    values
        (`event_date`, `country`, `platform`, `event_date_country_platform`, `dau`, `total_iap_revenue`, `total_ad_revenue`, `arpdau`, `matches_started`, `match_per_dau`, `win_ratio`, `defeat_ratio`, `server_error_per_dau`)


    