#!/usr/bin/env python3
"""
Test script for streamable-http transport functionality.
This script demonstrates how to interact with an MCP server using the mcp client library.
Run this script while the server is running in streamable-http mode.
"""

import asyncio
import pytest
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def test_full_mcp_workflow(session: ClientSession):
    """Test the complete MCP workflow with streamable-http transport."""
    print("🔗 Testing MCP server via session")

    # Test 2: List available tools
    print("\n📤 Step 2: List available tools")
    tools_result = await session.list_tools()
    tools = tools_result.tools
    print(f"🔧 Tools response: {[tool.name for tool in tools]}")
    
    tool_names = [tool.name for tool in tools]
    expected_tools = ["echo", "timestamp", "calculate"]
    for expected_tool in expected_tools:
        assert expected_tool in tool_names, f"Expected tool '{expected_tool}' not found"
    
    print(f"✅ Found expected tools: {expected_tools}")

    # Test 3: Call echo tool
    print("\n📤 Step 3: Call echo tool")
    echo_result = await session.call_tool("echo", {"message": "Hello from streamable-http test!"})
    print(f"🔄 Echo response: {echo_result}")
    assert echo_result is not None

    # Test 4: Call timestamp tool
    print("\n📤 Step 4: Call timestamp tool")
    timestamp_result = await session.call_tool("timestamp", {"format": "iso"})
    print(f"⏰ Timestamp response: {timestamp_result}")
    assert timestamp_result is not None

    # Test 5: Call calculate tool
    print("\n📤 Step 5: Call calculate tool")
    calc_result = await session.call_tool("calculate", {"operation": "add", "a": 10, "b": 5})
    print(f"🧮 Calculate response: {calc_result}")
    assert calc_result is not None

    # Test 6: Test error handling
    print("\n📤 Step 6: Test error handling")
    try:
        error_result = await session.call_tool("calculate", {"operation": "invalid_op", "a": 10, "b": 5})
        # Check if the result indicates an error
        if hasattr(error_result, 'isError') and error_result.isError:
            print("✅ Error handling working correctly - isError=True")
        elif "Unknown operation" in str(error_result) or "error" in str(error_result).lower():
            print("✅ Error handling working correctly - error message found")
        else:
            print(f"⚠️ Expected error but got result: {error_result}")
    except Exception as e:
        print(f"✅ Correctly caught error: {e}")

    # Test 7: List prompts
    print("\n📤 Step 7: List available prompts")
    try:
        prompts_result = await session.list_prompts()
        prompts = prompts_result.prompts
        print(f"📝 Prompts response: {[p.name for p in prompts]}")
        
        if prompts:
            # Test getting a prompt
            prompt_name = prompts[0].name
            print(f"\n📤 Step 7a: Get prompt '{prompt_name}'")
            prompt_content = await session.get_prompt(prompt_name, {"name": "Alice"})
            print(f"📝 Prompt response: {prompt_content}")
            assert prompt_content is not None
    except Exception as e:
        print(f"⚠️ Prompts not available or error: {e}")

    # Test 8: List resources
    print("\n📤 Step 8: List available resources")
    try:
        resources_result = await session.list_resources()
        resources = resources_result.resources
        print(f"📚 Resources response: {[r.uri for r in resources]}")
        
        if resources:
            # Test reading a resource
            resource_uri = resources[0].uri
            print(f"\n📤 Step 8a: Read resource '{resource_uri}'")
            resource_content, _ = await session.read_resource(resource_uri)
            print(f"📄 Resource response: {resource_content[:100]}...")
            assert resource_content is not None
    except Exception as e:
        print(f"⚠️ Resources not available or error: {e}")

    print("\n✅ All tests completed successfully!")


@pytest.fixture(scope="module")
async def client_session(host: str = "127.0.0.1", port: int = 8000):
    """Pytest fixture to create and manage an MCP client session for tests."""
    url = f"http://{host}:{port}/mcp"
    
    async with streamablehttp_client(url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


@pytest.mark.asyncio
async def test_streamable_http(client_session: ClientSession):
    """Basic pytest test for streamable-http transport."""
    tools_result = await client_session.list_tools()
    assert len(tools_result.tools) > 0


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test MCP streamable-http transport")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    
    args = parser.parse_args()
    
    async def main():
        print("🧪 MCP StreamableHTTP Transport Test")
        print("=====================================")
        print("Make sure your MCP server is running with:")
        print(f"  {{ cookiecutter.package_entrypoint }} --transport streamable-http --host {args.host} --port {args.port}")
        print()
        
        url = f"http://{args.host}:{args.port}/mcp"
        
        try:
            async with streamablehttp_client(url) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    await test_full_mcp_workflow(session)
        except Exception as e:
            print(f"❌ Test failed: {e}")
            print("\nMake sure the server is running and accessible!")
            exit(1)

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        exit(1)
