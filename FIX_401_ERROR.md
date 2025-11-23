# Fix for 401 Unauthorized Error

## Problem
Getting `401 - wxO unauthorized - Authorization header is not present` when clicking dashboard buttons.

## Root Cause
The API key is likely empty or not being passed correctly to the request headers.

## Solution Applied

### 1. Enhanced API Key Validation
- ✅ Checks if API key is empty
- ✅ Checks if API key is placeholder text
- ✅ Strips whitespace from API key
- ✅ Validates header is set correctly

### 2. Improved URL Format Handling
- ✅ Automatically adds `/api` to instance URLs
- ✅ Handles URLs with/without trailing slashes
- ✅ Correct endpoint: `{instance_url}/api/v1/orchestrate/runs`

### 3. Better Error Messages
- ✅ Specific error for 401 unauthorized
- ✅ Helpful tips for fixing API key issues
- ✅ Configuration status indicators

## How to Fix

### Step 1: Check Your .env File

```bash
cat .env
```

Should contain:
```env
WO_INSTANCE=https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/YOUR_INSTANCE_ID
WO_API_KEY=your_actual_api_key_here
SUPERMARKET_AGENT_ID=supermarket_inventory_manager_agent
```

**Important**: 
- `WO_API_KEY` must have a real value (not empty, not "your_api_key_here")
- No spaces around the `=` sign
- No quotes around values

### Step 2: Get Your API Key

1. Go to **WatsonX Orchestrate Console**
2. Navigate to **Settings → API Keys**
3. **Generate** a new key or **copy** existing one
4. Paste it in `.env` file as `WO_API_KEY=...`

### Step 3: Configure in Dashboard

1. **Start dashboard**: `streamlit run ai_supermarket/frontend/app.py`
2. **Open sidebar** (click ☰ icon)
3. **Enter credentials**:
   - API URL: Your instance URL (without /api)
   - API Key: Your API key
   - Agent ID: `supermarket_inventory_manager_agent`
4. **Click "💾 Save Configuration"**
5. **Verify**: Should show "✅ Configuration looks good!"

### Step 4: Test Connection

1. Click **"🔍 Check Low Stock"** in sidebar
2. Should work now!

## API URL Format

**Correct Format:**
```
https://api.eu-central-1.dl.watson-orchestrate.ibm.com/instances/20251122-1952-5015-406d-88c46ca8b12a
```

**The dashboard automatically adds `/api`**, so don't include it.

## Verification

To verify your credentials are correct:

1. **Check .env file exists and has values**
2. **Check sidebar shows configuration**
3. **Try a simple command**: "Check low stock"
4. **If still 401**: API key might be invalid/expired - generate new one

## Common Mistakes

❌ **Empty API Key**: `WO_API_KEY=` (no value)
❌ **Placeholder**: `WO_API_KEY=your_api_key_here`
❌ **Spaces**: `WO_API_KEY = abc123` (spaces around =)
❌ **Wrong URL**: Including `/api` in instance URL
❌ **Expired Key**: Using old/revoked API key

✅ **Correct**: `WO_API_KEY=actual_long_api_key_string`
✅ **Correct**: Instance URL without `/api` suffix

## Updated Code Features

The dashboard now:
- ✅ Validates API key is not empty
- ✅ Strips whitespace from credentials
- ✅ Shows clear error messages
- ✅ Provides helpful tips for 401 errors
- ✅ Displays configuration status

Try again after setting your API key correctly!

