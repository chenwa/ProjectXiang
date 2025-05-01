SELECT 
    users.id AS user_id,
    users.name AS user_name,
    addresses.id AS address_id,
    addresses.city AS address_city
FROM 
    users
FULL OUTER JOIN 
    addresses
ON 
    users.id = addresses.user_id;
