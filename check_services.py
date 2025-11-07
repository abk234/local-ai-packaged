#!/usr/bin/env python3
"""
check_services.py

Quick health check script to verify all services are running properly.
"""

import subprocess
import sys

def run_command(cmd):
    """Run a shell command."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def check_service(service_name, port=None):
    """Check if a service is running."""
    result = run_command([
        "docker", "ps", "--filter", f"name={service_name}",
        "--format", "{{.Names}}\t{{.Status}}\t{{.Ports}}"
    ])
    
    if result and service_name.split("-")[-1] in result:
        status = "✅ Running"
        if port:
            if f":{port}" in result:
                status += f" (port {port})"
        print(f"{status:30} {service_name}")
        return True
    else:
        print(f"{'❌ Not Running':30} {service_name}")
        return False

def main():
    print("=" * 70)
    print("Service Health Check")
    print("=" * 70)
    print()
    
    services = [
        # Supabase services
        ("supabase-db", 5432),
        ("supabase-kong", 8000),
        ("supabase-auth", None),
        ("supabase-studio", 3000),
        ("supabase-analytics", 5000),
        ("supabase-rest", None),
        ("supabase-storage", None),
        ("supabase-meta", None),
        ("realtime-dev.supabase-realtime", None),
        
        # Local AI services
        ("n8n", 6678),
        ("ollama", 12434),
        ("open-webui", 8080),
        ("flowise", 3001),
        ("localai-langfuse-web-1", 4000),
        ("localai-langfuse-worker-1", 4030),
        ("qdrant", 7333),
        ("neo4j", 7474),
        ("searxng", 8081),
        ("redis", 7379),
        ("localai-postgres-1", 5433),
        ("localai-clickhouse-1", 9123),
        ("localai-minio-1", 9010),
    ]
    
    running = 0
    total = len(services)
    
    print(f"{'Status':<30} {'Service Name'}")
    print("-" * 70)
    
    for service, port in services:
        if check_service(service, port):
            running += 1
    
    print()
    print("=" * 70)
    print(f"Summary: {running}/{total} services running")
    print("=" * 70)
    
    if running == total:
        print("\n✅ All services are running!")
        return 0
    else:
        print(f"\n⚠️  {total - running} service(s) not running")
        print("\nTo start services, run:")
        print("  python3 start_all_services.py --profile cpu")
        return 1

if __name__ == "__main__":
    sys.exit(main())

