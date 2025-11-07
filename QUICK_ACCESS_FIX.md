# Quick Access Fix for Flowise, ClickHouse, and Caddy

## 🔵 Flowise - Web Application with Login

**URL:** http://localhost:3001

**Credentials:**
- **Username:** `admin`
- **Password:** `lDWblThqRTLTf1EL`

**Steps:**
1. Open http://localhost:3001 in your browser
2. You should see a login page
3. Enter username: `admin`
4. Enter password: `lDWblThqRTLTf1EL`
5. Click "Login"

**If it doesn't work:**
- Check if service is running: `docker ps | grep flowise`
- Restart: `docker restart flowise`
- Wait 30 seconds and try again

---

## 🟢 ClickHouse - Database (No Web Login)

**Important:** ClickHouse is a **database**, not a web application. It doesn't have a login page.

### Access Methods:

#### Option 1: HTTP API (for queries)
- **URL:** http://localhost:9123
- **User:** `clickhouse`
- **Password:** `super-secret-key-1`

**Test connection:**
```bash
curl "http://localhost:9123/?user=clickhouse&password=super-secret-key-1&query=SELECT 1"
```

#### Option 2: Command Line Client
```bash
docker exec -it localai-clickhouse-1 clickhouse-client --user clickhouse --password super-secret-key-1
```

#### Option 3: Database Tools (Recommended)
Use **DBeaver**, **DataGrip**, or **ClickHouse Desktop**:

**Connection Details:**
- **Host:** `localhost`
- **Port:** `10000` (native) or `9123` (HTTP)
- **Database:** `default`
- **User:** `clickhouse`
- **Password:** `super-secret-key-1`

**Download DBeaver (Free):**
- https://dbeaver.io/download/

---

## 🟡 Caddy - Reverse Proxy (No Login)

**Important:** Caddy is a **reverse proxy**, not a web application. It doesn't have a login page.

### What Caddy Does:
- Routes traffic to other services
- Manages HTTPS/TLS certificates
- Acts as a gateway

### Access Services Through Caddy:

If you have domains configured, access services via Caddy:
- http://your-domain.com (if configured)

**Otherwise, access services directly:**
- n8n: http://localhost:6678
- Flowise: http://localhost:3001
- Open WebUI: http://localhost:8080
- etc.

### Check Caddy Status:
```bash
# Check if running
docker ps | grep caddy

# View logs
docker logs caddy --tail 50

# Check configuration
cat Caddyfile
```

### Caddy Admin API (if you need it):
- **URL:** http://localhost:2019
- **No authentication** (local only)

---

## Summary

| Service | Type | Has Login? | Access Method |
|---------|------|------------|---------------|
| **Flowise** | Web App | ✅ Yes | http://localhost:3001<br>User: `admin`<br>Pass: `lDWblThqRTLTf1EL` |
| **ClickHouse** | Database | ❌ No | Use database tools or CLI<br>User: `clickhouse`<br>Pass: `super-secret-key-1` |
| **Caddy** | Proxy | ❌ No | Routes to other services<br>No login interface |

---

## Still Having Issues?

### Flowise Login Problems:
1. Clear browser cache
2. Try incognito/private window
3. Check browser console for errors (F12)
4. Verify credentials are correct (case-sensitive)

### ClickHouse Access Problems:
1. Use a database tool (DBeaver recommended)
2. Or use the CLI method above
3. There is no web login page - it's a database

### Caddy Problems:
1. Caddy doesn't have a login - it's a proxy
2. Access your services directly on their ports
3. Or configure domains in Caddyfile if needed

