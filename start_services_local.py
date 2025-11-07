#!/usr/bin/env python3
"""
start_services_local.py

This script starts services using custom port mappings to avoid conflicts.
It's a wrapper around start_services.py that includes the local override file.
"""

import subprocess
import sys
import os

def run_command(cmd, cwd=None):
    """Run a shell command and print it."""
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 start_services_local.py --profile <cpu|gpu-nvidia|gpu-amd|none> [--environment <private|public>]")
        sys.exit(1)
    
    profile = 'cpu'
    environment = 'private'
    
    # Parse arguments
    if '--profile' in sys.argv:
        idx = sys.argv.index('--profile')
        if idx + 1 < len(sys.argv):
            profile = sys.argv[idx + 1]
    
    if '--environment' in sys.argv:
        idx = sys.argv.index('--environment')
        if idx + 1 < len(sys.argv):
            environment = sys.argv[idx + 1]
    
    print("=" * 60)
    print("Starting Local AI Package with Custom Ports")
    print("=" * 60)
    print(f"Profile: {profile}")
    print(f"Environment: {environment}")
    print("Using docker-compose.override.local.yml for port mappings")
    print("=" * 60)
    
    # First, run the standard setup (Supabase clone, env prep, etc.)
    print("\n1. Running standard setup...")
    from start_services import clone_supabase_repo, prepare_supabase_env, generate_searxng_secret_key, check_and_fix_docker_compose_for_searxng
    
    clone_supabase_repo()
    prepare_supabase_env()
    generate_searxng_secret_key()
    check_and_fix_docker_compose_for_searxng()
    
    # Stop existing containers
    print("\n2. Stopping existing containers...")
    cmd = ["docker", "compose", "-p", "localai"]
    if profile and profile != "none":
        cmd.extend(["--profile", profile])
    cmd.extend(["-f", "docker-compose.yml", "down"])
    run_command(cmd)
    
    # Start Supabase
    print("\n3. Starting Supabase services...")
    cmd = ["docker", "compose", "-p", "localai", "-f", "supabase/docker/docker-compose.yml"]
    if environment and environment == "public":
        cmd.extend(["-f", "docker-compose.override.public.supabase.yml"])
    cmd.extend(["up", "-d"])
    run_command(cmd)
    
    # Wait for Supabase
    print("\n4. Waiting for Supabase to initialize...")
    import time
    time.sleep(10)
    
    # Start local AI services with local override
    print("\n5. Starting local AI services with custom ports...")
    cmd = ["docker", "compose", "-p", "localai"]
    if profile and profile != "none":
        cmd.extend(["--profile", profile])
    cmd.extend(["-f", "docker-compose.yml"])
    if environment and environment == "private":
        cmd.extend(["-f", "docker-compose.override.private.yml"])
        cmd.extend(["-f", "docker-compose.override.local.yml"])  # Add local override
    if environment and environment == "public":
        cmd.extend(["-f", "docker-compose.override.public.yml"])
    cmd.extend(["up", "-d"])
    run_command(cmd)
    
    print("\n" + "=" * 60)
    print("✅ Services started with custom port mappings!")
    print("=" * 60)
    print("\nAccess services at:")
    print("  - n8n: http://localhost:6678")
    print("  - Open WebUI: http://localhost:8080")
    print("  - Flowise: http://localhost:3001")
    print("  - Langfuse: http://localhost:4000")
    print("  - Qdrant: http://localhost:7333")
    print("  - Neo4j: http://localhost:7474")
    print("  - SearXNG: http://localhost:8081")
    print("  - Ollama: http://localhost:12434")
    print("\nNote: Internal service communication uses container names,")
    print("      so services can still communicate even with custom ports.")

if __name__ == "__main__":
    main()

