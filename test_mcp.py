import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "backend/mcp_server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("\n" + "="*60)
            print("--- Available MCP Tools ---")
            print("="*60)
            for tool in tools.tools:
                print(f"\n• {tool.name}")
                print(f"  {tool.description}")

            # Test list_procurement_files
            print("\n" + "="*60)
            print("--- Testing list_procurement_files ---")
            print("="*60)
            files = await session.call_tool("list_procurement_files", arguments={})
            print(f"Files: {files.content}")

            # Test get_file_info
            if files.content and isinstance(files.content, list) and len(files.content) > 0:
                # Extract filename from TextContent object
                first_file_obj = files.content[0]
                if hasattr(first_file_obj, 'text'):
                    first_file = first_file_obj.text
                elif isinstance(first_file_obj, str):
                    first_file = first_file_obj
                else:
                    first_file = str(first_file_obj)
                
                if not first_file.startswith("Error"):
                    print("\n" + "="*60)
                    print(f"--- Testing get_file_info for: {first_file} ---")
                    print("="*60)
                    file_info = await session.call_tool("get_file_info", arguments={"filename": first_file})
                    print(f"File Info: {file_info.content}")

            # Test query_procurement_data
            print("\n" + "="*60)
            print("--- Testing query_procurement_data ---")
            print("="*60)
            query_result = await session.call_tool("query_procurement_data", arguments={"query": "risk", "n_results": 3})
            result_str = str(query_result.content)
            print(f"Query Result (First 300 chars):\n{result_str[:300]}...")

            # Test agent-based analysis (spend)
            print("\n" + "="*60)
            print("--- Testing analyze_spend ---")
            print("="*60)
            try:
                spend_result = await session.call_tool("analyze_spend", arguments={})
                result_str = str(spend_result.content)
                print(f"Spend Analysis (First 300 chars):\n{result_str[:300]}...")
            except Exception as e:
                print(f"Error: {e}")

            # List prompts if available
            try:
                prompts = await session.list_prompts()
                if prompts.prompts:
                    print("\n" + "="*60)
                    print("--- Available Prompts ---")
                    print("="*60)
                    for prompt in prompts.prompts:
                        print(f"\n• {prompt.name}")
                        print(f"  {prompt.description}")
            except Exception as e:
                print(f"\nNote: Prompts not available ({type(e).__name__})")

            # List resources if available
            try:
                resources = await session.list_resources()
                if resources.resources:
                    print("\n" + "="*60)
                    print("--- Available Resources ---")
                    print("="*60)
                    for resource in resources.resources:
                        print(f"\n• {resource.uri}")
                        print(f"  {resource.name}")
            except Exception as e:
                print(f"\nNote: Resources not available ({type(e).__name__})")

if __name__ == "__main__":
    asyncio.run(run())
