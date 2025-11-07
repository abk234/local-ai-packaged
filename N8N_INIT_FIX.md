# Fix n8n "Unauthorized" Initialization Errors

## Problem
n8n is showing multiple "Unauthorized" errors during initialization:
- "Init Problem: There was a problem loading init data: Unauthorized"
- "ResponseError: Unauthorized"
- "Could not check if an api key already exists"

## Root Cause
The `.env` file contains placeholder values for n8n secrets:
- `N8N_ENCRYPTION_KEY=sssss` (should be a 64-character hex string)
- `N8N_USER_MANAGEMENT_JWT_SECRET=sssssss` (should be a 64-character hex string)

These placeholder values prevent n8n from properly initializing and cause authentication/authorization failures.

## Solution

### Step 1: Generate Proper Secrets

Run this command to generate secure values:

```bash
python3 -c "import secrets; print('N8N_ENCRYPTION_KEY=' + secrets.token_hex(32)); print('N8N_USER_MANAGEMENT_JWT_SECRET=' + secrets.token_hex(32))"
```

### Step 2: Update .env File

Edit your `.env` file and replace the placeholder values:

```bash
# Replace these lines:
N8N_ENCRYPTION_KEY=sssss
N8N_USER_MANAGEMENT_JWT_SECRET=sssssss

# With proper 64-character hex values (from Step 1)
N8N_ENCRYPTION_KEY=<generated_64_char_hex>
N8N_USER_MANAGEMENT_JWT_SECRET=<generated_64_char_hex>
```

### Step 3: Restart n8n

```bash
docker restart n8n
```

Wait 15-20 seconds for n8n to fully restart and initialize.

### Step 4: Verify

1. Open n8n at http://localhost:6678
2. Check if the "Unauthorized" errors are gone
3. You should be able to access n8n without initialization errors

## Alternative: Use setup_env.py

You can also regenerate all environment variables:

```bash
python3 setup_env.py --force
```

**Note**: This will regenerate ALL secrets in your `.env` file, which may require restarting other services that depend on those values.

## Why This Happens

When n8n starts, it uses `N8N_ENCRYPTION_KEY` to encrypt sensitive data and `N8N_USER_MANAGEMENT_JWT_SECRET` for JWT token signing. If these are invalid placeholder values, n8n cannot:
- Properly encrypt/decrypt credentials
- Validate JWT tokens
- Initialize its internal state

This results in "Unauthorized" errors throughout the application.

## Prevention

Always use `setup_env.py` to generate proper secrets, or ensure your `.env` file has valid values before starting services.

## Related Issues

After fixing the initialization errors, you may still need to:
1. Create Ollama credentials in n8n (see `N8N_OLLAMA_FIX.md`)
2. Re-assign credentials to workflow nodes
3. Test your workflows

