"""
Custom MCP Server for Skills Integration
A local MCP server that provides custom tools for your project
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("skills-mcp-server")

# Create server instance
server = Server("skills-mcp-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools"""
    return [
        types.Tool(
            name="get_activities",
            description="Get all extracurricular activities",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="add_activity",
            description="Add a new extracurricular activity",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Activity name"},
                    "description": {"type": "string", "description": "Activity description"},
                    "schedule": {"type": "string", "description": "Activity schedule"},
                    "max_participants": {"type": "integer", "description": "Maximum participants"}
                },
                "required": ["name", "description", "schedule", "max_participants"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Handle tool calls"""
    
    if arguments is None:
        arguments = {}
    
    if name == "get_activities":
        # In a real implementation, this would fetch from your database
        activities = {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": 2
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM", 
                "max_participants": 20,
                "participants": 2
            }
        }
        
        return [types.TextContent(
            type="text",
            text=json.dumps(activities, indent=2)
        )]
    
    elif name == "add_activity":
        # In a real implementation, this would save to your database
        activity_data = {
            "name": arguments.get("name", ""),
            "description": arguments.get("description", ""),
            "schedule": arguments.get("schedule", ""),
            "max_participants": arguments.get("max_participants", 0),
            "participants": []
        }
        
        return [types.TextContent(
            type="text",
            text=f"Successfully added activity: {json.dumps(activity_data, indent=2)}"
        )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="skills-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
