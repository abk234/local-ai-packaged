# V3 Local Agentic RAG AI Agent - Complete Guide for Junior Developers

**Date Created:** 2025-11-07  
**Workflow Version:** V3  
**Purpose:** End-to-end guide for understanding, testing, and working with the Agentic RAG workflow

---

## 📋 Table of Contents

1. [What is This Workflow?](#what-is-this-workflow)
2. [High-Level Architecture](#high-level-architecture)
3. [Two Main Flows](#two-main-flows)
4. [Node-by-Node Breakdown](#node-by-node-breakdown)
5. [Data Flow Diagrams](#data-flow-diagrams)
6. [Prerequisites & Setup](#prerequisites--setup)
7. [Testing Guide](#testing-guide)
8. [Troubleshooting](#troubleshooting)
9. [Key Concepts Explained](#key-concepts-explained)

---

## What is This Workflow?

### Overview
The **V3 Local Agentic RAG AI Agent** is an intelligent document processing and question-answering system that:

1. **Automatically processes documents** you drop into a folder (PDFs, CSVs, Excel, text files)
2. **Stores them intelligently** in a vector database for fast semantic search
3. **Answers questions** about your documents using an AI agent that can:
   - Perform semantic search (RAG)
   - Query tabular data with SQL
   - Retrieve full documents when needed
   - Switch between tools intelligently based on the question

### Why "Agentic"?
Unlike simple RAG (which just searches and retrieves), this agent:
- **Reasons** about which tool to use
- **Self-improves** by trying different approaches if the first doesn't work
- **Handles multiple data types** (text, tables, structured data)
- **Maintains conversation context** across multiple questions

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    V3 Agentic RAG System                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐         ┌──────────────────┐        │
│  │  Document       │         │  Chat Interface    │        │
│  │  Processing     │         │  (Q&A System)     │        │
│  │  Flow           │         │                   │        │
│  └──────────────────┘         └──────────────────┘        │
│           │                           │                    │
│           │                           │                    │
│           ▼                           ▼                    │
│  ┌──────────────────────────────────────────────┐          │
│  │         PostgreSQL + pgvector                │          │
│  │  (Vector embeddings + metadata + tabular)     │          │
│  └──────────────────────────────────────────────┘          │
│           │                           │                    │
│           └───────────┬───────────────┘                    │
│                       ▼                                    │
│              ┌──────────────┐                             │
│              │  AI Agent    │                             │
│              │  (Ollama)    │                             │
│              └──────────────┘                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Two Main Flows

### Flow 1: Document Processing (Automatic)
**Trigger:** File added/changed in `/data/shared` folder

```
Local File Trigger
    ↓
Loop Over Items
    ↓
Set File ID (extract path, type, title)
    ↓
Delete Old Records (cleanup)
    ↓
Insert Document Metadata
    ↓
Read File from Disk
    ↓
Switch (by file type)
    ├─→ PDF → Extract PDF Text → Vector Store
    ├─→ Excel → Extract Excel → Aggregate → Store Rows + Vector Store
    ├─→ CSV → Extract CSV → Aggregate → Store Rows + Vector Store
    └─→ Text → Extract Text → Vector Store
```

### Flow 2: Chat Interface (Interactive)
**Trigger:** User sends a chat message

```
When Chat Message Received
    ↓
Edit Fields (extract chatInput, sessionId)
    ↓
RAG AI Agent (with tools)
    ├─→ Postgres PGVector Store (RAG search)
    ├─→ List Documents (tool)
    ├─→ Get File Contents (tool)
    └─→ Query Document Rows (SQL tool)
    ↓
Respond to Webhook (send answer)
```

---

## Node-by-Node Breakdown

### 🔵 Document Processing Flow Nodes

#### 1. **Local File Trigger**
- **Type:** `n8n-nodes-base.localFileTrigger`
- **What it does:** Watches `/data/shared` folder for new/changed files
- **Configuration:**
  - Path: `/data/shared`
  - Events: `add`, `change`
  - Uses polling to detect changes
- **Output:** File path information

#### 2. **Loop Over Items**
- **Type:** `n8n-nodes-base.splitInBatches`
- **What it does:** Processes multiple files one at a time
- **Why:** Ensures each file is fully processed before moving to the next

#### 3. **Set File ID**
- **Type:** `n8n-nodes-base.set`
- **What it does:** Extracts file information:
  - `file_id`: Full file path (e.g., `/data/shared/document.pdf`)
  - `file_type`: Extension (pdf, xlsx, csv, txt)
  - `file_title`: Filename without extension
- **Example Output:**
  ```json
  {
    "file_id": "/data/shared/sales_report.pdf",
    "file_type": "pdf",
    "file_title": "sales_report"
  }
  ```

#### 4. **Delete Old Doc Records**
- **Type:** `n8n-nodes-base.postgres`
- **What it does:** Removes old vector embeddings for this file (if re-uploaded)
- **SQL:** Deletes from `documents_pg` table where `file_id` matches

#### 5. **Delete Old Data Records**
- **Type:** `n8n-nodes-base.postgres`
- **What it does:** Removes old tabular data rows for this file
- **SQL:** Deletes from `document_rows` table

#### 6. **Insert Document Metadata**
- **Type:** `n8n-nodes-base.postgres`
- **What it does:** Stores file metadata in `document_metadata` table
- **Stores:** `id` (file path), `title`, `created_at`

#### 7. **Read/Write Files from Disk**
- **Type:** `n8n-nodes-base.readWriteFile`
- **What it does:** Reads the actual file content from disk
- **Output:** File binary/data

#### 8. **Switch**
- **Type:** `n8n-nodes-base.switch`
- **What it does:** Routes to different extractors based on file type
- **Routes:**
  - `pdf` → Extract PDF Text
  - `xlsx` → Extract from Excel
  - `csv` → Extract from CSV
  - `txt` → Extract Document Text (default)

#### 9. **Extract PDF Text**
- **Type:** `n8n-nodes-base.extractFromFile`
- **What it does:** Extracts text content from PDF files
- **Output:** Plain text from PDF

#### 10. **Extract from Excel**
- **Type:** `n8n-nodes-base.extractFromFile`
- **What it does:** Extracts data from Excel files
- **Output:** Array of rows (each row is an object with column names as keys)

#### 11. **Extract from CSV**
- **Type:** `n8n-nodes-base.extractFromFile`
- **What it does:** Extracts data from CSV files
- **Output:** Array of rows (similar to Excel)

#### 12. **Aggregate** (for Excel/CSV)
- **Type:** `n8n-nodes-base.aggregate`
- **What it does:** Combines all rows into a single data structure
- **Why:** Needed for processing multiple rows together

#### 13. **Summarize** (for Excel/CSV)
- **Type:** `n8n-nodes-base.summarize`
- **What it does:** Concatenates all row data into a single string
- **Output:** JSON string of all data

#### 14. **Set Schema** (for Excel/CSV)
- **Type:** `n8n-nodes-base.set`
- **What it does:** Extracts column names (schema) from the file
- **Stores:** 
  - `schema`: Column names as JSON string
  - `data`: All row data as JSON string

#### 15. **Insert Table Rows** (for Excel/CSV)
- **Type:** `n8n-nodes-base.postgres`
- **What it does:** Stores each row in `document_rows` table as JSONB
- **Structure:**
  ```sql
  INSERT INTO document_rows (dataset_id, row_data)
  VALUES ('/data/shared/file.csv', '{"column1": "value1", ...}'::jsonb)
  ```

#### 16. **Update Schema for Document Metadata** (for Excel/CSV)
- **Type:** `n8n-nodes-base.postgres`
- **What it does:** Updates `document_metadata` table with the file's schema
- **Why:** So the AI knows what columns are available for SQL queries

#### 17. **Extract Document Text** (for TXT files)
- **Type:** `n8n-nodes-base.extractFromFile`
- **What it does:** Extracts text from plain text files
- **Output:** Plain text content

#### 18. **Default Data Loader**
- **Type:** `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- **What it does:** Converts extracted text into LangChain document format
- **Adds metadata:** `file_id`, `file_title`
- **Output:** LangChain document objects

#### 19. **Recursive Character Text Splitter**
- **Type:** `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- **What it does:** Splits long documents into smaller chunks (400 characters)
- **Why:** Vector databases work better with smaller, focused chunks
- **Output:** Array of document chunks

#### 20. **Embeddings Ollama**
- **Type:** `@n8n/n8n-nodes-langchain.embeddingsOllama`
- **What it does:** Converts text chunks into vector embeddings
- **Model:** `nomic-embed-text:latest`
- **Output:** Vector embeddings (arrays of numbers)

#### 21. **Postgres PGVector Store** (Insert Mode)
- **Type:** `@n8n/n8n-nodes-langchain.vectorStorePGVector`
- **What it does:** Stores vector embeddings in PostgreSQL with pgvector extension
- **Table:** `documents_pg`
- **Stores:** Text chunks + embeddings + metadata

---

### 🟢 Chat Interface Flow Nodes

#### 22. **When Chat Message Received**
- **Type:** `@n8n/n8n-nodes-langchain.chatTrigger`
- **What it does:** Triggers when user sends a message via the chat interface
- **Input:** User's question/message
- **Output:** Chat message data

#### 23. **Webhook** (Alternative Entry)
- **Type:** `n8n-nodes-base.webhook`
- **What it does:** Allows external systems to send questions via HTTP POST
- **Path:** `/bf4dd093-bb02-472c-9454-7ab9af97bd1d`
- **Use case:** API integration

#### 24. **Edit Fields**
- **Type:** `n8n-nodes-base.set`
- **What it does:** Extracts and normalizes input data
- **Extracts:**
  - `chatInput`: The user's question
  - `sessionId`: Conversation session ID (for memory)

#### 25. **Postgres Chat Memory**
- **Type:** `@n8n/n8n-nodes-langchain.memoryPostgresChat`
- **What it does:** Stores conversation history in PostgreSQL
- **Why:** Allows the agent to remember previous messages in the conversation
- **Table:** Created automatically by LangChain

#### 26. **Ollama (Change Base URL)**
- **Type:** `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- **What it does:** LLM for the AI agent (uses OpenAI-compatible API)
- **Model:** `qwen2.5:14b-8k`
- **Base URL:** `http://ollama:11434/v1` (local Ollama instance)
- **Note:** Uses OpenAI node type but points to Ollama (n8n limitation)

#### 27. **RAG AI Agent**
- **Type:** `@n8n/n8n-nodes-langchain.agent`
- **What it does:** The "brain" that coordinates all tools
- **System Prompt:** Instructs agent to:
  - Start with RAG search
  - Use SQL for numerical queries
  - Retrieve full documents when needed
  - Be honest if answer not found
- **Tools Available:**
  1. **Postgres PGVector Store1** (RAG search)
  2. **List Documents** (see available files)
  3. **Get File Contents** (retrieve full document text)
  4. **Query Document Rows** (SQL queries on tabular data)

#### 28. **Postgres PGVector Store1** (Retrieve Mode)
- **Type:** `@n8n/n8n-nodes-langchain.vectorStorePGVector`
- **What it does:** Performs semantic search on stored documents
- **Mode:** `retrieve-as-tool`
- **How it works:**
  1. Converts user question to embedding
  2. Searches for similar document chunks
  3. Returns top matching chunks with context

#### 29. **List Documents** (Tool)
- **Type:** `n8n-nodes-base.postgresTool`
- **What it does:** Returns all available documents from `document_metadata`
- **Use case:** When user asks "what documents do you have?"

#### 30. **Get File Contents** (Tool)
- **Type:** `n8n-nodes-base.postgresTool`
- **What it does:** Retrieves full text of a specific document
- **SQL:** Aggregates all chunks for a given `file_id`
- **Use case:** When RAG chunks aren't enough, get full document

#### 31. **Query Document Rows** (Tool)
- **Type:** `n8n-nodes-base.postgresTool`
- **What it does:** Executes SQL queries on tabular data (CSV/Excel)
- **Example Queries:**
  ```sql
  -- Average revenue
  SELECT AVG((row_data->>'revenue')::numeric)
  FROM document_rows
  WHERE dataset_id = '/data/shared/sales.csv';
  
  -- Group by category
  SELECT 
    row_data->>'category' as category,
    SUM((row_data->>'sales')::numeric) as total_sales
  FROM document_rows
  WHERE dataset_id = '/data/shared/products.csv'
  GROUP BY row_data->>'category';
  ```

#### 32. **Embeddings Ollama1**
- **Type:** `@n8n/n8n-nodes-langchain.embeddingsOllama`
- **What it does:** Converts user questions to embeddings for RAG search
- **Model:** `nomic-embed-text:latest`
- **Connected to:** Postgres PGVector Store1

#### 33. **Respond to Webhook**
- **Type:** `n8n-nodes-base.respondToWebhook`
- **What it does:** Sends the AI agent's response back to the user
- **Output:** JSON with the answer

---

### 🟡 Setup Nodes (Run Once)

#### 34. **Create Document Metadata Table**
- **Type:** `n8n-nodes-base.postgres`
- **What it does:** Creates `document_metadata` table
- **Schema:**
  ```sql
  CREATE TABLE document_metadata (
    id TEXT PRIMARY KEY,
    title TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    schema TEXT
  );
  ```
- **Run:** Once during initial setup

#### 35. **Create Document Rows Table**
- **Type:** `n8n-nodes-base.postgres`
- **What it does:** Creates `document_rows` table for tabular data
- **Schema:**
  ```sql
  CREATE TABLE document_rows (
    id SERIAL PRIMARY KEY,
    dataset_id TEXT REFERENCES document_metadata(id),
    row_data JSONB
  );
  ```
- **Run:** Once during initial setup

---

## Data Flow Diagrams

### Document Processing Flow (Detailed)

```
┌─────────────────────┐
│ Local File Trigger  │  Detects: /data/shared/new_file.pdf
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Loop Over Items     │  Process one file at a time
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Set File ID         │  Extract: file_id, file_type, file_title
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Delete Old Records  │  Clean up previous version
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Insert Metadata     │  Store in document_metadata table
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Read File           │  Load file from disk
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Switch              │  Route by file type
└──────────┬──────────┘
           │
    ┌──────┴──────┬──────────┬──────────┐
    │            │          │          │
    ▼            ▼          ▼          ▼
┌────────┐  ┌────────┐ ┌────────┐ ┌────────┐
│Extract │  │Extract │ │Extract │ │Extract │
│PDF     │  │Excel   │ │CSV     │ │Text    │
└───┬────┘  └───┬────┘ └───┬────┘ └───┬────┘
    │           │          │          │
    │      ┌────┴────┐     │          │
    │      │Aggregate│     │          │
    │      └────┬────┘     │          │
    │           │          │          │
    │      ┌────┴────┐     │          │
    │      │Summarize│     │          │
    │      └────┬────┘     │          │
    │           │          │          │
    │      ┌────┴────┐     │          │
    │      │Set Schema│    │          │
    │      └────┬────┘     │          │
    │           │          │          │
    │      ┌────┴────┐     │          │
    │      │Insert   │     │          │
    │      │Rows     │     │          │
    │      └────┬────┘     │          │
    │           │          │          │
    └──────────┴──────────┴──────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Default Loader  │  Convert to LangChain format
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Text Splitter   │  Split into 400-char chunks
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Embeddings      │  Convert to vectors
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Vector Store    │  Store in PostgreSQL
        └─────────────────┘
```

### Chat Flow (Detailed)

```
┌──────────────────────────┐
│ User: "What's the total  │
│ revenue for Q1?"         │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Chat Trigger / Webhook    │  Receives question
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ Edit Fields              │  Extract: chatInput, sessionId
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│ RAG AI Agent             │  Decides which tool to use
└──────────┬───────────────┘
           │
    ┌──────┴──────┬──────────┬──────────┐
    │             │          │          │
    ▼             ▼          ▼          ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│Vector    │ │List     │ │Get File │ │Query    │
│Store     │ │Docs     │ │Contents │ │Rows     │
│(RAG)     │ │         │ │         │ │(SQL)    │
└────┬─────┘ └────┬────┘ └────┬────┘ └────┬────┘
     │            │           │           │
     └────────────┴───────────┴───────────┘
                    │
                    ▼
         ┌──────────────────┐
         │ Agent Processes  │  Combines results
         │ Results          │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Respond to       │  "The total revenue
         │ Webhook          │   for Q1 is $50,000"
         └──────────────────┘
```

---

## Prerequisites & Setup

### 1. Required Services Running

```bash
# Check all services are running
cd /Users/lxupkzwjs/Developer/local-ai-packaged
./check_services.py
```

**Required:**
- ✅ PostgreSQL (Supabase) - for vector storage and metadata
- ✅ Ollama - for LLM and embeddings
- ✅ n8n - workflow engine

### 2. Required Models in Ollama

```bash
# Check if models are pulled
docker exec ollama ollama list

# If missing, pull them:
docker exec ollama ollama pull qwen2.5:14b-8k
docker exec ollama ollama pull nomic-embed-text
```

### 3. Database Tables Setup

**Run these nodes once in n8n:**
1. **Create Document Metadata Table** - Creates `document_metadata` table
2. **Create Document Rows Table** - Creates `document_rows` table

**How to run:**
- Open the workflow in n8n
- Click on each node
- Click "Execute Node" button
- Verify success (green checkmark)

### 4. Required Credentials in n8n

**Postgres Account:**
- **Name:** "Postgres account"
- **Host:** `db` (Docker service name)
- **Port:** `5432`
- **Database:** `postgres`
- **User:** `postgres`
- **Password:** From your `.env` file (`POSTGRES_PASSWORD`)

**Ollama Account (for Embeddings):**
- **Name:** "Ollama account"
- **Base URL:** `http://ollama:11434`

**OpenAI Account (for LLM - actually Ollama):**
- **Name:** "OpenAi account"
- **Base URL:** `http://ollama:11434/v1`
- **API Key:** Can be anything (not used for local Ollama)

### 5. Verify Shared Folder

```bash
# Check the shared folder exists and is accessible
ls -la /Users/lxupkzwjs/Developer/local-ai-packaged/shared/

# Test from inside n8n container
docker exec n8n ls -la /data/shared
```

---

## Testing Guide

### Test 1: Setup Verification

**Step 1:** Verify tables exist
```sql
-- Connect to PostgreSQL
docker exec -it supabase-db psql -U postgres

-- Check tables
\dt

-- Should see:
-- - document_metadata
-- - document_rows
-- - documents_pg (created by LangChain)
```

**Step 2:** Verify workflow is active
- Open n8n UI: http://localhost:6678
- Go to Workflows
- Find "V3 Local Agentic RAG AI Agent"
- Should show "Active" status

### Test 2: Document Processing

**Step 1:** Create a test text file
```bash
echo "This is a test document about artificial intelligence and machine learning." > /Users/lxupkzwjs/Developer/local-ai-packaged/shared/test_doc.txt
```

**Step 2:** Watch n8n workflow execution
- Go to n8n UI
- Click on "Executions" tab
- You should see a new execution triggered by "Local File Trigger"
- Click on it to see the flow

**Step 3:** Verify data was stored
```sql
-- Check metadata
SELECT * FROM document_metadata;

-- Check vector embeddings
SELECT COUNT(*) FROM documents_pg;

-- Should see your document stored
```

### Test 3: CSV File Processing

**Step 1:** Create a test CSV
```bash
cat > /Users/lxupkzwjs/Developer/local-ai-packaged/shared/sales.csv << EOF
date,product,revenue,quantity
2024-01-01,Widget A,1000,10
2024-01-02,Widget B,2000,20
2024-01-03,Widget A,1500,15
EOF
```

**Step 2:** Verify processing
- Check n8n execution
- Verify `document_metadata` has the CSV with schema
- Verify `document_rows` has the rows stored as JSONB

**Step 3:** Query the data
```sql
-- Check metadata
SELECT id, title, schema FROM document_metadata WHERE id LIKE '%sales.csv';

-- Check rows
SELECT dataset_id, row_data FROM document_rows LIMIT 5;
```

### Test 4: Chat Interface

**Step 1:** Access the chat interface
- In n8n, go to the workflow
- Find "When chat message received" node
- Click on it
- You'll see a chat interface or webhook URL

**Step 2:** Ask a question
- Type: "What documents do you have?"
- The agent should use "List Documents" tool
- Should return list of files

**Step 3:** Test RAG search
- Type: "What does the test document say about AI?"
- Agent should:
  1. Use RAG search (Vector Store)
  2. Find relevant chunks
  3. Generate answer

**Step 4:** Test SQL query
- Type: "What's the total revenue in the sales CSV?"
- Agent should:
  1. Recognize this needs SQL
  2. Use "Query Document Rows" tool
  3. Execute: `SELECT SUM((row_data->>'revenue')::numeric) FROM document_rows WHERE dataset_id = '/data/shared/sales.csv'`
  4. Return the sum

### Test 5: Full Document Retrieval

**Step 1:** Upload a longer document
```bash
# Create a multi-paragraph document
cat > /Users/lxupkzwjs/Developer/local-ai-packaged/shared/long_doc.txt << EOF
Paragraph 1: Introduction to the topic.
Paragraph 2: Main discussion points.
Paragraph 3: Detailed analysis.
Paragraph 4: Conclusions and recommendations.
EOF
```

**Step 2:** Ask a question requiring full context
- Type: "Get me the full text of long_doc.txt"
- Agent should use "Get File Contents" tool
- Should return the complete document text

---

## Troubleshooting

### Issue 1: "Credential does not exist"

**Error:** `Credential with ID 'xxx' does not exist for type 'ollamaApi'`

**Solution:**
1. Go to n8n → Credentials
2. Create missing credentials:
   - **Ollama API:** Base URL = `http://ollama:11434`
   - **Postgres:** Use Docker service name `db` as host
   - **OpenAI:** Base URL = `http://ollama:11434/v1`
3. Re-assign credentials to nodes in workflow

### Issue 2: "Table does not exist"

**Error:** `relation "document_metadata" does not exist`

**Solution:**
1. Run the setup nodes:
   - "Create Document Metadata Table"
   - "Create Document Rows Table"
2. Verify with:
   ```sql
   \dt
   ```

### Issue 3: "Model not found" in Ollama

**Error:** `model 'qwen2.5:14b-8k' not found`

**Solution:**
```bash
# Pull the required models
docker exec ollama ollama pull qwen2.5:14b-8k
docker exec ollama ollama pull nomic-embed-text
```

### Issue 4: Files not triggering workflow

**Symptoms:** File added to `/data/shared` but workflow doesn't run

**Solution:**
1. Check Local File Trigger is active
2. Verify path is `/data/shared` (inside container)
3. Check file permissions:
   ```bash
   chmod 644 /Users/lxupkzwjs/Developer/local-ai-packaged/shared/*
   ```
4. Check n8n container can access:
   ```bash
   docker exec n8n ls -la /data/shared
   ```

### Issue 5: Vector search returns no results

**Symptoms:** RAG search finds nothing even though documents are stored

**Solution:**
1. Verify embeddings were created:
   ```sql
   SELECT COUNT(*) FROM documents_pg;
   ```
2. Check embedding model matches:
   - Storage: `nomic-embed-text`
   - Search: `nomic-embed-text`
3. Verify text was actually stored:
   ```sql
   SELECT content FROM documents_pg LIMIT 1;
   ```

### Issue 6: SQL queries fail on tabular data

**Symptoms:** "Query Document Rows" tool returns errors

**Solution:**
1. Verify schema was stored:
   ```sql
   SELECT schema FROM document_metadata WHERE id LIKE '%your_file.csv';
   ```
2. Check row_data structure:
   ```sql
   SELECT row_data FROM document_rows LIMIT 1;
   ```
3. Ensure SQL uses correct JSONB syntax:
   ```sql
   -- Correct
   row_data->>'column_name'
   
   -- Wrong
   row_data->column_name
   ```

### Issue 7: Agent doesn't use the right tool

**Symptoms:** Agent uses RAG when it should use SQL, or vice versa

**Solution:**
1. Improve the system prompt in "RAG AI Agent" node
2. Be more explicit in your question:
   - "Calculate the sum of..." → Triggers SQL
   - "What does the document say about..." → Triggers RAG
3. Check tool descriptions are clear in each tool node

---

## Key Concepts Explained

### What is RAG?
**Retrieval Augmented Generation:**
1. Convert documents to vector embeddings
2. Store in vector database
3. When user asks question:
   - Convert question to embedding
   - Find similar document chunks
   - Use those chunks as context for LLM
   - Generate answer with context

### What is pgvector?
**PostgreSQL extension for vector similarity search:**
- Stores vectors as a new data type
- Enables fast similarity search using cosine distance
- Allows SQL queries combined with vector search

### What is JSONB?
**Binary JSON in PostgreSQL:**
- Stores structured data (like CSV rows) as JSON
- Allows querying with SQL operators (`->`, `->>`)
- More flexible than creating separate tables for each CSV

### What is an Embedding?
**Numerical representation of text:**
- Converts words/sentences to arrays of numbers
- Similar text → Similar numbers
- Enables semantic search (meaning-based, not keyword-based)

### What is an AI Agent?
**LLM that can use tools:**
- Receives user question
- Decides which tool(s) to use
- Executes tools
- Combines results
- Generates final answer
- Can try multiple approaches if first fails

### What is Text Chunking?
**Splitting long documents into smaller pieces:**
- Vector databases work better with focused chunks
- 400 characters is a good balance
- Preserves context while enabling precise retrieval

---

## Next Steps for Development

1. **Customize System Prompt:** Edit the prompt in "RAG AI Agent" node for your use case
2. **Add More Tools:** Create additional Postgres tools for specific queries
3. **Improve Chunking:** Adjust chunk size based on your documents
4. **Add Metadata:** Store additional metadata (tags, categories, etc.)
5. **Optimize Queries:** Add indexes to PostgreSQL for faster searches
6. **Add Authentication:** Secure the webhook endpoint
7. **Monitor Performance:** Track which tools are used most often

---

## Quick Reference

### Important Paths
- **Local shared folder:** `/Users/lxupkzwjs/Developer/local-ai-packaged/shared`
- **Container shared folder:** `/data/shared`
- **n8n UI:** http://localhost:6678

### Important Tables
- `document_metadata` - File information
- `document_rows` - Tabular data (CSV/Excel rows)
- `documents_pg` - Vector embeddings (created by LangChain)

### Important Models
- `qwen2.5:14b-8k` - LLM for agent
- `nomic-embed-text` - Embeddings model

### Important Credentials
- **Postgres account** - Database connection
- **Ollama account** - Embeddings
- **OpenAi account** - LLM (points to Ollama)

---

**End of Guide**

