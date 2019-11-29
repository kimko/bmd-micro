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

# curl -d '{"lastName": "new"}' -H "Content-Type: application/json" -X PUT localhost:5000/users/92573ca0-8e53-4e17-82e1-ec3b78883aaf