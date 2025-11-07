#!/bin/bash
echo "=== Fixing Caddy for Localhost Access ==="
echo ""

# Create a backup of the original Caddyfile
cp Caddyfile Caddyfile.backup
echo "✅ Backup created: Caddyfile.backup"
echo ""

# Create a new Caddyfile with localhost routes
cat > Caddyfile << 'CADDYEOF'
{
    # Global options
    email {$LETSENCRYPT_EMAIL}
}

# Localhost routes for local development
:80 {
    # Route /n8n to n8n
    handle_path /n8n* {
        reverse_proxy n8n:5678
    }
    
    # Route /flowise to Flowise
    handle_path /flowise* {
        reverse_proxy flowise:3001
    }
    
    # Route /webui to Open WebUI
    handle_path /webui* {
        reverse_proxy open-webui:8080
    }
    
    # Route /langfuse to Langfuse
    handle_path /langfuse* {
        reverse_proxy langfuse-web:3000
    }
    
    # Route /supabase to Supabase
    handle_path /supabase* {
        reverse_proxy kong:8000
    }
    
    # Route /neo4j to Neo4j
    handle_path /neo4j* {
        reverse_proxy neo4j:7474
    }
    
    # Default route - redirect to n8n
    handle {
        reverse_proxy n8n:5678
    }
}

# Domain-based routes (for production)
{$N8N_HOSTNAME} {
    reverse_proxy n8n:5678
}

{$WEBUI_HOSTNAME} {
    reverse_proxy open-webui:8080
}

{$FLOWISE_HOSTNAME} {
    reverse_proxy flowise:3001
}

{$LANGFUSE_HOSTNAME} {
    reverse_proxy langfuse-web:3000
}

{$SUPABASE_HOSTNAME} {
    reverse_proxy kong:8000
}

{$NEO4J_HOSTNAME} {
    reverse_proxy neo4j:7474
}

import /etc/caddy/addons/*.conf
CADDYEOF

echo "✅ New Caddyfile created with localhost routes"
echo ""
echo "Restarting Caddy..."
docker restart caddy
echo ""
echo "✅ Caddy restarted!"
echo ""
echo "Now you can access services via:"
echo "  - http://localhost (defaults to n8n)"
echo "  - http://localhost/n8n"
echo "  - http://localhost/flowise"
echo "  - http://localhost/webui"
echo "  - http://localhost/langfuse"
echo "  - http://localhost/supabase"
echo "  - http://localhost/neo4j"
echo ""
echo "Or continue using direct ports (which also works):"
echo "  - http://localhost:6678 (n8n)"
echo "  - http://localhost:3001 (flowise)"
echo "  - etc."
