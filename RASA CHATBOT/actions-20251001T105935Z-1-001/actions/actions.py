from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import random
import datetime

class ActionPerformTriage(Action):
    def name(self) -> Text:
        return "action_perform_triage"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the reported symptoms
        symptoms = tracker.get_latest_entity_values("symptom")
        body_parts = tracker.get_latest_entity_values("body_part")
        
        # Emergency symptoms that require immediate attention
        emergency_symptoms = [
            "chest pain", "difficulty breathing", "shortness of breath", 
            "severe bleeding", "unconscious", "heart attack", "stroke",
            "severe head injury", "poisoning", "severe allergic reaction"
        ]
        
        # High priority symptoms
        high_priority = [
            "fever", "severe headache", "persistent vomiting", 
            "severe abdominal pain", "difficulty swallowing"
        ]
        
        # Medium priority symptoms  
        medium_priority = [
            "headache", "nausea", "fatigue", "joint pain", "muscle aches",
            "sore throat", "cough", "dizziness"
        ]
        
        # Low priority symptoms
        low_priority = [
            "minor cuts", "bruises", "mild headache", "runny nose",
            "minor rash", "mild indigestion"
        ]
        
        symptom_text = " ".join(symptoms) if symptoms else "your symptoms"
        
        # Check for emergency symptoms
        for symptom in symptoms:
            if any(emergency in symptom.lower() for emergency in emergency_symptoms):
                dispatcher.utter_message(
                    text=f"⚠️ Your symptoms ({symptom_text}) indicate a potential medical emergency. "
                         f"Please seek immediate medical attention or call 911."
                )
                return [SlotSet("triage_priority", "emergency")]
        
        # Check symptom severity and provide appropriate response
        if any(symptom.lower() in high_priority for symptom in symptoms):
            responses = [
                f"Based on your symptoms ({symptom_text}), I recommend scheduling an appointment with a healthcare provider within 24-48 hours.",
                f"Your symptoms ({symptom_text}) suggest you should see a doctor soon. Would you like me to help you book an appointment?",
                f"Given your symptoms ({symptom_text}), it's important to get medical evaluation. I can help you schedule a visit."
            ]
            priority = "high"
            
        elif any(symptom.lower() in medium_priority for symptom in symptoms):
            responses = [
                f"For your symptoms ({symptom_text}), I recommend monitoring them and consider seeing a healthcare provider if they persist or worsen.",
                f"Your symptoms ({symptom_text}) are concerning. If they don't improve in 2-3 days, please schedule an appointment.",
                f"Based on your symptoms ({symptom_text}), rest and self-care may help, but consult a doctor if symptoms persist."
            ]
            priority = "medium"
            
        else:
            responses = [
                f"Your symptoms ({symptom_text}) appear to be mild. Monitor them and seek care if they worsen or persist.",
                f"For your symptoms ({symptom_text}), try rest and basic self-care. Contact us if you have concerns.",
                f"Based on your symptoms ({symptom_text}), this seems manageable with home care, but don't hesitate to seek help if needed."
            ]
            priority = "low"
        
        # Add explanation for triage decision (Explainable AI feature)
        explanation = f"\n\n💡 **Triage Rationale**: I've assessed your symptoms as {priority} priority based on medical triage guidelines. This helps ensure appropriate care timing."
        
        selected_response = random.choice(responses) + explanation
        dispatcher.utter_message(text=selected_response)
        
        return [SlotSet("triage_priority", priority), SlotSet("last_symptoms", symptom_text)]

