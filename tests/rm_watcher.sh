NAME="ABC"
[ -z "$1" ] || NAME="$1"
curl --header "Content-Type: application/json" \
  --request DELETE \
  --data '{"name":"'$NAME'"}' \
  localhost:8080/watchers
