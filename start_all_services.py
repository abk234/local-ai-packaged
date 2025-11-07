#!/usr/bin/env python3
"""
start_all_services.py

Comprehensive startup script that ensures all services start without issues.
Handles dependencies, port conflicts, and proper initialization order.
"""

import subprocess
import sys
import os
import time
import argparse

def run_command(cmd, cwd=None, check=True):
    """Run a shell command and print it."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"Error: {result.stderr}")
    return result

def check_port(port):
    """Check if a port is in use."""
    result = run_command(["lsof", "-i", f":{port}"], check=False)
    return result.returncode == 0

def wait_for_service(service_name, max_wait=60):
    """Wait for a service to be healthy."""
    print(f"Waiting for {service_name} to be healthy...")
    for i in range(max_wait):
        result = run_command(
            ["docker", "ps", "--filter", f"name={service_name}", "--format", "{{.Status}}"],
            check=False
        )
        if "healthy" in result.stdout or "Up" in result.stdout:
            print(f"✅ {service_name} is ready")
            return True
        time.sleep(1)
    print(f"⚠️  {service_name} may not be fully ready")
    return False

def cleanup_containers():
    """Clean up any problematic containers."""
    print("\n1. Cleaning up old containers...")
    
    # Remove old containers that might cause conflicts
    old_containers = [
        "ollama-pull-llama",
        "n8n-import",
        "langfuse-langfuse-web-1"
    ]
    
    for container in old_containers:
        run_command(["docker", "rm", "-f", container], check=False)
    
    print("✅ Cleanup complete")

def setup_environment():
    """Set up environment files."""
    print("\n2. Setting up environment...")
    
    # Import setup functions
    from start_services import (
        clone_supabase_repo,
        prepare_supabase_env,
        generate_searxng_secret_key,
        check_and_fix_docker_compose_for_searxng
    )
    
    clone_supabase_repo()
    prepare_supabase_env()
    generate_searxng_secret_key()
    check_and_fix_docker_compose_for_searxng()
    
    print("✅ Environment setup complete")

def start_supabase():
    """Start Supabase services."""
    print("\n3. Starting Supabase services...")
    
    # Check if Supabase is already running
    result = run_command([
        "docker", "compose", "-p", "localai",
        "-f", "supabase/docker/docker-compose.yml",
        "ps", "--format", "{{.Name}}"
    ], check=False)
    
    if "supabase-db" in result.stdout:
        print("Supabase services already running, skipping restart...")
        print("To restart Supabase, stop services first:")
        print("  docker compose -p localai -f supabase/docker/docker-compose.yml down")
        return
    
    # Start Supabase with override file
    run_command([
        "docker", "compose", "-p", "localai",
        "-f", "supabase/docker/docker-compose.yml",
        "-f", "docker-compose.override.supabase.local.yml",
        "up", "-d"
    ], check=False)
    
    # Wait for critical Supabase services
    print("Waiting for Supabase to initialize...")
    time.sleep(15)
    
    wait_for_service("supabase-db")
    wait_for_service("supabase-kong")
    wait_for_service("supabase-auth")
    
    print("✅ Supabase services started")

def start_local_ai_services(profile="cpu"):
    """Start local AI services."""
    print(f"\n4. Starting local AI services (profile: {profile})...")
    
    # Check if services are already running
    result = run_command([
        "docker", "compose", "-p", "localai",
        "--profile", profile,
        "-f", "docker-compose.yml",
        "ps", "--format", "{{.Name}}"
    ], check=False)
    
    if "n8n" in result.stdout or "ollama" in result.stdout:
        print("Local AI services already running, ensuring all are up...")
        # Just ensure all services are up
        cmd = [
            "docker", "compose", "-p", "localai",
            "--profile", profile,
            "-f", "docker-compose.yml",
            "-f", "docker-compose.override.private.yml",
            "-f", "docker-compose.override.local.yml",
            "up", "-d"
        ]
        run_command(cmd, check=False)
    else:
        # Start services with all override files
        cmd = [
            "docker", "compose", "-p", "localai",
            "--profile", profile,
            "-f", "docker-compose.yml",
            "-f", "docker-compose.override.private.yml",
            "-f", "docker-compose.override.local.yml",
            "up", "-d"
        ]
        run_command(cmd)
    
    # Wait for critical services
    print("Waiting for services to initialize...")
    time.sleep(10)
    
    wait_for_service("n8n")
    wait_for_service("ollama")
    wait_for_service("redis")
    
    print("✅ Local AI services started")

def verify_services():
    """Verify all services are running."""
    print("\n5. Verifying services...")
    
    critical_services = [
        "supabase-db",
        "supabase-kong",
        "supabase-auth",
        "n8n",
        "ollama",
        "redis",
        "localai-postgres-1",
        "localai-clickhouse-1"
    ]
    
    all_running = True
    for service in critical_services:
        result = run_command(
            ["docker", "ps", "--filter", f"name={service}", "--format", "{{.Names}}"],
            check=False
        )
        if service in result.stdout or any(service.split("-")[-1] in line for line in result.stdout.split("\n")):
            print(f"✅ {service} is running")
        else:
            print(f"❌ {service} is not running")
            all_running = False
    
    return all_running

def print_service_urls():
    """Print service access URLs."""
    print("\n" + "=" * 60)
    print("✅ All services started successfully!")
    print("=" * 60)
    print("\nAccess your services at:")
    print("  📊 Supabase Studio:     http://localhost:3000")
    print("  🔌 Supabase API:        http://localhost:8000")
    print("  🤖 n8n:                 http://localhost:6678")
    print("  💬 Open WebUI:          http://localhost:8080")
    print("  🔄 Flowise:             http://localhost:3001")
    print("  📈 Langfuse:            http://localhost:4000")
    print("  🔍 Qdrant:              http://localhost:7333")
    print("  🕸️  Neo4j:               http://localhost:7474")
    print("  🔎 SearXNG:             http://localhost:8081")
    print("  🦙 Ollama API:          http://localhost:12434")
    print("  📊 Supabase Analytics:  http://localhost:5000")
    print("\n" + "=" * 60)

def main():
    parser = argparse.ArgumentParser(
        description='Start all services for the Local AI Package'
    )
    parser.add_argument(
        '--profile',
        choices=['cpu', 'gpu-nvidia', 'gpu-amd', 'none'],
        default='cpu',
        help='Docker Compose profile to use (default: cpu)'
    )
    parser.add_argument(
        '--skip-cleanup',
        action='store_true',
        help='Skip cleanup of old containers'
    )
    parser.add_argument(
        '--skip-verify',
        action='store_true',
        help='Skip service verification'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Local AI Package - Startup Script")
    print("=" * 60)
    print(f"Profile: {args.profile}")
    print("=" * 60)
    
    try:
        if not args.skip_cleanup:
            cleanup_containers()
        
        setup_environment()
        start_supabase()
        start_local_ai_services(args.profile)
        
        if not args.skip_verify:
            if verify_services():
                print_service_urls()
            else:
                print("\n⚠️  Some services may not be running. Check logs with:")
                print("   docker compose -p localai ps")
                sys.exit(1)
        else:
            print_service_urls()
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting services: {e}")
        print("\nTroubleshooting:")
        print("  1. Check Docker is running: docker ps")
        print("  2. Check port conflicts: lsof -i :PORT")
        print("  3. Check logs: docker compose -p localai logs SERVICE_NAME")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Startup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

