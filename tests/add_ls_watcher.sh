NAME="ABC"
[ -z "$1" ] || NAME="$1"
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"name":"'$NAME'","command":"ls","args":["-l", "-a"]}' \
  localhost:8080/watchers
