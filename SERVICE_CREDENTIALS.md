# Service Access Credentials & URLs

**Last Updated:** 2025-11-07  
**Status:** All 22 services running ✅

---

## 🔐 Quick Access Summary

| Service | URL | Credentials | Status |
|---------|-----|------------|--------|
| **n8n** | http://localhost:6678 | No login (or first-time setup) | ✅ Running |
| **Supabase Studio** | http://localhost:8000 | See Supabase section below | ✅ Running |
| **Open WebUI** | http://localhost:8080 | First-time signup | ✅ Running |
| **Flowise** | http://localhost:3001 | See Flowise section | ✅ Running |
| **Langfuse** | http://localhost:4000 | Default credentials | ✅ Running |
| **Qdrant** | http://localhost:7333 | No authentication | ✅ Running |
| **Neo4j** | http://localhost:7474 | See Neo4j section | ✅ Running |
| **SearXNG** | http://localhost:8081 | No authentication | ✅ Running |
| **MinIO** | http://localhost:9011 | See MinIO section | ✅ Running |

---

## 📋 Detailed Service Information

### 1. **n8n** (Workflow Automation)
- **URL:** http://localhost:6678
- **Alternative Port:** http://localhost:5678
- **Status:** ✅ Running
- **Credentials:** 
  - First-time access: Create account during initial setup
  - If already set up: Use your created credentials
- **Database:** Uses Supabase PostgreSQL
- **Note:** Workflows are auto-imported from `n8n/backup/workflows/`

---

### 2. **Supabase** (Database & Backend)
- **Studio URL:** http://localhost:8000
- **API URL:** http://localhost:8000/rest/v1/
- **Kong Gateway:** http://localhost:8000
- **Status:** ✅ All services running
- **Credentials:**
  - **Dashboard Username:** Check your `.env` file for `DASHBOARD_USERNAME`
  - **Dashboard Password:** Check your `.env` file for `DASHBOARD_PASSWORD`
  - **PostgreSQL:**
    - **Host:** `localhost` (or `db` from within Docker)
    - **Port:** `5432` (internal) or `5435` (pooler)
    - **Database:** `postgres`
    - **User:** `postgres`
    - **Password:** Check your `.env` file for `POSTGRES_PASSWORD`
  - **Service Role Key:** Check your `.env` file for `SERVICE_ROLE_KEY`
  - **Anon Key:** Check your `.env` file for `ANON_KEY`
- **Services:**
  - ✅ supabase-db (PostgreSQL)
  - ✅ supabase-kong (API Gateway)
  - ✅ supabase-auth (Authentication)
  - ✅ supabase-studio (Dashboard)
  - ✅ supabase-rest (REST API)
  - ✅ supabase-storage (File Storage)
  - ✅ supabase-meta (Metadata API)
  - ✅ supabase-realtime (Realtime)
  - ✅ supabase-analytics (Analytics) - Port 5000
  - ✅ supabase-vector (Vector/Embeddings)

---

### 3. **Open WebUI** (Chat Interface)
- **URL:** http://localhost:8080
- **Status:** ✅ Running
- **Credentials:**
  - First-time access: Create account during initial signup
  - No default credentials - you create your own
- **Features:**
  - Chat interface for Ollama models
  - Can integrate with n8n workflows
  - Supports multiple LLM providers

---

### 4. **Flowise** (AI Agent Builder)
- **URL:** http://localhost:3001
- **Status:** ✅ Running
- **Credentials:**
  - **Username:** Check your `.env` file for `FLOWISE_USERNAME`
  - **Password:** Check your `.env` file for `FLOWISE_PASSWORD`
- **Note:** If credentials are not set, Flowise may allow access without authentication

---

### 5. **Langfuse** (LLM Observability)
- **Web UI:** http://localhost:4000
- **Worker:** http://localhost:4030
- **Status:** ✅ Running
- **Credentials:**
  - **No default credentials** - Langfuse requires first-time account creation
  - **Action Required:** 
    1. Go to http://localhost:4000
    2. Click "Sign Up" or "Create Account"
    3. Enter your email and create a password
    4. This will be your admin account
- **Initialization:** 
  - Environment variables `LANGFUSE_INIT_USER_EMAIL`, `LANGFUSE_INIT_USER_NAME`, and `LANGFUSE_INIT_USER_PASSWORD` are not set
  - This means you need to create the account through the web UI
- **Database:** Uses ClickHouse and PostgreSQL
- **Note:** After creating your account, you'll have full admin access

---

### 6. **Qdrant** (Vector Database)
- **URL:** http://localhost:7333
- **API:** http://localhost:7333
- **Status:** ✅ Running
- **Credentials:** 
  - **No authentication required** (local setup)
  - API key can be configured but not required for local use
- **Alternative Ports:** 6333, 6334 (internal)

---

