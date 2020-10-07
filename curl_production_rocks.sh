# Do some testing and demoing against the production api

set -o xtrace

echo "Invalid Rock World 1 - wrong shape"
sleep 1
curl -d '[ ". .       ", ". . :::::::::::::::::::::", " :T.::::::", ". . ::::::", "   .::::::"]' -H "Content-Type: application/json" -X  POST https://bmd-micro.herokuapp.com/rockworlds | jq

echo "Invalid Rock World 2 - dumb chars"
sleep 1
curl -d '[ ". .BAD    ", ". . ::::::", " :T.::::::", ". . ::::::", "   .::::::"]' -H "Content-Type: application/json" -X  POST https://bmd-micro.herokuapp.com/rockworlds | jq


echo "Cool Rock World 1"
sleep 1
curl -d '[ ". .       ", ". . ::::::", " :T.::::::", ". . ::::::", "   .::::::"]' -H "Content-Type: application/json" -X  POST https://bmd-micro.herokuapp.com/rockworlds | jq