class ActionBookAppointment(Action):
    def name(self) -> Text:
        return "action_book_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get user's triage priority if available
        priority = tracker.get_slot("triage_priority")
        symptoms = tracker.get_slot("last_symptoms")
        
        # Generate appointment reference number
        ref_number = f"HC{random.randint(1000, 9999)}"
        
        # Calculate suggested appointment time based on priority
        now = datetime.datetime.now()
        if priority == "emergency":
            suggested_time = "immediately"
            message = f"🚨 Given the urgent nature of your condition, please go to the emergency room immediately. Reference: {ref_number}"
        elif priority == "high":
            suggested_time = (now + datetime.timedelta(days=1)).strftime("%B %d at 2:00 PM")
            message = f"✅ I've prioritized your appointment for {suggested_time} due to your symptoms. Reference: {ref_number}"
        elif priority == "medium":
            suggested_time = (now + datetime.timedelta(days=3)).strftime("%B %d at 10:00 AM")
            message = f"✅ Your appointment is scheduled for {suggested_time}. Reference: {ref_number}"
        else:
            suggested_time = (now + datetime.timedelta(days=7)).strftime("%B %d at 3:00 PM")
            message = f"✅ Your routine appointment is scheduled for {suggested_time}. Reference: {ref_number}"
        
        # Add personalized follow-up
        if symptoms:
            message += f"\n\n📋 **Appointment Notes**: We'll address your concerns about {symptoms}."
        
        message += f"\n\n📞 **Next Steps**: You'll receive a confirmation call within 2 hours. Please arrive 15 minutes early with your ID and insurance card."
        
        dispatcher.utter_message(text=message)
        
        return [
            SlotSet("appointment_reference", ref_number),
            SlotSet("appointment_time", suggested_time),
            SlotSet("appointment_booked", True)
        ]

class ActionEmergencyProtocol(Action):
    def name(self) -> Text:
        return "action_emergency_protocol"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        emergency_message = (
            "🚨 **MEDICAL EMERGENCY DETECTED** 🚨\n\n"
            "**IMMEDIATE ACTIONS:**\n"
            "1. 📞 Call 911 NOW if in the US\n"
            "2. 🏥 Go to nearest Emergency Room\n"
            "3. 👥 Don't drive yourself - call ambulance or have someone drive you\n\n"
            "**WHILE WAITING FOR HELP:**\n"
            "• Stay calm and breathe slowly\n"
            "• Don't eat or drink anything\n"
            "• Gather your medications/medical info\n"
            "• Have someone stay with you if possible\n\n"
            "**EMERGENCY CONTACTS:**\n"
            "• Emergency Services: 911\n"
            "• Poison Control: 1-800-222-1222\n"
            "• Crisis Hotline: 988\n\n"
            "⚠️ This chat cannot replace emergency medical care. Seek immediate professional help."
        )
        
        dispatcher.utter_message(text=emergency_message)
        
        return [SlotSet("emergency_triggered", True)]

class ActionProvideHealthAdvice(Action):
    def name(self) -> Text:
        return "action_provide_health_advice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        symptoms = tracker.get_slot("last_symptoms")
        
        general_advice = [
            "🏥 **General Health Recommendations:**\n"
            "• Stay hydrated - drink plenty of water\n"
            "• Get adequate rest (7-9 hours sleep)\n"
            "• Eat nutritious meals regularly\n"
            "• Take medications as prescribed\n"
            "• Monitor your symptoms and keep a health diary\n\n"
            "⚠️ **Important**: This is general guidance only. Always consult healthcare professionals for medical decisions.",
            
            "💊 **Self-Care Guidelines:**\n"
            "• Apply ice for swelling, heat for muscle tension\n"
            "• Practice stress management techniques\n"
            "• Avoid alcohol and smoking\n"
            "• Maintain good hygiene\n"
            "• Follow up with your healthcare provider\n\n"
            "📋 **When to seek immediate care**: Severe pain, difficulty breathing, chest pain, or rapidly worsening symptoms."
        ]
        
        if symptoms:
            advice_message = f"For your reported symptoms ({symptoms}), here's some guidance:\n\n" + random.choice(general_advice)
        else:
            advice_message = random.choice(general_advice)
            
        dispatcher.utter_message(text=advice_message)
        return []

