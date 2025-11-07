# Fix n8n Ollama Connection - "Unauthorized" Error

## Problem
The n8n workflow is getting an "unauthorized" error when trying to connect to Ollama. This is because the workflow references credentials that don't exist in your n8n instance.

## Solution

### Step 1: Create Ollama Credentials in n8n

1. Open n8n at http://localhost:6678
2. Go to **Credentials** (click on your profile icon → Credentials, or navigate to `/home/credentials`)
3. Click **Add Credential**
4. Search for **"Ollama"** and select **"Ollama API"**
5. Configure the credential:
   - **Name**: `Ollama account` (or any name you prefer)
   - **Base URL**: `http://ollama:11434` ⚠️ **IMPORTANT: Use the container name, not localhost!**
   - **API Key**: Leave empty (Ollama doesn't require authentication for local instances)

6. Click **Save**

### Step 2: Update Your Workflow

1. Open your workflow in n8n
2. For each Ollama node (Chat Model, Model, Embeddings):
   - Click on the node
   - In the **Credentials** section, select the Ollama credential you just created
   - Save the node

### Step 3: Verify Connection

1. Test the connection by clicking on an Ollama node
2. Click **Test** or **Execute Node**
3. You should see the models available: `qwen2.5:7b-instruct-q4_K_M` and `nomic-embed-text`

## Important Notes

### Internal vs External URLs

- **Inside Docker containers** (n8n → Ollama): Use `http://ollama:11434`
- **From your host machine**: Use `http://localhost:12434`

The port mapping `12434:11434` is only for external access. Inside the Docker network, containers communicate using service names and internal ports.

### Why This Happens

When workflows are imported, they reference credential IDs that don't exist in your n8n instance. You need to:
1. Create the credentials manually
2. Re-assign them to the workflow nodes

## Quick Test

You can verify network connectivity from the n8n container:

```bash
docker exec n8n wget -qO- http://ollama:11434/api/tags
```

This should return a JSON list of available models.

## Troubleshooting

### Still Getting "Unauthorized"?

1. **Check the URL**: Make sure it's `http://ollama:11434` (not `localhost:12434`)
2. **Check Ollama is running**: `docker ps | grep ollama`
3. **Check network**: Both containers should be on the same network (`localai_default`)
4. **Check logs**: `docker logs n8n | grep -i ollama`

### Connection Refused?

- Verify Ollama container is running: `docker ps | grep ollama`
- Check if containers are on the same network: `docker network inspect localai_default`

### Models Not Found?

- Verify models are downloaded: `docker exec ollama ollama list`
- If models are missing, pull them: `docker exec ollama ollama pull qwen2.5:7b-instruct-q4_K_M`

