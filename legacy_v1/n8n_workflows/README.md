# 🔄 N8N Workflow Setup Guide

Complete guide to setting up n8n workflows for the 3-agent system.

---

## 🚀 Quick Start

### Option A: n8n Cloud (Recommended)

1. **Sign Up**
   - Go to: https://n8n.io/cloud
   - Create free account
   - Get your URL: `https://yourname.app.n8n.cloud`

2. **Import Workflow**
   - Click "Workflows" → "+" → "Import from File"
   - Upload: `2_advanced_3agents.json`
   - Click "Import"

3. **Configure URLs**
   - Update Flask URLs in all 3 HTTP Request nodes
   - For cloud: `http://YOUR-SERVER-IP:5000`

4. **Get Webhook URL**
   - Click "📥 Webhook Trigger" node
   - Copy Production URL
   - Add to `.env`: `N8N_CAMPAIGN_WEBHOOK=<url>`

5. **Activate**
   - Toggle "Inactive" → "Active" (top right)
   - ✅ Done!

---

### Option B: Docker (Local)

1. **Install Docker**
   - Download: https://www.docker.com/get-started

2. **Run n8n**
```bash
   docker run -d \
     --name n8n \
     -p 5678:5678 \
     -v ~/.n8n:/home/node/.n8n \
     --restart unless-stopped \
     n8nio/n8n
```

3. **Access n8n**
   - Open: http://localhost:5678
   - Create account (first time only)

4. **Import Workflow**
   - Follow steps from Option A
   - Use URLs: `http://host.docker.internal:5000` (Mac/Windows)
   - Or: `http://172.17.0.1:5000` (Linux)

---

## 📊 Workflow Architecture

### Advanced 3-Agent Workflow
```
User Request
    ↓
📥 Webhook Trigger
    ↓
📋 Extract Input Data
    ↓
🔍 Agent 1: Analyst Bot (/api/analyst/analyze)
    ↓
🧠 Agent 2: Strategy Bot (/api/strategy/create)
    ↓
🎨 Agent 3: Content Bot (/api/content/generate)
    ↓
🔗 Combine All Results
    ↓
✅ Return Complete Campaign
```

**Processing Time:** 30-40 seconds  
**Cost:** $0 (100% FREE)

---

## 🔧 Configuration Guide

### Step 1: Update Flask URLs

In each HTTP Request node, update the URL:

**For Docker n8n (Mac/Windows):**
```
http://host.docker.internal:5000/api/analyst/analyze
http://host.docker.internal:5000/api/strategy/create
http://host.docker.internal:5000/api/content/generate
```

**For Docker n8n (Linux):**
```
http://172.17.0.1:5000/api/analyst/analyze
http://172.17.0.1:5000/api/strategy/create
http://172.17.0.1:5000/api/content/generate
```

**For n8n Cloud:**
```
http://YOUR-PUBLIC-IP:5000/api/analyst/analyze
http://YOUR-PUBLIC-IP:5000/api/strategy/create
http://YOUR-PUBLIC-IP:5000/api/content/generate
```

### Step 2: Update Timeouts

In each HTTP Request node → Options → Timeout:
- Analyst: 60000ms (1 min)
- Strategy: 90000ms (1.5 min)
- Content: 120000ms (2 min)

### Step 3: Test Connection

1. Click "Execute Node" on Analyst Bot node
2. Check if Flask is reachable
3. Should return: 200 OK

---

## 🧪 Testing

### Test 1: Individual Agents
```bash
# Test Analyst Bot
curl -X POST http://localhost:5000/api/analyst/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "business_profile": {"business_name": "Test Store"},
    "sales_data": []
  }'

# Test Strategy Bot
curl -X POST http://localhost:5000/api/strategy/create \
  -H "Content-Type: application/json" \
  -d '{
    "business_profile": {"business_name": "Test Store"},
    "campaign_goal": "sales",
    "insights": {}
  }'

# Test Content Bot
curl -X POST http://localhost:5000/api/content/generate \
  -H "Content-Type: application/json" \
  -d '{
    "business_profile": {"business_name": "Test Store"},
    "strategy": {"daily_plan": []}
  }'
```

