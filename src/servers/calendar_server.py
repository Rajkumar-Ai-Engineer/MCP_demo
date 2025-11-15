from src.logger.logger import logging 
from src.exception.exception import MCP_AGENT_Exception
import sys 
import datetime
from zoneinfo import ZoneInfo

from src.config.calendar_config import CalendarConfig

from mcp.server.fastmcp import FastMCP 


mcp = FastMCP("Calendar")

@mcp.tool()
def create_calendar_event(summary: str, start_time: str, end_time: str, location: str = None, description: str = None):
    try:
        calendar_client = CalendarConfig()
        response = calendar_client.create_calendar_service(
            summary=summary,
            start_time=start_time,
            end_time=end_time,
            location=location,
            description=description
        )
        return response
    except Exception as e:
        raise MCP_AGENT_Exception(e, sys)
    
@mcp.tool()
def list_upcoming_events(max_results: int = 10):
    """List upcoming calendar events"""
    try:
        # Convert to int to handle string inputs from LLM
        if isinstance(max_results, str):
            max_results = int(max_results)
        elif max_results is None:
            max_results = 10
        
        calendar_client = CalendarConfig()
        events = calendar_client.list_upcoming_events(max_results=max_results)
        return events
    except ValueError:
        # If conversion fails, use default
        max_results = 10
        calendar_client = CalendarConfig()
        events = calendar_client.list_upcoming_events(max_results=max_results)
        return events
    except Exception as e:
        raise MCP_AGENT_Exception(e, sys)
    
@mcp.tool()
def search_calendar_events(search_term: str):
    """Search for calendar events by description or title"""
    try:
        calendar_client = CalendarConfig()
        events = calendar_client.search_events_by_description(search_term)
        return events
    except Exception as e:
        raise MCP_AGENT_Exception(e, sys)

@mcp.tool()
def delete_calendar_event_by_description(description: str):
    """Delete calendar events that match the given description"""
    try:
        calendar_client = CalendarConfig()
        response = calendar_client.delete_event_by_description(description)
        return response
    except Exception as e:
        raise MCP_AGENT_Exception(e, sys)

@mcp.tool()
def delete_calendar_event(event_id: str):
    """Delete a calendar event by its exact event ID"""
    try:
        calendar_client = CalendarConfig()
        response = calendar_client.delete_calendar_event(event_id)
        return response
    except Exception as e:
        raise MCP_AGENT_Exception(e, sys)
    

if __name__ == "__main__":
    mcp.run(transport="stdio")