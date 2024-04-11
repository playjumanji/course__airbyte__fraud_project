with transaction_summary as (
    select 
        ct.user_id,
        count(ct.transaction_id) as total_transactions,
        sum(
            case
                when lt.is_fraudulent
                then 1
                else 0
            end 
        ) as fraudulent_transactions,
        sum(
            case
                when NOT lt.is_fraudulent
                then 1
                else 0
            end 
        ) as non_fraudulent_transactions
        from {{ ref('customer_transactions') }} ct
            join {{ ref('labeled_transactions') }} lt 
            on ct.transaction_id = lt.transaction_id
        group by 
            ct.user_id
)
select 
    user_id,
    total_transactions,
    fraudulent_transactions,
    non_fraudulent_transactions,
    (fraudulent_transactions::FLOAT / total_transactions) * 100 as risk_score
from
    transaction_summary