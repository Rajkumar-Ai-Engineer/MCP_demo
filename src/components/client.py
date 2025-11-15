import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient


async def process_request(input_string):
    """Process MCP request and return response"""
    # Configure Groq model with token limits
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
        max_tokens=1000,
        max_retries=2
    )

    # Use both mail and calendar servers
    client = MultiServerMCPClient(
        {"mail": {
            "transport": "stdio",
            "command": "python",
            "args": ["c:\\3 MONTH INTERNSHIP\\MCP\\MCP_TEST1\\src\\servers\\mail_mcp.py"],
        },
            "calendar": {
                "transport": "stdio",
                "command": "python",    
                "args": ["c:\\3 MONTH INTERNSHIP\\MCP\\MCP_TEST1\\src\\servers\\calendar_server.py"],
            }
        }
    )
    
    tools = await client.get_tools()
    agent = create_agent(llm, tools)
    response = await agent.ainvoke({"messages": input_string})
    # Extract only the final AI message content
    final_message = response["messages"][-1]
    if hasattr(final_message, 'content'):
        return final_message.content
    else:
        return str(final_message)

async def main(input_string):
    result = await process_request(input_string)
    print(result)
    return result

if __name__ == "__main__":
    input_string = input("Enter your request: ")
    asyncio.run(main(input_string))
    

