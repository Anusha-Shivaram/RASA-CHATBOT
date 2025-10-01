from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionPerformTriage(Action):
    def name(self) -> Text:
        return "action_perform_triage"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Based on your symptoms, I recommend seeing a doctor.")
        return []

class ActionBookAppointment(Action):
    def name(self) -> Text:
        return "action_book_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="I've scheduled an appointment for you. You'll receive confirmation shortly.")
        return []

class ActionEmergencyProtocol(Action):
    def name(self) -> Text:
        return "action_emergency_protocol"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="🚨 This is a medical emergency. Please call 911 immediately!")
        return []
