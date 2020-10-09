# Do some testing and demoing against the production api
set -euo pipefail

echo "Create new User"
sleep 1

curl -d '{ "email": "angela.merkel@bundestag.de", "firstName": "Angela", "lastName": "Merkel", "zipCode": "97202"}' -H "Content-Type: application/json" -X  POST https://bmd-micro.herokuapp.com/users

sleep 2
clear

echo "Create another new User"
sleep 1

curl -d '{ "email": "mitterand@elysee.fr", "firstName": "François", "lastName": "Mitterrand", "zipCode": "97202"}' -H "Content-Type: application/json" -X  POST https://bmd-micro.herokuapp.com/users

sleep 2
clear

echo "Create a third User"
sleep 1

curl -d '{ "email": "nobody@cares.com", "firstName": "Test", "lastName": "User", "zipCode": "97202"}' -H "Content-Type: application/json" -X  POST https://bmd-micro.herokuapp.com/users

sleep 2
clear

echo "Show first User"
sleep 1

curl https://bmd-micro.herokuapp.com/users/1

sleep 2
clear

echo "Delete third user"
sleep 1

curl -X DELETE https://bmd-micro.herokuapp.com/users/3

sleep 2
clear

echo "Update first User"
sleep 1

curl -d '{"firstName": "Angi"}' -H "Content-Type: application/json" -X PUT https://bmd-micro.herokuapp.com/users/1

sleep 2
clear

echo "Show all Users"
sleep 1

curl https://bmd-micro.herokuapp.com/users
