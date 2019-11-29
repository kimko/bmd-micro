curl -d '{ "email": "angela.merkel@bundestag.de", "firstName": "Angela", "lastName": "Merkel", "zipCode": "97202"}' -H "Content-Type: application/json" -X  POST localhost:5000/users

sleep 1

curl -d '{ "email": "mitterand@elysee.fr", "firstName": "François", "lastName": "Mitterrand", "zipCode": "97202"}' -H "Content-Type: application/json" -X  POST localhost:5000/users

sleep 1

curl localhost:5000/users

sleep 1

curl localhost:5000/users/91f5e205-51db-4f9e-8f6e-98d9adffc723