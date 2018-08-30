curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"name":"xyz","command":"ls","args":["-l", "-a"]}' \
  localhost:8080/watchers
