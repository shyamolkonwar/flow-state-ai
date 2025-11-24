#!/bin/bash
# Helper script to run integration tests

echo "Starting FlowFacilitator agent..."
python3 main.py > agent.log 2>&1 &
AGENT_PID=$!

echo "Agent PID: $AGENT_PID"
echo "Waiting for agent to start..."
sleep 5

# Check if agent is running
if curl -s http://127.0.0.1:8765/status > /dev/null 2>&1; then
    echo "✓ Agent is running"
    echo ""
    echo "Running integration test..."
    python3 test_integration.py
    TEST_EXIT=$?
    
    echo ""
    echo "Stopping agent..."
    kill $AGENT_PID 2>/dev/null
    
    exit $TEST_EXIT
else
    echo "✗ Agent failed to start"
    echo "Check agent.log for errors"
    kill $AGENT_PID 2>/dev/null
    exit 1
fi
