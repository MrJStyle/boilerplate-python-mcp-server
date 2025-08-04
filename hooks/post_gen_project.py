#!/usr/bin/env python3
"""Post-generation hook for cookiecutter template."""

import os
import subprocess
import sys
import time


def run_command(command, cwd=None, timeout=60):
    """Run a shell command with timeout."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout
        )
        print(f"✅ {command}")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return result
    except subprocess.TimeoutExpired:
        print(f"⏰ {command} (timed out after {timeout}s)")
        return None
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        if e.stdout:
            print(f"   Output: {e.stdout.strip()}")
        return None


def test_stdio_transport(cwd):
    """Test stdio transport functionality."""
    print("\n🧪 Testing stdio transport...")
    result = run_command("uv run python tests/test_stdio.py", cwd=cwd)
    if result:
        print("✅ Stdio transport test passed")
        return True
    else:
        print("❌ Stdio transport test failed")
        return False


def test_streamable_http_transport(cwd):
    """Test streamable-http transport functionality."""
    print("\n🧪 Testing streamable-http transport...")
    
    # Start server in background
    print("🚀 Starting server with streamable-http transport...")
    server_process = subprocess.Popen([
        "uv", "run", "{{ cookiecutter.package_entrypoint }}",
        "--transport", "streamable-http", "--host", "localhost", "--port", "8001"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    
    try:
        # Wait for server to start
        time.sleep(3)
        
        # Check if server is running
        if server_process.poll() is not None:
            stdout, stderr = server_process.communicate()
            print("❌ Server failed to start:")
            print(f"   stdout: {stdout.decode()}")
            print(f"   stderr: {stderr.decode()}")
            return False
        
        # Run the streamable-http test
        result = run_command(
            "uv run python tests/test_streamable_http.py --host localhost --port 8001",
            cwd=cwd
        )
        
        if result:
            print("✅ Streamable-http transport test passed")
            return True
        else:
            print("❌ Streamable-http transport test failed")
            return False
            
    finally:
        # Stop the server
        print("🛑 Stopping test server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
            server_process.wait()


def main():
    """Main post-generation tasks."""
    project_dir = os.getcwd()
    print(f"🚀 Setting up project in: {project_dir}")
    
    # Initialize git repository
    print("\n📝 Initializing git repository...")
    run_command("git init", cwd=project_dir)
    
    # Check if uv is available
    uv_available = run_command("uv --version") is not None
    
    if uv_available:
        print("\n📦 Installing dependencies with uv...")
        # First, remove the placeholder uv.lock if it exists
        if os.path.exists("uv.lock"):
            os.remove("uv.lock")
        
        # Generate uv.lock and install dependencies
        run_command("uv lock", cwd=project_dir)
        run_command("uv sync --all-extras", cwd=project_dir)
            
        # Run initial tests
        print("\n🧪 Running initial transport tests...")
        stdio_ok = test_stdio_transport(cwd=project_dir)
        http_ok = test_streamable_http_transport(cwd=project_dir)
        
        if not stdio_ok or not http_ok:
            print("\n❌ Some transport tests failed. Please review the output above.")
        else:
            print("\n✅ All transport tests passed!")
    else:
        print("\n⚠️  uv not found. Please install dependencies manually:")
        print("   pip install -e .[dev]")
    
    # Remove unnecessary files based on configuration
    files_to_remove = []
    
    if "{{ cookiecutter.include_docker }}" != "y":
        files_to_remove.extend(["Dockerfile", ".dockerignore"])
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🗑️  Removed: {file_path}")
    
    print("\n✨ Project setup complete!")
    print(f"\n📁 Project created: {{ cookiecutter.project_name }}")
    print("\n🚀 Next steps:")
    print("   cd {{ cookiecutter.project_slug }}")
    
    if uv_available:
        print("   uv run {{ cookiecutter.package_entrypoint }}")
    else:
        print("   pip install -e .[dev]")
        print("   {{ cookiecutter.package_entrypoint }}")


if __name__ == "__main__":
    main()