class ActionCheckAppointment(Action):
    def name(self) -> Text:
        return "action_check_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        appointment_ref = tracker.get_slot("appointment_reference")
        appointment_time = tracker.get_slot("appointment_time")
        
        if appointment_ref and appointment_time:
            message = (
                f"📅 **Your Appointment Details:**\n"
                f"• Reference: {appointment_ref}\n"
                f"• Scheduled: {appointment_time}\n"
                f"• Status: Confirmed ✅\n"
                f"• Location: Main Clinic, 123 Health Street\n\n"
                f"📞 Need to make changes? Just let me know!"
            )
        else:
            message = (
                "🔍 I don't see any appointments in our system for you. "
                "Would you like to schedule one? I can help you book an appointment that fits your needs."
            )
        
        dispatcher.utter_message(text=message)
        return []

class ActionModifyAppointment(Action):
    def name(self) -> Text:
        return "action_modify_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        appointment_ref = tracker.get_slot("appointment_reference")
        
        if appointment_ref:
            # Generate new time options
            now = datetime.datetime.now()
            option1 = (now + datetime.timedelta(days=2)).strftime("%B %d at 9:00 AM")
            option2 = (now + datetime.timedelta(days=4)).strftime("%B %d at 2:00 PM")
            option3 = (now + datetime.timedelta(days=6)).strftime("%B %d at 11:00 AM")
            
            message = (
                f"📅 **Reschedule Appointment {appointment_ref}**\n\n"
                f"Available time slots:\n"
                f"1️⃣ {option1}\n"
                f"2️⃣ {option2}\n"
                f"3️⃣ {option3}\n\n"
                f"Would any of these work for you? Or let me know your preferred time."
            )
        else:
            message = (
                "❓ I don't see an existing appointment to modify. "
                "Would you like to book a new appointment instead?"
            )
        
        dispatcher.utter_message(text=message)
        return []

class ActionCancelAppointment(Action):
    def name(self) -> Text:
        return "action_cancel_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        appointment_ref = tracker.get_slot("appointment_reference")
        
        if appointment_ref:
            message = (
                f"❌ **Appointment Cancellation**\n\n"
                f"Your appointment {appointment_ref} has been cancelled.\n\n"
                f"📋 **Cancellation Details:**\n"
                f"• No cancellation fee\n"
                f"• Slot released for other patients\n"
                f"• You can rebook anytime\n\n"
                f"💙 We hope you're feeling better. Don't hesitate to reach out if you need care in the future."
            )
        else:
            message = "❓ I don't see an appointment to cancel. Is there anything else I can help you with?"
        
        dispatcher.utter_message(text=message)
        return [
            SlotSet("appointment_reference", None),
            SlotSet("appointment_time", None),
            SlotSet("appointment_booked", False)
        ]

class ActionInitiateHandover(Action):
    def name(self) -> Text:
        return "action_initiate_handover"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        symptoms = tracker.get_slot("last_symptoms")
        
        handover_message = (
            "👥 **Human Support Request**\n\n"
            "I'm connecting you with a healthcare professional who can provide personalized assistance.\n\n"
            "📋 **What I'll share with them:**\n"
        )
        
        if symptoms:
            handover_message += f"• Your reported symptoms: {symptoms}\n"
        
        handover_message += (
            "• Our conversation history\n"
            "• Any appointments or references\n\n"
            "⏱️ **Expected wait time**: 2-5 minutes\n"
            "📞 **Alternative**: Call us directly at (555) 123-CARE\n\n"
            "Please stay online while I connect you..."
        )
        
        dispatcher.utter_message(text=handover_message)
        return [SlotSet("human_handover_requested", True)]

class ActionCollectFeedback(Action):
    def name(self) -> Text:
        return "action_collect_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        feedback_message = (
            "📝 **We Value Your Feedback!**\n\n"
            "Thank you for taking the time to share your experience with our healthcare assistant.\n\n"
            "📊 **Your feedback helps us:**\n"
            "• Improve our AI responses\n"
            "• Enhance patient care\n"
            "• Train our healthcare team\n"
            "• Develop better health services\n\n"
            "🏆 **Rate our service** (1-5 stars): ⭐⭐⭐⭐⭐\n"
            "💬 **Additional comments**: Feel free to share any specific suggestions or concerns.\n\n"
            "Your feedback is confidential and helps us serve you better!"
        )
        
        dispatcher.utter_message(text=feedback_message)
        return [SlotSet("feedback_collected", True)]

