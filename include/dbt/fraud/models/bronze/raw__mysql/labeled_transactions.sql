select 
    *
from
    {{ source('raw__mysql', 'labeled_transactions') }}