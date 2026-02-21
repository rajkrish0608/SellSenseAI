#!/bin/bash

echo "========================================"
echo "🔧 N8N SETUP FOR AGENTIC SALES AI"
echo "========================================"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found!"
    echo "Please install Docker: https://www.docker.com/get-started"
    exit 1
fi

echo "✅ Docker found"
echo ""

# Start n8n with docker-compose
if [ -f "n8n_workflows/docker-compose.yml" ]; then
    echo "🚀 Starting n8n with docker-compose..."
    cd n8n_workflows
    docker-compose up -d
    cd ..
else
    echo "🚀 Starting n8n with docker run..."
    docker run -d \
      --name n8n-agentic-ai \
      -p 5678:5678 \
      -v ~/.n8n:/home/node/.n8n \
      --restart unless-stopped \
      --add-host=host.docker.internal:host-gateway \
      n8nio/n8n
fi

echo ""
echo "⏳ Waiting for n8n to start (30 seconds)..."
sleep 30

echo ""
echo "========================================"
echo "✅ N8N STARTED!"
echo "========================================"
echo ""
echo "📍 Access n8n at: http://localhost:5678"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. Open n8n: http://localhost:5678"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "2. Import workflow:"
echo "   • Click 'Workflows' → '+' → 'Import from File'"
echo "   • Select: n8n_workflows/2_advanced_3agents.json"
echo ""
echo "3. Update Flask URLs:"
echo "   • Mac/Windows: http://host.docker.internal:5000"
echo "   • Linux: http://172.17.0.1:5000"
echo ""
echo "4. Get webhook URL:"
echo "   • Click 'Webhook Trigger' node"
echo "   • Copy Production URL"
echo ""
echo "5. Add to .env:"
echo "   N8N_CAMPAIGN_WEBHOOK=<your-webhook-url>"
echo ""
echo "6. Activate workflow (toggle to Active)"
echo ""
echo "7. Test workflow:"
echo "   python n8n_workflows/test_workflow.py"
echo ""
echo "========================================"
echo ""
echo "🛑 To stop n8n:"
echo "   docker stop n8n-agentic-ai"
echo ""
echo "🔄 To restart n8n:"
echo "   docker start n8n-agentic-ai"
echo ""
echo "📊 To view logs:"
echo "   docker logs -f n8n-agentic-ai"
echo ""
echo "========================================"