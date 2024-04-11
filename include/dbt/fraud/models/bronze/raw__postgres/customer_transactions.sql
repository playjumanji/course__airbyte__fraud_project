select 
    *
from
    {{ source('raw__postgres', 'customer_transactions') }}