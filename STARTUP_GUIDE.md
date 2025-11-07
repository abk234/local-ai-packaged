# Startup Guide

This guide ensures your Local AI Package starts without issues.

## Quick Start

### Option 1: Automated Startup (Recommended)

```bash
python3 start_all_services.py --profile cpu
```

This script will:
- Clean up old containers
- Set up environment files
- Start Supabase services
- Start local AI services
- Verify all services are running

### Option 2: Manual Startup

```bash
# 1. Set up environment
python3 setup_env.py --force

# 2. Start Supabase
docker compose -p localai \
  -f supabase/docker/docker-compose.yml \
  -f docker-compose.override.supabase.local.yml \
  up -d

# 3. Wait for Supabase (15-30 seconds)
sleep 20

# 4. Start local AI services
docker compose -p localai \
  --profile cpu \
  -f docker-compose.yml \
  -f docker-compose.override.private.yml \
  -f docker-compose.override.local.yml \
  up -d
```

## Health Check

Check if all services are running:

```bash
python3 check_services.py
```

Or manually:

```bash
docker compose -p localai ps
docker compose -p localai -f supabase/docker/docker-compose.yml ps
```

## Service Access URLs

Once started, access your services at:

- **Supabase Studio**: http://localhost:3000
- **Supabase API**: http://localhost:8000
- **n8n**: http://localhost:6678
- **Open WebUI**: http://localhost:8080
- **Flowise**: http://localhost:3001
- **Langfuse**: http://localhost:4000
- **Qdrant**: http://localhost:7333
- **Neo4j**: http://localhost:7474
- **SearXNG**: http://localhost:8081
- **Ollama API**: http://localhost:12434
- **Supabase Analytics**: http://localhost:5000

## Troubleshooting

### Port Conflicts

If you see port conflicts, check what's using the port:

```bash
lsof -i :PORT_NUMBER
```

### Service Not Starting

Check service logs:

```bash
docker compose -p localai logs SERVICE_NAME
```

### Reset Everything

To completely reset and start fresh:

```bash
# Stop all services
docker compose -p localai down
docker compose -p localai -f supabase/docker/docker-compose.yml down

# Remove volumes (optional - this will delete data)
docker volume prune -f

# Start fresh
python3 start_all_services.py --profile cpu
```

### Common Issues

1. **Supabase pooler not starting**: This is optional and can be skipped. All other Supabase services will work fine.

2. **n8n waiting for database**: Wait a bit longer for Supabase to fully initialize (30-60 seconds).

3. **Port already in use**: Check if you have other Docker containers or services using the same ports.

## Startup Order

Services start in this order:

1. **Infrastructure** (Postgres, Redis, ClickHouse, MinIO)
2. **Supabase** (db, auth, kong, rest, storage, studio)
3. **AI Services** (Ollama, Langfuse, Qdrant, Neo4j)
4. **Applications** (n8n, Open WebUI, Flowise, SearXNG)

The startup script handles this automatically.

## Environment Variables

Make sure your `.env` file has all required variables. Run:

```bash
python3 setup_env.py --force
```

This will generate/update your `.env` file with all required values.

## Profiles

- `cpu`: For CPU-only systems (default)
- `gpu-nvidia`: For NVIDIA GPU systems
- `gpu-amd`: For AMD GPU systems
- `none`: No profile (minimal services)

## Next Steps

After services are running:

1. Access Supabase Studio to set up your database schema
2. Configure n8n workflows
3. Set up Open WebUI with your Ollama models
4. Start building your AI applications!

