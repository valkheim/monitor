# Get stats about a watcher
NAME="ABC"
[ -z "$1" ] || NAME="$1"
curl -vvv localhost:8080/stats/$NAME
