# Testing the V3 Workflow - Step by Step

## Current Status

✅ **Setup Tables Exist:**
- `document_metadata` - ✅ Created (empty)
- `document_rows` - ✅ Created

❌ **Vector Table:**
- `documents_pg` - ❌ Not created yet (will be auto-created by LangChain)

## Why `documents_pg` Doesn't Exist Yet

The `documents_pg` table is **automatically created by LangChain** when the vector store node first runs. It's not created by the setup nodes.

**It will be created when:**
1. A file is processed through the workflow
2. The "Postgres PGVector Store" node runs in "insert" mode
3. LangChain detects the table doesn't exist and creates it

## Quick Test to Create the Table

### Option 1: Trigger the Workflow Manually

1. **Check if workflow is active:**
   - Open n8n: http://localhost:6678
   - Go to Workflows
   - Find "V3 Local Agentic RAG AI Agent"
   - Ensure it's "Active"

2. **Trigger with existing file:**
   ```bash
   # Touch the file to trigger "change" event
   touch /Users/lxupkzwjs/Developer/local-ai-packaged/shared/test.txt
   ```

3. **Or add a new file:**
   ```bash
   echo "This is a test document about machine learning and artificial intelligence." > /Users/lxupkzwjs/Developer/local-ai-packaged/shared/test2.txt
   ```

4. **Watch the execution:**
   - Go to n8n → Executions
   - You should see a new execution
   - Click on it to see the flow
   - The "Postgres PGVector Store" node should create the table

### Option 2: Manually Create the Table (Not Recommended)

If you want to create it manually (though LangChain will recreate it with its own schema):

```sql
-- Enable pgvector extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the table (LangChain will use this or create its own)
CREATE TABLE IF NOT EXISTS documents_pg (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT,
  metadata JSONB,
  embedding vector(768)  -- nomic-embed-text uses 768 dimensions
);

-- Create index for similarity search
CREATE INDEX IF NOT EXISTS documents_pg_embedding_idx 
ON documents_pg 
USING ivfflat (embedding vector_cosine_ops);
```

**Note:** LangChain may still recreate this with its own schema, so it's better to let it create it automatically.

## Verification Steps

### 1. Check pgvector Extension
```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
```

### 2. Check Workflow Status
- Open n8n UI
- Verify workflow is active
- Check recent executions

### 3. Process a Test File
```bash
# Create a test file
cat > /Users/lxupkzwjs/Developer/local-ai-packaged/shared/test_doc.txt << EOF
This is a comprehensive document about artificial intelligence.
It covers machine learning, deep learning, and neural networks.
The document explains how AI systems work and their applications.
EOF
```

### 4. Verify Table Creation
```sql
-- Check if table exists
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name = 'documents_pg';

-- If it exists, check contents
SELECT COUNT(*) FROM documents_pg;
SELECT content, metadata FROM documents_pg LIMIT 1;
```

### 5. Check Document Metadata
```sql
-- Should see your processed file
SELECT * FROM document_metadata;
```

## Troubleshooting

### Issue: Workflow Not Triggering

**Check:**
1. Is the workflow active in n8n?
2. Is the Local File Trigger node configured correctly?
3. Can n8n access `/data/shared`?
   ```bash
   docker exec n8n ls -la /data/shared
   ```

### Issue: Table Still Not Created

**Check:**
1. Did the workflow execution complete successfully?
2. Check n8n execution logs for errors
3. Verify Postgres connection credentials in n8n
4. Check if pgvector extension is enabled

### Issue: Embeddings Not Working

**Check:**
1. Is Ollama running?
   ```bash
   docker ps | grep ollama
   ```
2. Is the embedding model available?
   ```bash
   docker exec ollama ollama list | grep nomic-embed-text
   ```
3. If missing, pull it:
   ```bash
   docker exec ollama ollama pull nomic-embed-text
   ```

## Expected Result After Processing

After processing a file, you should see:

1. **document_metadata table:**
   ```sql
   SELECT * FROM document_metadata;
   -- Should show your file with id, title, created_at
   ```

2. **documents_pg table:**
   ```sql
   SELECT COUNT(*) FROM documents_pg;
   -- Should show number of chunks (e.g., if 400-char chunks, a 1000-char doc = 3 chunks)
   
   SELECT content, metadata FROM documents_pg LIMIT 1;
   -- Should show text chunks with file_id in metadata
   ```

3. **n8n Execution:**
   - Green checkmarks on all nodes
   - No errors in execution log

## Next Steps

Once `documents_pg` is created and populated:

1. **Test the chat interface:**
   - Use "When chat message received" node in n8n
   - Ask: "What documents do you have?"
   - Ask: "What does the test document say about AI?"

2. **Test RAG search:**
   - Ask questions about the content
   - Verify the agent uses the vector store tool

3. **Test with CSV:**
   - Process the `sales.csv` file
   - Ask: "What's the total revenue in the sales data?"

