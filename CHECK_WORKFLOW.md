# Checking V3 Workflow Status

## Issue
Workflow is not triggering when files are added to `/data/shared`.

## Steps to Diagnose

### 1. Check if Workflow is Imported

**Via n8n UI:**
1. Open http://localhost:6678
2. Go to "Workflows" in the left sidebar
3. Look for "V3 Local Agentic RAG AI Agent"
4. Check if it exists and if it shows "Active" status

**Via Command Line:**
```bash
# Check import logs
docker logs n8n-import

# Check if workflow files exist
ls -la n8n/backup/workflows/
```

### 2. Activate the Workflow

If the workflow exists but is **not active**:
1. Open the workflow in n8n UI
2. Click the toggle switch in the top right to activate it
3. The workflow should show "Active" status

### 3. Activate the Local File Trigger

**Important:** Even if the workflow is active, the trigger node itself needs to be activated:

1. Open the "V3 Local Agentic RAG AI Agent" workflow
2. Find the "Local File Trigger" node
3. Click on it
4. Look for an "Activate" button or toggle
5. The trigger should show as "Active" or "Listening"

### 4. Verify Trigger Configuration

Check that the Local File Trigger is configured correctly:
- **Path:** `/data/shared`
- **Events:** `add`, `change` (both should be checked)
- **Options:** `usePolling: true` (should be enabled)

### 5. Test the Trigger

**Option A: Modify existing file**
```bash
# Append to test.txt
echo "New content" >> /Users/lxupkzwjs/Developer/local-ai-packaged/shared/test.txt
```

**Option B: Create new file**
```bash
# Create a new file
echo "Test content" > /Users/lxupkzwjs/Developer/local-ai-packaged/shared/test_new.txt
```

**Option C: Touch file to trigger change event**
```bash
touch /Users/lxupkzwjs/Developer/local-ai-packaged/shared/test.txt
```

### 6. Check n8n Executions

After triggering:
1. Go to n8n UI → "Executions" tab
2. You should see a new execution
3. If you see it, click to view details
4. Check for any errors in the execution

### 7. Check n8n Logs

```bash
# Watch n8n logs in real-time
docker logs -f n8n

# Or check recent logs
docker logs n8n --tail 100 | grep -i "trigger\|file\|error"
```

## Common Issues

### Issue 1: Workflow Not Imported

**Solution:**
```bash
# Manually import the workflow
docker exec n8n n8n import:workflow --input=/backup/workflows/V3_Local_Agentic_RAG_AI_Agent.json
```

### Issue 2: Workflow Not Active

**Solution:**
- Open workflow in n8n UI
- Toggle the "Active" switch to ON

### Issue 3: Trigger Not Active

**Solution:**
- Open the workflow
- Click on "Local File Trigger" node
- Activate the trigger (there may be a button or toggle)

### Issue 4: Polling Not Working

**Solution:**
- Check that `usePolling: true` is set in trigger options
- Try restarting n8n:
  ```bash
  docker restart n8n
  ```

### Issue 5: File Permissions

**Solution:**
```bash
# Ensure files are readable
chmod 644 /Users/lxupkzwjs/Developer/local-ai-packaged/shared/*
```

## Manual Workflow Execution

If the trigger still doesn't work, you can manually execute the workflow:

1. Open the workflow in n8n
2. Click "Execute Workflow" button
3. Provide test data:
   ```json
   {
     "path": "/data/shared/test.txt"
   }
   ```

## Next Steps

1. **Check n8n UI** - Verify workflow exists and is active
2. **Activate trigger** - Ensure Local File Trigger is activated
3. **Test with new file** - Create a new file to trigger "add" event
4. **Check executions** - Monitor n8n executions tab
5. **Review logs** - Check n8n logs for errors

