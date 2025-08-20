# rasa_bot/actions/actions.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
import requests
import json

class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Custom behavior when session starts
        events = [SessionStarted()]
        
        # Add any custom logic here for session start
        dispatcher.utter_message(response="utter_greet")
        
        events.append(ActionExecuted("action_listen"))
        return events

class ActionGetCovidStats(Action):
    def name(self) -> Text:
        return "action_get_covid_stats"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # This is a placeholder - in a real implementation, you would call a COVID API
        try:
            # Example API call (replace with actual COVID API)
            # response = requests.get("https://api.covid19api.com/summary")
            # data = response.json()
            
            # For demo purposes, we'll use mock data
            stats_message = "Current COVID-19 statistics (sample data):\n" \
                           "Global Cases: 676.9M\n" \
                           "Global Deaths: 6.88M\n" \
                           "Global Recovered: 652.2M\n" \
                           "Data updated: March 2023"
            
            dispatcher.utter_message(text=stats_message)
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I couldn't retrieve COVID statistics at the moment.")
        
        return []

class ActionProvideITTicket(Action):
    def name(self) -> Text:
        return "action_provide_it_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Generate a mock ticket number
        import random
        ticket_number = f"IT{random.randint(10000, 99999)}"
        
        dispatcher.utter_message(
            text=f"I've created a ticket for your issue: #{ticket_number}. " \
                 "Our IT team will contact you within 24 hours. " \
                 "You can also call our helpdesk at 555-1234 for immediate assistance."
        )
        
        return []

class ActionFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Custom fallback action
        dispatcher.utter_message(
            text="I'm sorry, I didn't quite understand that. " \
                 "I'm a specialized assistant for medical FAQs and IT helpdesk questions. " \
                 "How can I help you with COVID-19 information or IT issues?"
        )
        
        return []
    