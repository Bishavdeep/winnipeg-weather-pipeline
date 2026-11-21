{{ config(materialized='table') }}

/* 
  This model takes the raw JSON from S3 and flattens it into 
  a clean, daily weather summary table with all 7 forecast days.
*/

WITH raw_data AS (
    SELECT 
        raw_data,
        loaded_at
    FROM {{ source('raw_data', 'raw_weather_json') }}
),

flattened AS (
    SELECT
        f.value::DATE AS weather_date,
        raw_data:daily.temperature_2m_max[f.index]::FLOAT AS max_temp_celsius,
        raw_data:daily.temperature_2m_min[f.index]::FLOAT AS min_temp_celsius,
        raw_data:daily.precipitation_sum[f.index]::FLOAT AS precipitation_mm,
        raw_data:latitude::FLOAT AS latitude,
        raw_data:longitude::FLOAT AS longitude,
        raw_data:timezone::STRING AS timezone,
        loaded_at
    FROM raw_data,
    LATERAL FLATTEN(input => raw_data:daily.time) f
)

SELECT * FROM flattened
ORDER BY weather_date