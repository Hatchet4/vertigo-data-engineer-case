
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select event_date_country_platform
from `winter-accord-469013-d5`.`analytics`.`daily_metrics`
where event_date_country_platform is null



  
  
      
    ) dbt_internal_test