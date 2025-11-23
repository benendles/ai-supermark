# Troubleshooting 401 Unauthorized Error

## Problem
Getting `401 - wxO unauthorized - Authorization header is not present` error when using the dashboard.

## Solutions

### Solution 1: Check API Key Configuration

The API key might be empty or not properly set. Follow these steps:

1. **Check .env file**:
   ```bash
   cat .env
   ```
   Verify that `WO_API_KEY` has a value (not empty, not "your_api_key_here")

2. **Check Sidebar Configuration**:
   - Open dashboard sidebar
   - Look at "API Key" field
   - If empty, enter your API key
   - Click "💾 Save Configuration"

3. **Get a Valid API Key**:
   - Go to WatsonX Orchestrate console
   - Navigate to: Settings → API Keys
   - Generate a new API key or copy existing one
   - Paste it in the dashboard sidebar

### Solution 2: Verify API URL Format

The API URL should be in this format:
```
https://api.{region}.dl.watson-orchestrate.ibm.com/instances/{instance-id}
```

**Do NOT include `/api` at the end** - the dashboard adds it automatically.

**Correct Examples:**
- ✅ `https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/20251122-1952-5015-406d-88c46ca8b12a`
- ✅ `https://api.us-south.dl.watson-orchestrate.ibm.com/instances/abc123`

**Incorrect Examples:**
- ❌ `https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/xxx/api` (don't add /api)
- ❌ `https://api.eu-central-1.dl.watson-orchestrate.ibm.com/api/instances/xxx` (wrong format)

### Solution 3: Verify Agent ID

The Agent ID should match exactly what's in WatsonX Orchestrate:

1. **Find Agent ID in Console**:
   - Go to WatsonX Orchestrate → Agents
   - Find `supermarket_inventory_manager_agent`
   - Check the ID column (might be different from name)

2. **Use Correct ID**:
   - Try using the agent name: `supermarket_inventory_manager_agent`
   - Or use the actual ID from the console
   - Enter in dashboard sidebar → Agent ID field

### Solution 4: Test API Connection

Test if your credentials work:

```python
import requests

api_url = "https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/YOUR_INSTANCE_ID"
api_key = "YOUR_API_KEY"
agent_id = "supermarket_inventory_manager_agent"

url = f"{api_url}/api/v1/orchestrate/runs"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "agent_id": agent_id,
    "input": "Check low stock"
}

response = requests.post(url, headers=headers, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
```

If this works, the credentials are correct. If not, check the error message.

### Solution 5: Check API Key Format

WatsonX API keys are usually long strings. Make sure:
- ✅ No extra spaces before/after
- ✅ No quotes around the key
- ✅ Complete key copied (not truncated)
- ✅ Key hasn't expired

### Solution 6: Verify Instance URL

1. **Get Instance URL from Console**:
   - Log into WatsonX Orchestrate
   - Look at the browser URL or instance settings
   - Copy the full instance URL

2. **Format Should Be**:
   ```
   https://api.{region}.dl.watson-orchestrate.ibm.com/instances/{id}
   ```

### Solution 7: Check Environment Variables

If using `.env` file:

1. **Verify .env exists**:
   ```bash
   ls -la .env
   ```

2. **Check .env format**:
   ```env
   WO_INSTANCE=https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/YOUR_ID
   WO_API_KEY=your_actual_api_key_here
   SUPERMARKET_AGENT_ID=supermarket_inventory_manager_agent
   ```

3. **No spaces around =**:
   - ✅ `WO_API_KEY=abc123`
   - ❌ `WO_API_KEY = abc123` (spaces cause issues)

### Solution 8: Restart Dashboard

After changing configuration:

1. Stop the dashboard (Ctrl+C)
2. Restart: `streamlit run ai_supermarket/frontend/app.py`
3. Re-enter credentials in sidebar
4. Click "💾 Save Configuration"

## Quick Diagnostic Checklist

- [ ] API Key is not empty
- [ ] API Key doesn't contain "your_api_key_here" placeholder
- [ ] API URL is in correct format (no /api at end)
- [ ] Agent ID matches console
- [ ] .env file exists and is formatted correctly
- [ ] Dashboard restarted after .env changes
- [ ] Credentials saved in sidebar

## Still Not Working?

1. **Check WatsonX Console**:
   - Verify agent exists and is active
   - Check agent has all tools attached
   - Verify API key is active (not revoked)

2. **Try Direct API Call**:
   Use the test script above to verify credentials work

3. **Check Network**:
   - Ensure you can access WatsonX Orchestrate console
   - Check firewall/proxy settings
   - Verify SSL certificates

4. **Contact Support**:
   - Check WatsonX Orchestrate documentation
   - Review API authentication guide
   - Contact IBM support if needed

## Updated Dashboard Features

The dashboard now includes:
- ✅ Better validation of API credentials
- ✅ Clear error messages for 401 errors
- ✅ Configuration status indicators
- ✅ Helpful tips in error messages
- ✅ Automatic URL format correction

Try the dashboard again after checking the above items!

