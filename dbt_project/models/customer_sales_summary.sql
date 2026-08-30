SELECT
    customer_id,
    SUM(total_amount) AS total_spent
FROM {{ source('raw', 'sales') }}
GROUP BY customer_id