### Test 2: Complete Workflow
```bash
curl -X POST http://localhost:5678/webhook/campaign-3-agents \
  -H "Content-Type: application/json" \
  -d '{
    "business_profile": {
      "business_name": "Sparkle Jewelry",
      "niche": "Jewelry",
      "target_audience": "Women 25-40",
      "brand_voice": "Elegant"
    },
    "campaign_goal": "flash_sale",
    "sales_data": [
      {"week": "2026-02-10", "revenue": 35000, "items_sold": 45}
    ]
  }'
```

**Expected:**
- Processing: 30-40 seconds
- Response: Complete campaign JSON with 7 days

---

## 📈 Monitoring

### View Executions

1. Go to n8n → "Executions" (left sidebar)
2. See all workflow runs
3. Click any execution to see:
   - Input data
   - Each agent's output
   - Processing time
   - Success/failure status

### Check Logs

**n8n Logs:**
```bash
# Docker
docker logs n8n

# Follow logs
docker logs -f n8n
```

**Flask Logs:**
- Check terminal where `python app.py` is running
- See agent execution logs in real-time

---

## 🐛 Troubleshooting

### Issue: Connection Refused

**Symptoms:** HTTP Request nodes fail with "ECONNREFUSED"

**Solutions:**
1. Make sure Flask is running: `python app.py`
2. Check Flask URL is correct
3. For Docker:
   - Mac/Windows: Use `host.docker.internal`
   - Linux: Use `172.17.0.1`
4. For Cloud: Use public IP or deployed URL

### Issue: Timeout

**Symptoms:** Workflow times out after 60 seconds

**Solutions:**
1. Increase timeout in HTTP Request nodes
2. Check if Gemini API is responding
3. Verify API key in `.env`

### Issue: Invalid JSON

**Symptoms:** "JSON parse error" in results

**Solutions:**
1. Check Flask endpoints return valid JSON
2. Test endpoints individually with curl
3. Check Gemini API is working

### Issue: Webhook Not Working

**Symptoms:** 404 when calling webhook URL

**Solutions:**
1. Make sure workflow is activated (green toggle)
2. Check webhook URL is correct
3. Try re-saving the workflow

---

## 🎯 Best Practices

### 1. Use Production Webhook

Always use the "Production URL" from webhook trigger, not test URL.

### 2. Add Error Handling

In n8n, add "Error Workflow" to handle failures gracefully.

### 3. Set Timeouts

Always set appropriate timeouts for API calls:
- Quick operations: 30-60s
- AI generation: 90-120s

### 4. Monitor Executions

Regularly check execution logs for errors or slow performance.

### 5. Secure Webhooks

In production, add authentication to webhook endpoints.

---

## 🚀 Advanced Usage

### Multiple Workflows

You can create multiple workflows for different purposes:

1. **Campaign Generation** - Main 3-agent workflow
2. **Sales Analysis** - Just analyst bot
3. **Content Only** - Just content generation
4. **Scheduled Campaigns** - Auto-generate weekly

### Integration with Other Tools

n8n can connect to 300+ services:
- Google Sheets (save campaigns)
- Slack (notifications)
- Email (send reports)
- Airtable (database)
- Zapier alternative

---

## 📝 Workflow Files

- `2_advanced_3agents.json` - Main 3-agent workflow
- Test files available in this directory

---

## 🆘 Support

**Issues?**
- Check troubleshooting section above
- Test Flask endpoints individually
- Review n8n execution logs
- Ensure all dependencies installed

**n8n Documentation:**
- https://docs.n8n.io

**Flask Application:**
- Run: `python test_setup.py`
- Check: http://localhost:5000/health

---

## ✅ Checklist

- [ ] n8n installed (Docker or Cloud)
- [ ] Workflow imported
- [ ] URLs updated in all HTTP nodes
- [ ] Timeouts configured
- [ ] Workflow activated
- [ ] Webhook URL copied to .env
- [ ] Flask running
- [ ] Individual agents tested
- [ ] Full workflow tested
- [ ] Executions monitored

---

**Once everything is checked, your n8n integration is complete!** 🎉