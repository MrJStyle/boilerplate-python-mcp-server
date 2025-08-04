"""Main entry point for {{ cookiecutter.project_name }}."""

import sys
from typing import Any
from enum import Enum

import typer
from loguru import logger
from rich.console import Console

from .server import create_server

app = typer.Typer(
    name="{{ cookiecutter.package_name }}",
    help="{{ cookiecutter.project_description }}",
    add_completion=False,
)
console = Console()

class Transport(str, Enum):
    stdio = "stdio"
    streamable_http = "streamable-http"


@app.command()
def serve(
    transport: Transport = typer.Option(
        "stdio",
        "--transport",
        "-t",
        help="Transport mechanism (stdio or streamable-http)",
    ),
    host: str = typer.Option(
        "localhost",
        "--host",
        "-h",
        help="Host to bind to (for streamable-http transport)",
    ),
    port: int = typer.Option(
        8000,
        "--port",
        "-p",
        help="Port to bind to (for streamable-http transport)",
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        "-l",
        help="Log level (DEBUG, INFO, WARNING, ERROR)",
    ),
) -> None:
    """Start the MCP server."""
    # Configure logging
    logger.remove()
    logger.add(
        sys.stderr,
        level=log_level.upper(),
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )

    console.print(f"🚀 Starting {{ cookiecutter.project_name }} server...")
    console.print(f"📡 Transport: {transport}")
    
    if transport == "streamable-http":
        console.print(f"🌐 Host: {host}")
        console.print(f"📝 Port: {port}")
    
    console.print(f"📊 Log level: {log_level.upper()}")

    try:
        # Get the FastMCP server
        mcp_server = create_server()
        
        # Run the server using FastMCP's built-in run method
        if transport == "stdio":
            mcp_server.run()
        elif transport == "streamable-http":
            # For streamable-http, we need to run with uvicorn
            import uvicorn
            app = mcp_server.streamable_http_app()
            uvicorn.run(app, host=host, port=port, log_level=log_level.lower())
        else:
            raise ValueError(f"Unsupported transport: {transport}")
            
    except KeyboardInterrupt:
        console.print("\n👋 Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        console.print(f"❌ Error: {e}", style="red")
        sys.exit(1)


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
