# Fix for 401 Unauthorized Error in Flask UI

## Problem
Getting `401 Unauthorized` error when using the Flask UI to interact with WatsonX Orchestrate agent.

## Solution Applied

### 1. Enhanced API Key Validation
- ✅ Checks if API key is empty or placeholder
- ✅ Validates API key length (minimum 8 characters)
- ✅ Strips whitespace from API key
- ✅ Better error messages for invalid keys

### 2. Improved Error Handling
- ✅ Specific error messages for 401 (Unauthorized)
- ✅ Helpful tips for common authentication issues
- ✅ Better error formatting in frontend

### 3. Configuration Check
The Flask app now validates:
- API key is not empty
- API key is not "your_api_key_here" placeholder
- API key is not "none" or "None"
- API key has minimum length

## How to Fix

### Step 1: Check Your API Key

1. **Open Configuration Modal** in the Flask UI
2. **Check API Key field** - make sure it's not empty
3. **Verify API Key** is correct from WatsonX Orchestrate console

### Step 2: Get a Valid API Key

1. Go to **WatsonX Orchestrate Console**
2. Navigate to **Settings → API Keys**
3. **Generate** a new key or **copy** existing one
4. **Paste** it in the Flask UI Configuration modal

### Step 3: Save Configuration

1. Click **"💾 Save Configuration"** button
2. Verify status shows **"✅ Configuration looks good!"**
3. Try your command again

## Common Issues

### Issue 1: API Key is Empty
**Error**: "API Key is empty or invalid"

**Solution**: 
- Enter your API key in the Configuration modal
- Make sure it's not just whitespace
- Copy the entire key (no truncation)

### Issue 2: API Key is Invalid/Expired
**Error**: "401 Unauthorized"

**Solution**:
- Generate a new API key from WatsonX console
- Make sure the key hasn't expired
- Check the key is for the correct instance

### Issue 3: API Key Not Saved
**Error**: Configuration not persisting

**Solution**:
- Click "💾 Save Configuration" after entering credentials
- Check browser console for errors
- Try refreshing the page

## Verification

After fixing, you should see:
- ✅ Status indicator shows "Ready" (green)
- ✅ Configuration modal shows "✅ Configuration looks good!"
- ✅ Commands execute without 401 errors

## Updated Code Features

The Flask app now:
- ✅ Validates API key before making requests
- ✅ Provides clear error messages for 401 errors
- ✅ Shows helpful tips in the UI
- ✅ Checks for common API key issues

## Testing

Test with a simple command:
```
Check low stock
```

If you still get 401:
1. Double-check API key in Configuration
2. Verify API key in WatsonX console
3. Try generating a new API key
4. Check that agent ID is correct

The enhanced error messages will now guide you to the specific issue!

