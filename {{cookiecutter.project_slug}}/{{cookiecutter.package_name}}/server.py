"""MCP Server implementation for {{ cookiecutter.project_name }}."""

import json
from datetime import datetime
from typing import Optional

from loguru import logger
from mcp.server.fastmcp import FastMCP

# Create the FastMCP server
mcp = FastMCP("{{ cookiecutter.package_name }}")


@mcp.tool()
def echo(message: str) -> str:
    """Echo back the input message"""
    logger.info(f"Echo tool called with message: {message}")
    return f"Echo: {message}"


@mcp.tool()
def timestamp(format: str = "iso") -> str:
    """Get current timestamp
    
    Args:
        format: Timestamp format (iso, unix, or human)
    """
    logger.info(f"Timestamp tool called with format: {format}")
    now = datetime.now()
    
    if format == "iso":
        return now.isoformat()
    elif format == "unix":
        return str(int(now.timestamp()))
    elif format == "human":
        return now.strftime("%Y-%m-%d %H:%M:%S")
    else:
        raise ValueError(f"Unknown format: {format}")


@mcp.tool()
def calculate(operation: str, a: float, b: float) -> float:
    """Perform basic arithmetic calculations
    
    Args:
        operation: Mathematical operation (add, subtract, multiply, divide)
        a: First number
        b: Second number
    """
    logger.info(f"Calculate tool called: {a} {operation} {b}")
    
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")


@mcp.prompt()
def hello(name: Optional[str] = None) -> str:
    """A simple greeting prompt
    
    Args:
        name: Name to greet (optional)
    """
    user_name = name or "World"
    logger.info(f"Hello prompt called for: {user_name}")
    return f"Hello, {user_name}! Welcome to {{ cookiecutter.project_name }}."


@mcp.resource("config://settings")
def get_server_config() -> str:
    """Server configuration settings"""
    logger.info("Config resource accessed")
    settings = {
        "name": "{{ cookiecutter.project_name }}",
        "version": "{{ cookiecutter.version }}",
        "author": "{{ cookiecutter.author_name }}",
        "description": "{{ cookiecutter.project_description }}",
    }
    return json.dumps(settings, indent=2)


def create_server() -> FastMCP:
    """Create and configure the FastMCP server."""
    logger.info("Creating FastMCP server")
    return mcp
