from src.logger.logger import logging
from src.exception.exception import MCP_AGENT_Exception
import sys
import os

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import datetime 
from zoneinfo import ZoneInfo

import pickle


class CalendarConfig:
    
    def __init__(self):
         # Scopes
        self.scopes: list = [
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        self.credentials_path:str = os.path.join("src","config","credentials.json")
        self.creds = None 
        self.tokens_path:str = os.path.join("src","config","token.pickle")
        
        self.authenticate()
    
        self.calendar_service_build = build(serviceName="calendar",version="v3",credentials=self.creds)
    
    def authenticate(self):
        if os.path.exists(self.tokens_path):
            with open(self.tokens_path,"rb") as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file=self.credentials_path,
                    scopes=self.scopes
                )
                self.creds = flow.run_local_server(port=0)
            with open(self.tokens_path,"wb") as token:
                pickle.dump(self.creds,token)
                
    def create_calendar_service(self,summary:str,start_time,end_time,location:str=None,description:str=None):
        
        try:
            # Convert string to datetime if needed
            if isinstance(start_time, str):
                start_time = datetime.datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            if isinstance(end_time, str):
                end_time = datetime.datetime.fromisoformat(end_time.replace("Z", "+00:00"))
                
            # Set timeZone
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
            if end_time.tzinfo is None:
                end_time = end_time.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
                
            event = {
                "summary":summary,
                "start":{
                    "dateTime":start_time.isoformat(),
                    "timeZone":"Asia/Kolkata",
                        },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Asia/Kolkata',
                        },
                    }
            
            if description is not None:
                event["description"] = str(description)
            if location is not None:
                event["location"] = str(location)
            
            excuter =self.calendar_service_build.events().insert(calendarId='primary',body=event).execute()
            logging.info("Event created successfully in calendar")
            return excuter
            
        except Exception as e:
            logging.error("Error Occured in the event creation of calendar")
            raise MCP_AGENT_Exception(e,sys)
        
    def list_upcoming_events(self, max_results: int = 10):
        try:
            now_time = datetime.datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()
            upcoming_events = self.calendar_service_build.events().list(
               calendarId="primary",
                timeMin=now_time,
                maxResults = max_results,
                singleEvents=True,
                orderBy="startTime"
            ).execute()
            
            events = upcoming_events.get("items",[])
            
            if not events:
                print("No upcoming events found.")
                return []
            
            print(f"Upcoming {len(events)} events:")
            for event in events:
                start = event['start'].get('dateTime',event['start'].get('date'))
                print(f"{start}: {event['summary']}")
            return events
        
        except Exception as e:
            logging.error("Error occured during list upcoming Events")
            raise MCP_AGENT_Exception(e,sys)
        
   
    def search_events_by_description(self, search_term: str):
        try:
            now_time = datetime.datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()
            events_result = self.calendar_service_build.events().list(
                calendarId="primary",
                timeMin=now_time,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
                q=search_term
            ).execute()
            events = events_result.get("items", [])
            # Return simplified event data
            simplified_events = []
            for event in events:
                simplified_events.append({
                    "id": event.get("id"),
                    "summary": event.get("summary"),
                    "start": event.get("start", {}).get("dateTime"),
                    "description": event.get("description", "")
                })
            return simplified_events
        except Exception as e:
            logging.error("Error occurred during searching events")
            raise MCP_AGENT_Exception(e, sys)
    
    def delete_event_by_description(self, description: str):
        try:
            events = self.search_events_by_description(description)
            if not events:
                return f"No events found matching '{description}'"
            
            deleted_count = 0
            for event in events:
                if description.lower() in event.get('summary', '').lower() or description.lower() in event.get('description', '').lower():
                    self.calendar_service_build.events().delete(
                        calendarId="primary",
                        eventId=event['id']
                    ).execute()
                    deleted_count += 1
                    logging.info(f"Deleted event: {event.get('summary', 'No title')}")
            
            return f"Deleted {deleted_count} event(s) matching '{description}'"
        except Exception as e:
            logging.error("Error occurred during deleting events by description")
            raise MCP_AGENT_Exception(e, sys)
    
    def delete_calendar_event(self, event_id: str):
        try:
            self.calendar_service_build.events().delete(
                calendarId="primary",
                eventId=event_id
            ).execute()
            logging.info(f"Event with ID {event_id} deleted successfully.")
            return f"Event with ID {event_id} deleted successfully."
        except Exception as e:
            logging.error("Error occurred during deleting the calendar event")
            raise MCP_AGENT_Exception(e, sys)