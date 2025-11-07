#!/usr/bin/env python3
"""
setup_env.py

This script helps set up the .env file with secure random values and checks for port conflicts.
It will:
1. Check which ports are already in use
2. Generate secure random values for all required secrets
3. Create or update the .env file with appropriate values
"""

import os
import subprocess
import secrets
import string
import socket
from pathlib import Path

# Port mappings from docker-compose.override.private.yml
PORT_MAPPINGS = {
    'flowise': 3001,
    'open-webui': 8080,
    'n8n': 5678,
    'qdrant': [6333, 6334],
    'neo4j': [7473, 7474, 7687],
    'langfuse-worker': 3030,
    'langfuse-web': 3000,
    'clickhouse': [8123, 9000, 9009],
    'minio': [9010, 9011],
    'postgres': 5433,
    'redis': 6379,
    'searxng': 8081,
    'ollama': 11434,
    'caddy': [80, 443],
}

def generate_secret(length=64):
    """Generate a secure random secret."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_hex_secret(length=64):
    """Generate a secure random hex secret."""
    return secrets.token_hex(length // 2)

def check_port_available(port, host='127.0.0.1'):
    """Check if a port is available."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            return result != 0
    except Exception:
        return False

def find_available_port(start_port, host='127.0.0.1', max_attempts=100):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        if check_port_available(port, host):
            return port
    return None

def check_ports():
    """Check which ports are in use and suggest alternatives."""
    print("Checking port availability...")
    print("=" * 60)
    
    conflicts = {}
    suggestions = {}
    
    for service, ports in PORT_MAPPINGS.items():
        if isinstance(ports, list):
            port_list = ports
        else:
            port_list = [ports]
        
        for port in port_list:
            if not check_port_available(port):
                if service not in conflicts:
                    conflicts[service] = []
                conflicts[service].append(port)
                # Suggest alternative
                alt_port = find_available_port(port + 1000)
                if alt_port:
                    if service not in suggestions:
                        suggestions[service] = []
                    suggestions[service].append((port, alt_port))
    
    if conflicts:
        print("⚠️  PORT CONFLICTS DETECTED:")
        print("-" * 60)
        for service, ports in conflicts.items():
            print(f"  {service}: ports {ports} are in use")
            if service in suggestions:
                for orig, alt in suggestions[service]:
                    print(f"    → Consider using port {alt} instead of {orig}")
        print("\n💡 TIP: You can modify docker-compose.override.private.yml")
        print("   to use different ports for these services.")
    else:
        print("✅ All required ports are available!")
    
    print("=" * 60)
    return conflicts, suggestions

