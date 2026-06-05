#!/bin/bash

# Secure Folder Command Center - Deployment Script
# This script deploys the application to gatewaynexus.org

set -e

echo "🚀 Starting Secure Folder Command Center Deployment"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker is installed${NC}"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker Compose is installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠ Creating .env file from template${NC}"
    cp .env.example .env || true
    echo -e "${YELLOW}⚠ Please edit .env with your configuration before proceeding${NC}"
fi

# Create SSL directory if it doesn't exist
mkdir -p ssl

# Generate self-signed SSL certificate if it doesn't exist
if [ ! -f ssl/cert.pem ] || [ ! -f ssl/key.pem ]; then
    echo -e "${YELLOW}⚠ Generating self-signed SSL certificate${NC}"
    openssl req -x509 -newkey rsa:4096 -nodes -out ssl/cert.pem -keyout ssl/key.pem -days 365 \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=gatewaynexus.org" || true
    echo -e "${GREEN}✓ SSL certificate generated${NC}"
fi

# Create secure_documents directory
mkdir -p secure_documents
mkdir -p logs

# Pull latest images
echo -e "${YELLOW}📦 Pulling Docker images${NC}"
docker-compose pull || true

# Build images
echo -e "${YELLOW}🔨 Building Docker images${NC}"
docker-compose build

# Start services
echo -e "${YELLOW}🚀 Starting services${NC}"
docker-compose up -d

# Wait for API to be ready
echo -e "${YELLOW}⏳ Waiting for API to start${NC}"
sleep 10

# Check if services are running
echo -e "${YELLOW}🔍 Checking service health${NC}"

if docker-compose ps | grep -q "api.*healthy"; then
    echo -e "${GREEN}✓ API is healthy${NC}"
else
    echo -e "${YELLOW}⚠ API may still be starting. Checking logs...${NC}"
    docker-compose logs api | tail -20
fi

if docker-compose ps | grep -q "nginx"; then
    echo -e "${GREEN}✓ Nginx is running${NC}"
else
    echo -e "${RED}✗ Nginx failed to start${NC}"
fi

# Display connection information
echo ""
echo -e "${GREEN}=================================================="
echo "✓ Secure Folder Command Center is running!"
echo "==================================================${NC}"
echo ""
echo "📱 Web Interface: https://gatewaynexus.org"
echo "🔌 API Endpoint: https://gatewaynexus.org/api"
echo ""
echo "📝 Logs:"
echo "   - API: docker-compose logs -f api"
echo "   - Nginx: docker-compose logs -f nginx"
echo "   - All: docker-compose logs -f"
echo ""
echo "🛑 To stop: docker-compose down"
echo "🔄 To restart: docker-compose restart"
echo ""
echo "🔒 Important:"
echo "   - Update .env with production credentials"
echo "   - Install real SSL certificate (Let's Encrypt)"
echo "   - Configure DNS to point gatewaynexus.org to this server"
echo ""
