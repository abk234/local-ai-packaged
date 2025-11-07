# Local Setup Guide

This guide will help you set up the Local AI Package on your machine without conflicting with existing Docker containers.

## Quick Start

1. **Run the setup script** to check for port conflicts and generate/update your `.env` file:
   ```bash
   python3 setup_env.py
   ```

2. **Review port conflicts** - The script will tell you which ports are already in use.

3. **Choose your approach**:
   - **Option A**: Stop conflicting services (recommended if you don't need them)
   - **Option B**: Use alternative ports (see below)

## Port Conflicts Resolution

### Current Port Mappings (Default)

| Service | Port(s) | Description |
|---------|---------|-------------|
| n8n | 5678 | Workflow automation platform |
| Flowise | 3001 | AI agent builder |
| Open WebUI | 8080 | Chat interface |
| Langfuse Web | 3000 | LLM observability UI |
| Langfuse Worker | 3030 | Background worker |
| Qdrant | 6333, 6334 | Vector database |
| Neo4j | 7473, 7474, 7687 | Graph database |
| ClickHouse | 8123, 9000, 9009 | Analytics database |
| MinIO | 9010, 9011 | S3-compatible storage |
| Postgres | 5433 | Database (Supabase) |
| Redis | 6379 | Cache/queue |
| SearXNG | 8081 | Search engine |
| Ollama | 11434 | LLM server |
| Caddy | 80, 443 | Reverse proxy |

### Using Alternative Ports

If you have port conflicts, you can use the custom override file:

```bash
# Use the custom port mappings
docker compose \
  -f docker-compose.yml \
  -f docker-compose.override.private.yml \
  -f docker-compose.override.local.yml \
  --profile cpu \
  up -d
```

Or modify `docker-compose.override.local.yml` to use your preferred ports.

### Alternative Port Mappings (Conflict-Free)

| Service | Original | Alternative |
|---------|----------|------------|
| n8n | 5678 | 6678 |
| Langfuse Web | 3000 | 4000 |
| Langfuse Worker | 3030 | 4030 |
| ClickHouse | 8123 | 9123 |
| ClickHouse | 9000 | 10000 |
| Postgres | 5433 | 6433 |
| Redis | 6379 | 7379 |
| Ollama | 11434 | 12434 |

## Environment Variables

### Required Variables

The setup script will generate these automatically:

**N8N Configuration:**
- `N8N_ENCRYPTION_KEY` - Encryption key for n8n
- `N8N_USER_MANAGEMENT_JWT_SECRET` - JWT secret for user management

**Supabase Secrets:**
- `POSTGRES_PASSWORD` - Database password
- `JWT_SECRET` - JWT signing secret
- `ANON_KEY` - Anonymous API key
- `SERVICE_ROLE_KEY` - Service role API key
- `DASHBOARD_USERNAME` - Dashboard username (default: admin)
- `DASHBOARD_PASSWORD` - Dashboard password
- `POOLER_TENANT_ID` - Connection pooler tenant ID
- `POOLER_DB_POOL_SIZE` - Connection pool size (default: 5)

**Neo4j:**
- `NEO4J_AUTH` - Authentication (format: `neo4j/password`)

**Langfuse:**
- `CLICKHOUSE_PASSWORD` - ClickHouse database password
- `MINIO_ROOT_PASSWORD` - MinIO root password
- `LANGFUSE_SALT` - Salt for hashing
- `NEXTAUTH_SECRET` - NextAuth.js secret
- `ENCRYPTION_KEY` - Encryption key

**Flowise:**
- `FLOWISE_USERNAME` - Admin username (default: admin)
- `FLOWISE_PASSWORD` - Admin password

### Optional Variables (for production)

Only set these if deploying to production with custom domains:

```bash
N8N_HOSTNAME=n8n.yourdomain.com
WEBUI_HOSTNAME=openwebui.yourdomain.com
FLOWISE_HOSTNAME=flowise.yourdomain.com
SUPABASE_HOSTNAME=supabase.yourdomain.com
OLLAMA_HOSTNAME=ollama.yourdomain.com
SEARXNG_HOSTNAME=searxng.yourdomain.com
NEO4J_HOSTNAME=neo4j.yourdomain.com
LANGFUSE_HOSTNAME=langfuse.yourdomain.com
LETSENCRYPT_EMAIL=your-email@example.com
```

## Starting Services

### Check for Port Conflicts First

```bash
python3 setup_env.py
```

### Start with Default Ports

```bash
python3 start_services.py --profile cpu
```

### Start with Custom Ports (if conflicts exist)

1. Edit `start_services.py` to include the local override, or run manually:

```bash
# Start Supabase
docker compose -p localai -f supabase/docker/docker-compose.yml up -d

# Wait a bit for Supabase to initialize
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

### GPU Support

If you have GPU support:

```bash
# NVIDIA GPU
python3 start_services.py --profile gpu-nvidia

# AMD GPU (Linux)
python3 start_services.py --profile gpu-amd
```

## Accessing Services

After starting, access services at:

| Service | Default URL | Alternative URL (if using local override) |
|---------|-------------|-------------------------------------------|
| n8n | http://localhost:5678 | http://localhost:6678 |
| Open WebUI | http://localhost:8080 | http://localhost:8080 |
| Flowise | http://localhost:3001 | http://localhost:3001 |
| Langfuse | http://localhost:3000 | http://localhost:4000 |
| Qdrant | http://localhost:6333 | http://localhost:7333 |
| Neo4j | http://localhost:7474 | http://localhost:7474 |
| SearXNG | http://localhost:8081 | http://localhost:8081 |

## Troubleshooting

### Port Already in Use

1. **Find what's using the port:**
   ```bash
   lsof -i -P | grep LISTEN | grep <port>
   ```

2. **Stop the conflicting service** or **use alternative ports** (see above)

### Services Not Starting

1. **Check Docker logs:**
   ```bash
   docker compose -p localai logs
   ```

2. **Verify .env file exists and has all required variables:**
   ```bash
   python3 setup_env.py --force  # Regenerate if needed
   ```

3. **Check disk space:**
   ```bash
   df -h
   ```

### Supabase Issues

- Make sure `POSTGRES_PASSWORD` doesn't contain special characters like `@`
- Ensure `POOLER_DB_POOL_SIZE=5` is set in your `.env`
- Check Supabase logs: `docker compose -p localai logs supabase`

### Permission Issues

For SearXNG, ensure the directory has correct permissions:
```bash
chmod 755 searxng
```

## Next Steps

1. Set up n8n at http://localhost:5678 (or your custom port)
2. Configure credentials in n8n for:
   - Ollama: `http://ollama:11434` (internal) or `http://localhost:12434` (if using custom port)
   - Postgres: Host `db`, use credentials from `.env`
   - Qdrant: `http://qdrant:6333` (internal)
3. Import workflows from the `n8n/backup/workflows/` directory
4. Set up Open WebUI and add the n8n integration

## Security Notes

- Never commit your `.env` file to version control
- All generated secrets are cryptographically secure
- For production, use strong passwords and enable HTTPS via Caddy
- Review and restrict port access in production environments