### 7. **Neo4j** (Graph Database)
- **Browser URL:** http://localhost:7474
- **Bolt URL:** bolt://localhost:7687
- **Status:** ✅ Running
- **Credentials:**
  - **Username:** `neo4j` (default)
  - **Password:** Check your `.env` file for `NEO4J_AUTH`
  - Format: `NEO4J_AUTH=neo4j/your_password`
  - If not set, default might be `neo4j/neo4j` (you'll be prompted to change)
- **Note:** First login requires password change if using default

---

### 8. **SearXNG** (Search Engine)
- **URL:** http://localhost:8081
- **Status:** ✅ Running
- **Credentials:** 
  - **No authentication required**
  - Public search interface
- **Features:** Privacy-focused metasearch engine

---

### 9. **MinIO** (S3-Compatible Storage)
- **Console URL:** http://localhost:9011
- **API URL:** http://localhost:9010
- **Status:** ✅ Running
- **Credentials:**
  - **Default Username:** `minioadmin`
  - **Default Password:** `minioadmin`
  - **Note:** Change these in production!
- **Access Key:** `minioadmin`
- **Secret Key:** `minioadmin`

---

### 10. **Ollama** (Local LLM)
- **API URL:** http://localhost:12434
- **Status:** ✅ Running
- **Credentials:** 
  - **No authentication required** (local setup)
- **Models Available:**
  - `qwen2.5:7b-instruct-q4_K_M`
  - `nomic-embed-text`
  - Check: `docker exec ollama ollama list`

---

### 11. **Redis/Valkey** (Cache)
- **URL:** redis://localhost:7379
- **Status:** ✅ Running
- **Credentials:** 
  - **No authentication** (local setup)
  - Password can be configured but not required

---

### 12. **ClickHouse** (Analytics Database)
- **HTTP Port:** http://localhost:9123
- **Native Port:** localhost:10000
- **Status:** ✅ Running
- **Credentials:**
  - **Default User:** `default`
  - **Default Password:** (empty/not set)
- **Note:** Used by Langfuse for analytics

---

### 13. **PostgreSQL** (Local AI Package)
- **Host:** localhost
- **Port:** 5433
- **Status:** ✅ Running
- **Credentials:**
  - **Database:** `postgres`
  - **User:** `postgres`
  - **Password:** Check your `.env` file for `POSTGRES_PASSWORD`
- **Note:** Separate from Supabase PostgreSQL

---

### 14. **Caddy** (Reverse Proxy)
- **HTTP:** http://localhost:80
- **HTTPS:** https://localhost:443
- **Status:** ✅ Running
- **Credentials:** 
  - Managed HTTPS/TLS
  - Configured via `Caddyfile`
- **Note:** Used for custom domain routing

---

## 🔍 How to Find Your Credentials

### Method 1: Check .env File
```bash
cd /Users/lxupkzwjs/Developer/local-ai-packaged
cat .env | grep -E "PASSWORD|USERNAME|AUTH|KEY"
```

### Method 2: Check Environment Variables in Containers
```bash
# Supabase credentials
docker exec supabase-db printenv | grep -E "POSTGRES_PASSWORD|DASHBOARD"

# Flowise credentials
docker exec flowise printenv | grep FLOWISE

# Neo4j credentials
docker exec localai-neo4j-1 printenv | grep NEO4J
```

### Method 3: Check Service Logs
```bash
# Check n8n for first-time setup
docker logs n8n | grep -i "user\|password\|setup"

# Check Langfuse for admin credentials
docker logs localai-langfuse-web-1 | grep -i "admin\|password"
```

---

## 🚀 Quick Access Commands

### Open Services in Browser
```bash
# n8n
open http://localhost:6678

# Supabase Studio
open http://localhost:8000

# Open WebUI
open http://localhost:8080

# Flowise
open http://localhost:3001

# Langfuse
open http://localhost:4000

# Qdrant
open http://localhost:7333

# Neo4j Browser
open http://localhost:7474

# SearXNG
open http://localhost:8081

# MinIO Console
open http://localhost:9011
```

### Check Service Status
```bash
cd /Users/lxupkzwjs/Developer/local-ai-packaged
./check_services.py
```

### View All Running Containers
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

## 📝 Important Notes

1. **First-Time Setup:**
   - Some services (n8n, Open WebUI, Langfuse) require initial account creation
   - Check service logs if you can't access them

2. **Default Credentials:**
   - Many services use default credentials for local development
   - **Change these in production!**

3. **Password Storage:**
   - All sensitive credentials are stored in `.env` file
   - Never commit `.env` to version control

4. **Service Health:**
   - All 22 services are currently running ✅
   - Use `./check_services.py` to verify status

5. **Port Conflicts:**
   - Custom ports are used to avoid conflicts
   - See `docker-compose.override.private.yml` for port mappings

---

## 🔒 Security Recommendations

1. **Change Default Passwords:**
   - MinIO: Change from `minioadmin/minioadmin`
   - Neo4j: Change default password
   - Any service with default credentials

2. **Environment Variables:**
   - Keep `.env` file secure
   - Use strong, unique passwords
   - Rotate credentials periodically

3. **Network Access:**
   - Most services are bound to `127.0.0.1` (localhost only)
   - Only accessible from your machine
   - Caddy handles external access if configured

---

## 🆘 Troubleshooting

### Can't Access a Service?

1. **Check if service is running:**
   ```bash
   docker ps | grep <service-name>
   ```

2. **Check service logs:**
   ```bash
   docker logs <service-name> --tail 50
   ```

3. **Verify port is accessible:**
   ```bash
   lsof -i :<port>
   ```

4. **Check health status:**
   ```bash
   ./check_services.py
   ```

### Forgot Credentials?

1. Check `.env` file
2. Check service logs for initialization
3. Reset by recreating the service (data may be lost)

---

**End of Document**

