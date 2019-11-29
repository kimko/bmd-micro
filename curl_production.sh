curl -d '{ "email": "angela.merkel@bundestag.de", "firstName": "Angela", "lastName": "Merkel", "zipCode": "97202"}' -H "Content-Type: application/json" -X  POST https://bmd-micro.herokuapp.com/users

sleep 1

curl -d '{ "email": "mitterand@elysee.fr", "firstName": "François", "lastName": "Mitterrand", "zipCode": "97202"}' -H "Content-Type: application/json" -X  POST https://bmd-micro.herokuapp.com/users

sleep 1

curl https://bmd-micro.herokuapp.com/users

sleep 1

curl -X DELETE https://bmd-micro.herokuapp.com/users/5949ac73-39bc-4498-b6f8-e265631fc240

sleep 1

curl -d '{"firstName": "Angi"}' -H "Content-Type: application/json" -X PUT https://bmd-micro.herokuapp.com/users/864acfcc-ae05-4485-80c9-1066bc761c11

sleep 1

curl https://bmd-micro.herokuapp.com/users/864acfcc-ae05-4485-80c9-1066bc761c11