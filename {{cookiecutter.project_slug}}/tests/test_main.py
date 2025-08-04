"""Tests for {{ cookiecutter.project_name }}."""

import pytest
import tempfile
import os
from pathlib import Path
from {{ cookiecutter.package_name }} import __version__


def test_version():
    """Test version is defined."""
    assert __version__ == "{{ cookiecutter.version }}"


@pytest.mark.asyncio
async def test_server_creation():
    """Test server can be created."""
    from {{ cookiecutter.package_name }}.server import create_server
    
    server = create_server()
    assert server is not None


@pytest.mark.asyncio
async def test_example_tools():
    """Test example tools."""
    from {{ cookiecutter.package_name }}.tools.example_tool import execute_example_tool
    
    # Test echo tool
    result = await execute_example_tool("example_echo", {"message": "Hello"})
    assert result == "Echo: Hello"
    
    # Test timestamp tool
    result = await execute_example_tool("example_timestamp", {"format": "unix"})
    assert isinstance(result, int)
    
    # Test calculate tool
    result = await execute_example_tool("example_calculate", {
        "operation": "add",
        "a": 2,
        "b": 3
    })
    assert result == 5


@pytest.mark.asyncio
async def test_tool_error_handling():
    """Test tool error handling."""
    from {{ cookiecutter.package_name }}.tools.example_tool import execute_example_tool
    
    # Test division by zero
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        await execute_example_tool("example_calculate", {
            "operation": "divide",
            "a": 5,
            "b": 0
        })
    
    # Test unknown operation
    with pytest.raises(ValueError, match="Unknown operation"):
        await execute_example_tool("example_calculate", {
            "operation": "invalid",
            "a": 1,
            "b": 2
        })
    
    # Test unknown tool
    with pytest.raises(ValueError, match="Unknown example tool"):
        await execute_example_tool("invalid_tool", {})


@pytest.mark.asyncio
async def test_file_tools():
    """Test file operation tools."""
    from {{ cookiecutter.package_name }}.tools.file_tools import execute_file_tool
    import tempfile
    import os
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test file write
        test_file = os.path.join(temp_dir, "test.txt")
        test_content = "Hello, World!"
        
        result = await execute_file_tool("file_write", {
            "path": test_file,
            "content": test_content
        })
        assert result["success"] is True
        assert result["size"] == len(test_content)
        
        # Test file read
        result = await execute_file_tool("file_read", {
            "path": test_file
        })
        assert result["content"] == test_content
        assert result["size"] == len(test_content)
        
        # Test file list
        result = await execute_file_tool("file_list", {
            "path": temp_dir
        })
        assert result["count"] == 1
        assert len(result["files"]) == 1
        assert result["files"][0]["name"] == "test.txt"


@pytest.mark.asyncio
async def test_file_tools_error_handling():
    """Test file tools error handling."""
    from {{ cookiecutter.package_name }}.tools.file_tools import execute_file_tool
    
    # Test reading non-existent file
    with pytest.raises(ValueError, match="Error reading file"):
        await execute_file_tool("file_read", {
            "path": "/non/existent/file.txt"
        })
    
    # Test listing non-existent directory
    with pytest.raises(ValueError, match="Error listing directory"):
        await execute_file_tool("file_list", {
            "path": "/non/existent/directory"
        })
    
    # Test unknown tool
    with pytest.raises(ValueError, match="Unknown file tool"):
        await execute_file_tool("invalid_file_tool", {})
