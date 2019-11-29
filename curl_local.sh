curl -d '{ "email": "angela.merkel@bundestag.de", "firstName": "Angela", "lastName": "Merkel", "zipCode": "97202"}' -H "Content-Type: application/json" -X  POST localhost:5000/users

sleep 1

curl -d '{ "email": "mitterand@elysee.fr", "firstName": "François", "lastName": "Mitterrand", "zipCode": "97202"}' -H "Content-Type: application/json" -X  POST localhost:5000/users

sleep 1

curl localhost:5000/users

sleep 1

curl localhost:5000/users/91f5e205-51db-4f9e-8f6e-98d9adffc723

sleep 1

curl -X DELETE localhost:5000/users/5949ac73-39bc-4498-b6f8-e265631fc240

sleep 1

curl -d'{"lastName": "new"}' -H "Content-Type: application/json" -x PUT localhost:5000/users/22f3ed69-2785-4d95-a6fc-2088495a3571