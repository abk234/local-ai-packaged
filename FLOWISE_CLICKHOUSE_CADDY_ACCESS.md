# Flowise, ClickHouse, and Caddy Access Guide

**Date:** 2025-11-07  
**Purpose:** Troubleshooting login and access issues

---

## 1. Flowise Access

### URL
- **Web UI:** http://localhost:3001

### Credentials
- **Username:** `admin`
- **Password:** `lDWblThqRTLTf1EL`

### Troubleshooting

**If you can't log in:**

1. **Verify service is running:**
   ```bash
   docker ps | grep flowise
   ```

2. **Check if credentials are correct:**
   ```bash
   docker exec flowise printenv | grep FLOWISE
   ```
   Should show:
   - `FLOWISE_USERNAME=admin`
   - `FLOWISE_PASSWORD=lDWblThqRTLTf1EL`

3. **Reset credentials (if needed):**
   - Edit `.env` file:
     ```bash
     FLOWISE_USERNAME=admin
     FLOWISE_PASSWORD=your-new-password
     ```
   - Restart Flowise:
     ```bash
     docker restart flowise
     ```

4. **Check Flowise logs:**
   ```bash
   docker logs flowise --tail 50
   ```

5. **Try accessing directly:**
   - Open http://localhost:3001 in your browser
   - If you see a login page, use the credentials above
   - If you see an error, check the logs

### Common Issues

- **"Cannot connect" error:** Service might not be fully started, wait 30 seconds and try again
- **"Invalid credentials":** Double-check username and password (case-sensitive)
- **Blank page:** Check browser console for errors, verify service is running

---

## 2. ClickHouse Access

### Important Note
**ClickHouse is a database, not a web application with a login interface.** It's accessed via:
- HTTP API (port 9123)
- Native protocol (port 10000)
- Command line client
- Third-party tools (like DBeaver, DataGrip)

### Access Methods

#### Method 1: HTTP Interface (Read-only queries)
- **URL:** http://localhost:9123
- **Credentials:**
  - **User:** `default` (or `clickhouse` if configured)
  - **Password:** Usually empty for local setup, or check `CLICKHOUSE_PASSWORD` in `.env`

**Test connection:**
```bash
curl "http://localhost:9123/?query=SELECT 1"
```

#### Method 2: ClickHouse Client (CLI)
```bash
docker exec -it localai-clickhouse-1 clickhouse-client
```

#### Method 3: Database Tools
Use tools like:
- **DBeaver** (free, cross-platform)
- **DataGrip** (JetBrains, paid)
- **ClickHouse Desktop** (official GUI)

**Connection details:**
- **Host:** `localhost`
- **Port:** `10000` (native) or `9123` (HTTP)
- **Database:** `default`
- **User:** `default` or `clickhouse`
- **Password:** Check `.env` file for `CLICKHOUSE_PASSWORD` (may be empty)

#### Method 4: Check Credentials
```bash
# Check environment variables
docker exec localai-clickhouse-1 printenv | grep CLICKHOUSE

# Check if password is set
docker exec localai-clickhouse-1 printenv CLICKHOUSE_PASSWORD
```

### Troubleshooting

**If you can't connect:**

1. **Verify service is running:**
   ```bash
   docker ps | grep clickhouse
   ```

2. **Test HTTP connection:**
   ```bash
   curl "http://localhost:9123/?query=SELECT version()"
   ```

3. **Check ClickHouse logs:**
   ```bash
   docker logs localai-clickhouse-1 --tail 50
   ```

4. **Try without password (if password is empty):**
   ```bash
   docker exec -it localai-clickhouse-1 clickhouse-client --user default
   ```

### Common Issues

- **"Connection refused":** Service might not be running or port is wrong
- **"Authentication failed":** Password might be set, check `.env` file
- **"No web interface":** ClickHouse doesn't have a built-in web UI - use a database tool

---

## 3. Caddy Access

### Important Note
**Caddy is a reverse proxy/web server, not a web application with a login interface.** It doesn't have a login page - it routes traffic to other services.

### What Caddy Does
- Manages HTTPS/TLS certificates
- Routes traffic to services based on domain names
- Acts as a reverse proxy

### Access Methods

#### Method 1: Check Caddy Status
```bash
# Check if Caddy is running
docker ps | grep caddy

# Check Caddy logs
docker logs caddy --tail 50

# Check Caddy admin API (if enabled)
curl http://localhost:2019/config/
```

#### Method 2: View Caddy Configuration
```bash
# View Caddyfile
cat Caddyfile

# Check mounted configuration
docker exec caddy cat /etc/caddy/Caddyfile
```

#### Method 3: Access Services Through Caddy
If Caddy is configured with domains, access services via:
- http://your-domain.com (if configured)
- Or directly via service ports (e.g., http://localhost:6678 for n8n)

### Troubleshooting

**If Caddy isn't working:**

1. **Check if Caddy is running:**
   ```bash
   docker ps | grep caddy
   ```

2. **Check Caddy logs:**
   ```bash
   docker logs caddy --tail 100
   ```

3. **Verify Caddyfile exists:**
   ```bash
   ls -la Caddyfile
   cat Caddyfile
   ```

4. **Check port bindings:**
   ```bash
   docker ps | grep caddy
   # Should show ports 80 and 443
   ```

5. **Test HTTP access:**
   ```bash
   curl http://localhost:80
   ```

### Common Issues

- **"No login page":** Caddy doesn't have a login - it's a proxy
- **"Connection refused":** Caddy might not be running or ports aren't exposed
- **"404 Not Found":** Caddy is running but no routes are configured, or you're accessing the wrong URL

### Caddy Admin API (if enabled)
If Caddy admin API is enabled, you can access it at:
- **URL:** http://localhost:2019
- **No authentication** (local setup only)

**Check admin API:**
```bash
curl http://localhost:2019/config/
```

---

## Quick Reference

### Flowise
- **URL:** http://localhost:3001
- **Username:** `admin`
- **Password:** `lDWblThqRTLTf1EL`
- **Type:** Web application with login

### ClickHouse
- **HTTP:** http://localhost:9123
- **Native:** localhost:10000
- **User:** `default` or `clickhouse`
- **Password:** Check `.env` (may be empty)
- **Type:** Database (use database tools, not web login)

### Caddy
- **HTTP:** http://localhost:80
- **HTTPS:** https://localhost:443
- **Admin API:** http://localhost:2019 (if enabled)
- **Type:** Reverse proxy (no login interface)

---

## Summary

1. **Flowise:** Has a web login - use `admin` / `lDWblThqRTLTf1EL`
2. **ClickHouse:** Database, not a web app - use database tools or CLI
3. **Caddy:** Reverse proxy, no login - routes traffic to other services

---

## Still Having Issues?

### For Flowise:
```bash
# Check service status
docker ps | grep flowise

# View logs
docker logs flowise --tail 50

# Restart if needed
docker restart flowise
```

### For ClickHouse:
```bash
# Check service status
docker ps | grep clickhouse

# Test connection
curl "http://localhost:9123/?query=SELECT 1"

# Access via CLI
docker exec -it localai-clickhouse-1 clickhouse-client
```

### For Caddy:
```bash
# Check service status
docker ps | grep caddy

# View logs
docker logs caddy --tail 50

# Check configuration
cat Caddyfile
```

---

**End of Guide**

