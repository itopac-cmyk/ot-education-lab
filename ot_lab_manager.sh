#!/bin/bash
# OT-Education-Lab Management Tool

function start_ot() {
    echo "Launching OT Digital Twin Lab..."
    cd lab_infra && docker-compose up -d
    echo "Waiting for Digital Twin Engine..."
    sleep 5
    docker-compose ps
}

function test_sync() {
    echo "Testing PLC-to-Twin Synchronization..."
    # Force a modbus write via the attacker node (simulated)
    # We use a simple curl to the engine to see if it responds
    STATUS=\$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9000/api/state)
    if [ "\$STATUS" == "200" ]; then
        echo "✅ Digital Twin Engine is ONLINE."
    else
        echo "❌ Digital Twin Engine is OFFLINE."
    fi
}

case "\$1" in
    start) start_ot ;;
    stop) cd lab_infra && docker-compose down ;;
    test) test_sync ;;
    *) echo "Usage: \$0 {start|stop|test}" ;;
esac
