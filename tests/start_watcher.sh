NAME="ABC"
[ -z "$1" ] || NAME="$1"
curl -H "Content-Type: application/json" localhost:8080/watcher/start/$NAME
