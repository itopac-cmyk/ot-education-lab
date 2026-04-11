#!/bin/bash
function start_ot() {
    echo "Launching OT Lab..."
    cd lab_infra && docker-compose up -d
    sleep 5
}
function test_sync() {
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9000/api/state)
    if [ "$STATUS" == "200" ]; then
        echo "✅ Digital Twin Engine is ONLINE."
    else
        echo "❌ Digital Twin Engine is OFFLINE."
    fi
}
case "$1" in
    start) start_ot ;;
    stop) cd lab_infra && docker-compose down ;;
    test) test_sync ;;
    *) echo "Usage: $0 {start|stop|test}" ;;
esac
