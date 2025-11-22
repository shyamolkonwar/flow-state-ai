#!/bin/bash

# FlowFacilitator - Start Local Development Environment
# This script starts all required services for local development

set -e

echo "🚀 Starting FlowFacilitator Local Environment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

# Navigate to project root
cd "$(dirname "$0")/.."

# Start Supabase
echo -e "${YELLOW}Starting Supabase...${NC}"
cd infra/supabase

# Generate JWT secret if not exists
if [ ! -f .env ]; then
    echo "Generating environment variables..."
    JWT_SECRET=$(openssl rand -base64 32)
    SERVICE_ROLE_KEY=$(openssl rand -base64 32)
    ANON_KEY=$(openssl rand -base64 32)
    SECRET_KEY_BASE=$(openssl rand -base64 64)
    
    cat > .env << EOF
JWT_SECRET=${JWT_SECRET}
SERVICE_ROLE_KEY=${SERVICE_ROLE_KEY}
ANON_KEY=${ANON_KEY}
SECRET_KEY_BASE=${SECRET_KEY_BASE}
EOF
fi

docker-compose up -d

# Wait for Postgres to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 10

# Check if migrations have been applied
echo -e "${YELLOW}Checking database migrations...${NC}"
MIGRATION_CHECK=$(docker exec supabase-db psql -U postgres -d postgres -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='sessions';" 2>/dev/null || echo "0")

if [ "$MIGRATION_CHECK" = "0" ]; then
    echo "Applying database migrations..."
    docker exec -i supabase-db psql -U postgres -d postgres < migrations/001_initial_schema.sql
    echo -e "${GREEN}✅ Migrations applied${NC}"
else
    echo -e "${GREEN}✅ Database already initialized${NC}"
fi

cd ../..

echo -e "${GREEN}✅ Supabase started${NC}"
echo "   - Database: postgresql://postgres:postgres@localhost:54322/postgres"
echo "   - API: http://localhost:54321"
echo "   - Studio: http://localhost:54323"

# Display next steps
echo ""
echo "📝 Next steps:"
echo "   1. Start the agent:"
echo "      cd agent && source venv/bin/activate && python main.py --dev"
echo ""
echo "   2. Start the dashboard:"
echo "      cd dashboard/ui && npm run dev"
echo ""
echo "   3. Load Chrome extension:"
echo "      Open chrome://extensions/, enable Developer mode, and load unpacked from chrome-extension/"
echo ""
echo "🎯 Happy coding!"
