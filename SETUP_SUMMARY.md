# Setup Summary

## What I've Created for You

### 1. **setup_env.py** - Environment Setup Script
   - Checks for port conflicts automatically
   - Generates secure random values for all required environment variables
   - Preserves existing `.env` values (won't overwrite unless you use `--force`)
   - Provides suggestions for alternative ports when conflicts are detected

### 2. **docker-compose.override.local.yml** - Custom Port Mappings
   - Pre-configured with alternative ports to avoid conflicts
   - Maps conflicting ports to available alternatives
   - Can be used alongside the standard override files

### 3. **start_services_local.py** - Helper Script for Custom Ports
   - Wrapper around `start_services.py` that includes the local override
   - Automatically uses custom port mappings
   - Same interface as the original script

### 4. **SETUP_GUIDE.md** - Comprehensive Setup Documentation
   - Detailed port mapping reference
   - Troubleshooting guide
   - Step-by-step instructions

## Current Port Conflicts Detected

Based on your system, these ports are already in use:

| Service | Default Port | Alternative Port |
|---------|--------------|-----------------|
| n8n | 5678 | **6678** |
| Langfuse Web | 3000 | **4000** |
| Langfuse Worker | 3030 | **4030** |
| ClickHouse | 8123 | **9123** |
| ClickHouse | 9000 | **10000** |
| Postgres | 5433 | **6433** |
| Redis | 6379 | **7379** |
| Ollama | 11434 | **12434** |

## Quick Start Options

### Option 1: Use Custom Ports (Recommended - No Conflicts)

```bash
# 1. Check your environment (optional - your .env already exists)
python3 setup_env.py

# 2. Start services with custom ports
python3 start_services_local.py --profile cpu
```

### Option 2: Stop Conflicting Services First

If you want to use the default ports, stop the conflicting services:

```bash
# Find what's using the ports
lsof -i -P | grep LISTEN | grep -E "(5678|3000|3030|8123|9000|5433|6379|11434)"

# Stop those services, then use the standard script
python3 start_services.py --profile cpu
```

### Option 3: Manual Docker Compose

If you prefer manual control:

```bash
# Start Supabase
docker compose -p localai -f supabase/docker/docker-compose.yml up -d

# Wait a bit
sleep 10

# Start local AI services with custom ports
docker compose \
  -p localai \
  --profile cpu \
  -f docker-compose.yml \
  -f docker-compose.override.private.yml \
  -f docker-compose.override.local.yml \
  up -d
```

## Environment Variables

Your `.env` file already exists. The setup script detected it and preserved it.

**If you need to regenerate secrets** (not recommended unless necessary):
```bash
python3 setup_env.py --force
```

**Required variables** (should already be in your `.env`):
- N8N_ENCRYPTION_KEY
- N8N_USER_MANAGEMENT_JWT_SECRET
- POSTGRES_PASSWORD
- JWT_SECRET
- ANON_KEY
- SERVICE_ROLE_KEY
- DASHBOARD_USERNAME
- DASHBOARD_PASSWORD
- POOLER_TENANT_ID
- POOLER_DB_POOL_SIZE
- NEO4J_AUTH
- CLICKHOUSE_PASSWORD
- MINIO_ROOT_PASSWORD
- LANGFUSE_SALT
- NEXTAUTH_SECRET
- ENCRYPTION_KEY
- FLOWISE_USERNAME
- FLOWISE_PASSWORD

## Service URLs (with Custom Ports)

After starting with `start_services_local.py`:

- **n8n**: http://localhost:6678
- **Open WebUI**: http://localhost:8080
- **Flowise**: http://localhost:3001
- **Langfuse**: http://localhost:4000
- **Qdrant Dashboard**: http://localhost:7333
- **Neo4j Browser**: http://localhost:7474
- **SearXNG**: http://localhost:8081
- **Ollama API**: http://localhost:12434

## Important Notes

1. **Internal Communication**: Services communicate using Docker container names (e.g., `ollama:11434`, `db:5432`), so custom host ports don't affect internal communication.

2. **n8n Configuration**: When setting up Ollama credentials in n8n, use:
   - Internal: `http://ollama:11434` (for workflows)
   - External: `http://localhost:12434` (if accessing from host)

3. **Postgres Connection**: Use host `db` (not `localhost`) when connecting from n8n or other services.

4. **Port Conflicts**: The custom ports are chosen to avoid conflicts, but if you have other services using those ports too, you can edit `docker-compose.override.local.yml` to use different ports.

## Next Steps

1. **Start the services**:
   ```bash
   python3 start_services_local.py --profile cpu
   ```

2. **Wait for services to initialize** (may take a few minutes for first run)

3. **Access n8n** at http://localhost:6678 and set up your account

4. **Configure credentials** in n8n for:
   - Ollama: `http://ollama:11434`
   - Postgres: Host `db`, use credentials from `.env`
   - Qdrant: `http://qdrant:6333`

5. **Set up Open WebUI** at http://localhost:8080

6. **Import workflows** from `n8n/backup/workflows/`

## Troubleshooting

See `SETUP_GUIDE.md` for detailed troubleshooting steps.

Common issues:
- **Port still in use**: Edit `docker-compose.override.local.yml` to use different ports
- **Services not starting**: Check logs with `docker compose -p localai logs`
- **Supabase issues**: Ensure `POSTGRES_PASSWORD` doesn't contain `@` character

