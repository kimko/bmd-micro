# Do some testing and demoing against the production api
set -euo pipefail

echo "Invalid Rock World 1 - wrong shape"
sleep 1
curl -d '[ ". .       ", ". . :::::::::::::::::::::", " :T.::::::", ". . ::::::", "   .::::::"]' -H "Content-Type: application/json" -X  POST localhost:5000/rockworlds | jq

echo "Invalid Rock World 2 - dumb chars"
sleep 1
curl -d '[ ". .BAD    ", ". . ::::::", " :T.::::::", ". . ::::::", "   .::::::"]' -H "Content-Type: application/json" -X  POST localhost:5000/rockworlds | jq


echo "Cool Rock World 1"
sleep 1
curl -d '[ ". .       ", ". . ::::::", " :T.::::::", ". . ::::::", "   .::::::"]' -H "Content-Type: application/json" -X  POST localhost:5000/rockworlds | jq

echo "update Rock World 1"
sleep 1
curl -d '[ ". .       ", ". . .....T"]' -H "Content-Type: application/json" -X  PUT localhost:5000/rockworlds/1 | jq

echo "Get World 1"
curl localhost:5000/rockworlds/1 | jq

echo "random world"
curl -X  POST 'localhost:5000/rockworlds?random=true&columns=20&rows=20' | jq