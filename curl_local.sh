curl -d '{ "email": "angela.merkel@bundestag.de", "firstName": "Angela", "lastName": "Merkel", "zipCode": "97202"}' -H "Content-Type: application/json" -X  POST localhost:5000/users

sleep 1

curl -d '{ "email": "mitterand@elysee.fr", "firstName": "François", "lastName": "Mitterrand", "zipCode": "97202"}' -H "Content-Type: application/json" -X  POST localhost:5000/users

sleep 1

curl -d '{ "email": "nobody@cares.com", "firstName": "Test", "lastName": "User", "zipCode": "97202"}' -H "Content-Type: application/json" -X  POST localhost:5000/users

sleep 1

curl localhost:5000/users/1

sleep 1

curl -X DELETE localhost:5000/users/3

sleep 1

curl -d '{"firstName": "Angi"}' -H "Content-Type: application/json" -X PUT localhost:5000/users/1

sleep 1

curl localhost:5000/users