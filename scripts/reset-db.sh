#!/bin/bash

# FlowFacilitator - Reset Local Database
# WARNING: This will delete all data!

set -e

echo "⚠️  WARNING: This will delete ALL local data!"
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

# Navigate to project root
cd "$(dirname "$0")/.."

echo "🔄 Resetting database..."

# Stop containers
cd infra/supabase
docker-compose down -v

# Remove volume
docker volume rm supabase_postgres-data 2>/dev/null || true

# Restart
docker-compose up -d

# Wait for Postgres
echo "Waiting for PostgreSQL..."
sleep 10

# Apply migrations
echo "Applying migrations..."
docker exec -i supabase-db psql -U postgres -d postgres < migrations/001_initial_schema.sql

echo "✅ Database reset complete"
