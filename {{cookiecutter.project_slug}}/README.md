# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Features

- 🚀 **Rapid Setup**: Morden Python MCP Server implemention with sensible defaults.
- 📦 **Modern Package Management**: Uses [uv](https://docs.astral.sh/uv/) for blazing-fast dependency management.
- 🏢 **Nexus Publishing Ready**: Streamlined support for packaging and publishing to company private Nexus repository.
- 🐳 **Container-Friendly**: Includes a `Dockerfile` for easy building and deployment of Docker images.

## Quick start

This guide will help you get the server running, whether you just generated this project or cloned it from a repository.

### Prerequisites

- Python {{ cookiecutter.python_version }}+
- [uv](https://docs.astral.sh/uv/) installed (`pip install uv`)

### Setup and Run

1. **Navigate to the project directory.**

   If you just generated the project, you are likely already here.

   If you cloned it, `cd` into the directory:

   ```bash
   # This step is only needed if you cloned the repository
   git clone git@github.com:/AfterShip/{{ cookiecutter.project_name }}.git
   cd {{ cookiecutter.project_name }}
   ```

2. **Set up the virtual environment.**

   **If you generated this project from a template locally:** The virtual environment is already created for you. Simply activate it:

   ```bash
   source .venv/bin/activate
   ```

   **If you cloned this repository:** You need to create the virtual environment first:

   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. **Install dependencies.**

   This command installs all project dependencies, including development tools and optional extras.

   ```bash
   uv sync --dev --all-extras
   ```

4. **Run the server.**

   You can now start the server with a single command:

   ```bash
   uv run {{ cookiecutter.package_entrypoint }}
   ```

   Your MCP server is now running and ready to accept connections!

## Development Guide

Extending the server is straightforward. The core logic is in `{{ cookiecutter.package_name }}/server.py`.

### How to Add a New Tool

Tools are functions that the model can call. Add a new one using the `@mcp.tool()` decorator.

```python
# In {{ cookiecutter.package_name }}/server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("{{ cookiecutter.package_name }}")

@mcp.tool()
def my_new_tool(arg1: str, arg2: int) -> str:
    """A description of what my new tool does."""
    # Your tool's logic here
    return f"Result: {arg1} and {arg2}"
```

### How to Add a New Prompt

Prompts provide ready-to-use inputs for the model. Add one with the `@mcp.prompt()` decorator.

```python
# In {{ cookiecutter.package_name }}/server.py

@mcp.prompt()
def my_cool_prompt(name: str = "User") -> str:
    """A prompt that greets the user."""
    return f"Hello, {name}! Here is a cool prompt for you."
```

### How to Add a New Resource

Resources expose data or files to the model. Use the `@mcp.resource()` decorator.

```python
# In {{ cookiecutter.package_name }}/server.py

@mcp.resource("config://my-resource")
def get_my_resource() -> str:
    """Returns the content of my-resource."""
    return "This is the content of the resource."
```

## How to launch the server

The server supports two different transport modes:

### STDIO Transport (Default)

This is the default mode for MCP clients like Claude Desktop. The server communicates through standard input/output:

```bash
# Default stdio mode
uv run {{ cookiecutter.package_entrypoint }}

# Explicitly specify stdio mode
uv run {{ cookiecutter.package_entrypoint }} --transport stdio
```

### HTTP Transport

For web-based integrations or when you need HTTP-based communication:

```bash
# Start HTTP server on default port (typically 8000)
uv run {{ cookiecutter.package_entrypoint }} --transport streamable-http

# Start HTTP server on a specific port
uv run {{ cookiecutter.package_entrypoint }} --transport streamable-http --port 3000

# Start HTTP server with specific host and port
uv run {{ cookiecutter.package_entrypoint }} --transport streamable-http --host 0.0.0.0 --port 3000
```

> **Note**: When using HTTP transport, the server will be accessible at `http://localhost:PORT/mcp` (or your specified host/port).

## Packaging and Publishing to Nexus (Mainly targets STDIO)

This guide explains how to build your project using `uv` and publish it to the company's private Nexus repository using `twine`.

### 1. Build the Package with `uv`

Use the `uv build` command to create the distributable source and wheel files.

```bash
# This command bundles your project into .tar.gz and .whl files
uv build
```

After running the command, you will find the distribution files inside the `dist/` directory.

### 2. Configure Your `~/.pypirc` for Nexus

To upload packages, you need to configure your Nexus credentials in a `.pypirc` file located in your home directory (`~/.pypirc`).

Create or edit the file with the following content, replacing the placeholders with your Nexus credentials.

```ini
[distutils]
index-servers =
    nexus

[nexus]
repository = {{ cookiecutter.nexus_repo_url }}
username = your-nexus-username
password = your-nexus-password
```

**Note**: Apply to the **SRE team** for a team nexus account

### 3. Upload the Package with `twine`

With your package built and credentials configured, use `twine` to upload the files from the `dist/` directory.

```bash
# Upload the package to the 'nexus' repository defined in your .pypirc
twine upload --repository nexus dist/*
```

## Deployment with Docker (Mainly targets STREAMABLE-HTTP)

A `Dockerfile` is provided for easy containerization.

```bash
# Build the Docker image
docker build -t {{ cookiecutter.project_slug }} .

# Run the container
# The -i flag is important for the stdio transport to work correctly
docker run -i {{ cookiecutter.project_slug }}
```

## MCP Client Configuration Guide

This section provides detailed instructions on how to configure this server in various MCP clients, supporting both STDIO and Streamable-HTTP transport modes.

### STDIO Transport Configuration

STDIO is the default transport mode for MCP servers, suitable for most MCP clients (such as Claude Desktop, VS Code, etc.).

#### Method 1: Run with uvx from Nexus (Recommended for Production)

```json
{
    "servers": {
        "{{ cookiecutter.project_name }}": {
            "type": "stdio",
            "command": "uvx",
            "args": [
                "--index",
                "{{ cookiecutter.nexus_url }}",
                "{{ cookiecutter.package_entrypoint }}"
            ]
        }
    }
}
```

#### Method 2: Use Local Development Environment

```json
{
    "servers": {
        "{{ cookiecutter.package_entrypoint }}": {
            "type": "stdio",
            "command": "uv",
            "args": [
                "run",
                "{{ cookiecutter.package_entrypoint }}"
            ],
            "cwd": "/path/to/your/{{ cookiecutter.project_slug }}"
        }
    }
}
```


### Streamable-HTTP Transport Configuration

HTTP transport is suitable for web applications, remote deployments, or integration scenarios that require HTTP protocol.

#### Basic HTTP Configuration

First, start the HTTP server:

```bash
uv run {{ cookiecutter.package_entrypoint }} --transport streamable-http --port 8000
```

Then configure in your MCP client:

```json
{
    "servers": {
        "{{ cookiecutter.project_name }}": {
            "type": "http",
            "url": "http://localhost:8000/mcp"
        }
    }
}
```

#### Custom Port and Host

Start the server:

```bash
uv run {{ cookiecutter.package_entrypoint }} --transport streamable-http --host 0.0.0.0 --port 3000
```

Client configuration:

```json
{
    "servers": {
        "{{ cookiecutter.project_name }}": {
            "type": "http",
            "url": "http://your-server-host:3000/mcp"
        }
    }
}
```

#### HTTP Configuration with Docker

If using Docker deployment:

```bash
# Start Docker container with port mapping
docker run -p 8000:8000 {{ cookiecutter.project_slug }} --transport streamable-http --host 0.0.0.0 --port 8000
```

Client configuration:

```json
{
    "servers": {
        "{{ cookiecutter.project_name }}": {
            "type": "http",
            "url": "http://localhost:8000/mcp"
        }
    }
}
```

### Configuration Examples: Common MCP Clients

#### Claude Desktop Configuration

In `~/.config/claude-desktop/config.json`:

```json
{
    "servers": {
        "{{ cookiecutter.project_name }}": {
            "type": "stdio",
            "command": "uvx",
            "args": [
                "--index",
                "{{ cookiecutter.nexus_url }}",
                "{{ cookiecutter.package_entrypoint }}"
            ]
        }
    }
}
```

#### Cursor Configuration

In `~/.cursor/mcp.json`

```json
{
    "servers": {
        "{{ cookiecutter.project_name }}": {
            "type": "stdio",
            "command": "uvx",
            "args": [
                "--index",
                "{{ cookiecutter.nexus_url }}",
                "{{ cookiecutter.package_entrypoint }}"
            ]
        }
    }
}
```

#### VS Code

In `.vscode/mcp.json`

```json
{
    "servers": {
        "{{ cookiecutter.project_name }}": {
            "type": "stdio",
            "command": "uvx",
            "args": [
                "--index",
                "{{ cookiecutter.nexus_url }}",
                "{{ cookiecutter.package_entrypoint }}"
            ]
        }
    }
}
```