def generate_env_file(force=False):
    """Generate .env file with secure random values."""
    env_path = Path('.env')
    env_example_path = Path('.env.example')
    
    # Check if .env already exists
    if env_path.exists() and not force:
        print(f"\n⚠️  .env file already exists at {env_path}")
        print("   Skipping .env file generation (use --force to overwrite).")
        print("   The existing file will be preserved.")
        return
    
    # Generate all required secrets
    print("\nGenerating secure random values for secrets...")
    
    env_vars = {
        # N8N Configuration
        'N8N_ENCRYPTION_KEY': generate_hex_secret(32),
        'N8N_USER_MANAGEMENT_JWT_SECRET': generate_hex_secret(32),
        
        # Supabase Secrets
        'POSTGRES_PASSWORD': generate_secret(32),
        'JWT_SECRET': generate_hex_secret(64),
        'ANON_KEY': generate_hex_secret(64),
        'SERVICE_ROLE_KEY': generate_hex_secret(64),
        'DASHBOARD_USERNAME': 'admin',
        'DASHBOARD_PASSWORD': generate_secret(16),
        'POOLER_TENANT_ID': generate_hex_secret(32),
        'POOLER_DB_POOL_SIZE': '5',
        
        # Neo4j Secrets
        'NEO4J_AUTH': f'neo4j/{generate_secret(16)}',
        
        # Langfuse credentials
        'CLICKHOUSE_PASSWORD': generate_secret(32),
        'MINIO_ROOT_PASSWORD': generate_secret(32),
        'LANGFUSE_SALT': generate_hex_secret(32),
        'NEXTAUTH_SECRET': generate_hex_secret(32),
        'ENCRYPTION_KEY': generate_hex_secret(32),
        
        # Flowise credentials
        'FLOWISE_USERNAME': 'admin',
        'FLOWISE_PASSWORD': generate_secret(16),
        
        # Optional Supabase variables (can be empty for local dev)
        'LOGFLARE_PUBLIC_ACCESS_TOKEN': '',
        'LOGFLARE_PRIVATE_ACCESS_TOKEN': '',
        'PG_META_CRYPTO_KEY': generate_hex_secret(32),
        
        # Optional: Caddy Config (commented out for local development)
        # 'N8N_HOSTNAME': '',
        # 'WEBUI_HOSTNAME': '',
        # 'FLOWISE_HOSTNAME': '',
        # 'SUPABASE_HOSTNAME': '',
        # 'OLLAMA_HOSTNAME': '',
        # 'SEARXNG_HOSTNAME': '',
        # 'NEO4J_HOSTNAME': '',
        # 'LANGFUSE_HOSTNAME': '',
        # 'LETSENCRYPT_EMAIL': '',
    }
    
    # Read existing .env if it exists to preserve custom values
    existing_vars = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    existing_vars[key.strip()] = value.strip()
    
    # Merge: use existing values if present, otherwise use generated
    final_vars = {}
    for key, default_value in env_vars.items():
        if key in existing_vars:
            final_vars[key] = existing_vars[key]
            print(f"  ✓ Preserved existing value for {key}")
        else:
            final_vars[key] = default_value
            print(f"  ✓ Generated new value for {key}")
    
    # Write .env file
    env_content = """# Local AI Package Environment Variables
# Generated by setup_env.py
# 
# IMPORTANT: Keep this file secure and never commit it to version control!

############
# N8N Configuration
############
N8N_ENCRYPTION_KEY={N8N_ENCRYPTION_KEY}
N8N_USER_MANAGEMENT_JWT_SECRET={N8N_USER_MANAGEMENT_JWT_SECRET}

############
# Supabase Secrets
############
POSTGRES_PASSWORD={POSTGRES_PASSWORD}
JWT_SECRET={JWT_SECRET}
ANON_KEY={ANON_KEY}
SERVICE_ROLE_KEY={SERVICE_ROLE_KEY}
DASHBOARD_USERNAME={DASHBOARD_USERNAME}
DASHBOARD_PASSWORD={DASHBOARD_PASSWORD}
POOLER_TENANT_ID={POOLER_TENANT_ID}
POOLER_DB_POOL_SIZE={POOLER_DB_POOL_SIZE}

############
# Neo4j Secrets
############
NEO4J_AUTH={NEO4J_AUTH}

############
# Langfuse credentials
############
CLICKHOUSE_PASSWORD={CLICKHOUSE_PASSWORD}
MINIO_ROOT_PASSWORD={MINIO_ROOT_PASSWORD}
LANGFUSE_SALT={LANGFUSE_SALT}
NEXTAUTH_SECRET={NEXTAUTH_SECRET}
ENCRYPTION_KEY={ENCRYPTION_KEY}

############
# Flowise credentials
############
FLOWISE_USERNAME={FLOWISE_USERNAME}
FLOWISE_PASSWORD={FLOWISE_PASSWORD}

############
# Optional Supabase variables (for local dev, can be empty)
############
LOGFLARE_PUBLIC_ACCESS_TOKEN={LOGFLARE_PUBLIC_ACCESS_TOKEN}
LOGFLARE_PRIVATE_ACCESS_TOKEN={LOGFLARE_PRIVATE_ACCESS_TOKEN}
PG_META_CRYPTO_KEY={PG_META_CRYPTO_KEY}

############
# Caddy Config (for production - leave commented for local development)
############
# N8N_HOSTNAME=n8n.yourdomain.com
# WEBUI_HOSTNAME=openwebui.yourdomain.com
# FLOWISE_HOSTNAME=flowise.yourdomain.com
# SUPABASE_HOSTNAME=supabase.yourdomain.com
# OLLAMA_HOSTNAME=ollama.yourdomain.com
# SEARXNG_HOSTNAME=searxng.yourdomain.com
# NEO4J_HOSTNAME=neo4j.yourdomain.com
# LANGFUSE_HOSTNAME=langfuse.yourdomain.com
# LETSENCRYPT_EMAIL=your-email@example.com
""".format(**final_vars)
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ .env file created/updated at {env_path}")
    print("\n⚠️  SECURITY REMINDER:")
    print("   - Keep this file secure and never commit it to version control")
    print("   - The generated secrets are cryptographically secure")
    print("   - You can regenerate them anytime by running this script again")

def main():
    import sys
    
    force = '--force' in sys.argv
    
    print("=" * 60)
    print("Local AI Package - Environment Setup")
    print("=" * 60)
    
    # Check ports first
    conflicts, suggestions = check_ports()
    
    # Generate .env file
    print("\n")
    generate_env_file(force=force)
    
    if conflicts:
        print("\n" + "=" * 60)
        print("⚠️  ACTION REQUIRED:")
        print("=" * 60)
        print("Some ports are already in use. You have two options:")
        print("\n1. Stop the conflicting services:")
        print("   - Check what's using the ports: lsof -i -P | grep LISTEN")
        print("   - Stop those services or Docker containers")
        print("\n2. Modify port mappings:")
        print("   - Edit docker-compose.override.private.yml")
        print("   - Change the port mappings for conflicting services")
        print("   - Example: Change '3000:3000' to '3002:3000'")
        print("\n" + "=" * 60)
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Review the .env file and adjust any values if needed")
    print("2. Run: python start_services.py --profile cpu")
    print("   (or --profile gpu-nvidia / gpu-amd if you have GPU support)")

if __name__ == "__main__":
    main()

