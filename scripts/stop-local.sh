#!/bin/bash

# FlowFacilitator - Stop Local Development Environment

set -e

echo "🛑 Stopping FlowFacilitator Local Environment..."

# Navigate to project root
cd "$(dirname "$0")/.."

# Stop Supabase
echo "Stopping Supabase..."
cd infra/supabase
docker-compose down

echo "✅ All services stopped"
