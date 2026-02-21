# 🐛 N8N Troubleshooting Guide

Common issues and solutions for n8n integration.

---

## Issue 1: Connection Refused (ECONNREFUSED)

**Symptoms:**
```
Error: connect ECONNREFUSED 127.0.0.1:5000
```

**Causes:**
- Flask is not running
- Wrong URL in n8n nodes
- Docker networking issue

**Solutions:**

1. **Check Flask is running:**
```bash
   # Start Flask
   python app.py
   
   # Verify it's running
   curl http://localhost:5000/health
```

2. **Update URLs in n8n:**
   - Mac/Windows Docker: `http://host.docker.internal:5000`
   - Linux Docker: `http://172.17.0.1:5000`
   - Cloud n8n: `http://YOUR-PUBLIC-IP:5000`

3. **Test connectivity from n8n:**
   - Click "Execute Node" on any HTTP Request node
   - Check the error message
   - Verify the URL is reachable

---

## Issue 2: Timeout Errors

**Symptoms:**
```
Error: Request timed out after 60000ms
```

**Causes:**
- Default timeout too short for AI processing
- Gemini API slow response
- Network latency

**Solutions:**

1. **Increase timeout in n8n:**
   - Click HTTP Request node
   - Go to "Options" tab
   - Set "Timeout" to 120000 (2 minutes)

2. **Check Gemini API:**
```bash
   # Test Gemini directly
   python -c "
   from ai_services.gemini_ai import create_gemini_ai
   gemini = create_gemini_ai()
   print(gemini.generate('Hello'))
   "
```

3. **Verify API key:**
   - Check `.env` has `GOOGLE_GEMINI_API_KEY`
   - Test with: `python test_setup.py`

---

## Issue 3: Webhook 404 Not Found

**Symptoms:**
```
Error: 404 Not Found
```

**Causes:**
- Workflow not activated
- Wrong webhook URL
- Workflow deleted/modified

**Solutions:**

1. **Activate workflow:**
   - Open workflow in n8n
   - Toggle "Inactive" → "Active" (top right)
   - Green = active

2. **Get correct webhook URL:**
   - Click "Webhook Trigger" node
   - Copy the "Production URL"
   - Update in `.env`

3. **Test webhook:**
```bash
   curl -X POST <webhook-url> \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
```

---

## Issue 4: Invalid JSON Response

**Symptoms:**
```
Error: Unexpected token in JSON
```

**Causes:**
- Flask endpoint returning HTML instead of JSON
- Error in Flask code
- Gemini returning malformed JSON

**Solutions:**

1. **Test Flask endpoints directly:**
```bash
   curl -X POST http://localhost:5000/api/analyst/analyze \
     -H "Content-Type: application/json" \
     -d '{"business_profile": {}, "sales_data": []}'
```

2. **Check Flask logs:**
   - Look for errors in terminal
   - Check if Gemini is working

3. **Add error handling:**
   - Ensure all endpoints return JSON
   - Check `Content-Type: application/json` header

---

## Issue 5: n8n Won't Start

**Symptoms:**
```
docker: Error response from daemon
```

**Causes:**
- Port 5678 already in use
- Docker not running
- Insufficient permissions

**Solutions:**

1. **Check port availability:**
```bash
   # Mac/Linux
   lsof -i :5678
   
   # Windows
   netstat -ano | findstr :5678
```

2. **Kill conflicting process:**
```bash
   # Mac/Linux
   kill -9 <PID>
   
   # Windows
   taskkill /F /PID <PID>
```

3. **Use different port:**
```bash
   docker run -d -p 5679:5678 n8nio/n8n
```

---

## Issue 6: Workflow Execution Hangs

**Symptoms:**
- Workflow runs but never completes
- No error messages
- Execution shows "Running" forever

**Causes:**
- Infinite loop in code node
- Agent not returning response
- Network issue

**Solutions:**

1. **Check n8n execution logs:**
   - Click execution in "Executions" tab
   - See which node is stuck
   - Check node output

2. **Test stuck agent:**
```bash
   # Test the specific agent endpoint
   curl -X POST http://localhost:5000/api/analyst/analyze \
     -H "Content-Type: application/json" \
     -d '{"business_profile": {}, "sales_data": []}'
```

3. **Restart n8n:**
```bash
   docker restart n8n-agentic-ai
```

---

## Issue 7: Docker host.docker.internal Not Working

**Symptoms:**
```
Error: getaddrinfo ENOTFOUND host.docker.internal
```

**Cause:**
- Linux doesn't support `host.docker.internal` by default

**Solution:**

Use `172.17.0.1` instead:
```
http://172.17.0.1:5000/api/analyst/analyze
```

Or add to docker-compose.yml:
```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

---

## Issue 8: Gemini API Quota Exceeded

**Symptoms:**
```
Error: 429 Too Many Requests
```

**Cause:**
- Exceeded free tier limit (60 req/min)

**Solutions:**

1. **Wait and retry:**
   - Free tier resets every minute
   - Add delay between requests

2. **Implement rate limiting:**
   - Add delay node in n8n workflow
   - Limit concurrent executions

3. **Upgrade to paid tier:**
   - Google Cloud pricing
   - Higher quota limits

---

## Issue 9: Data Not Passing Between Nodes

**Symptoms:**
- Nodes execute but data is null/empty
- Subsequent nodes fail

**Cause:**
- Incorrect node references
- Wrong data structure

**Solution:**

1. **Check node references:**
```javascript
   // Correct
   $('🔍 AGENT 1: Analyst Bot').item.json
   
   // Wrong
   $json.insights  // Only works for previous node
```

2. **Verify data structure:**
   - Click on node
   - Check "Output" tab
   - Ensure data is present

---

## Issue 10: Workflow Imported But Nodes Don't Work

**Symptoms:**
- Workflow imports successfully
- But execution fails immediately

**Cause:**
- n8n version mismatch
- Node types changed

**Solution:**

1. **Update n8n:**
```bash
   docker pull n8nio/n8n:latest
   docker stop n8n-agentic-ai
   docker rm n8n-agentic-ai
   # Run setup script again
```

2. **Recreate nodes manually:**
   - Follow the README guide
   - Create workflow from scratch

---

## Quick Diagnostic Checklist

Run through this checklist:

- [ ] Flask is running (`python app.py`)
- [ ] Flask health check works (`curl http://localhost:5000/health`)
- [ ] n8n is running (`docker ps | grep n8n`)
- [ ] Workflow is activated (green toggle)
- [ ] URLs are correct in all nodes
- [ ] Timeouts are set appropriately
- [ ] Gemini API key is in `.env`
- [ ] Webhook URL is in `.env`
- [ ] Individual agents work (`curl` tests)
- [ ] n8n execution logs show no errors

---

## Still Having Issues?

1. **Run full test:**
```bash
   python test_setup.py
   python n8n_workflows/test_workflow.py
```

2. **Check logs:**
```bash
   # Flask logs
   # (see terminal where app.py is running)
   
   # n8n logs
   docker logs -f n8n-agentic-ai
```

3. **Test manually:**
   - Open workflow in n8n
   - Click "Execute Workflow"
   - Watch each node execute
   - Check outputs at each step

---

**Most issues are solved by:**
1. ✅ Verifying Flask is running
2. ✅ Using correct URLs for your setup
3. ✅ Activating the workflow
4. ✅ Setting appropriate timeouts