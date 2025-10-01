# Healthcare Chatbot Actions Package - Simplified Version
# GitHub Repository: https://github.com/user/healthcare-chatbot
# MSc AI Assignment - Custom Actions Module

"""
Healthcare Chatbot Actions Package - Simplified Demo

This package contains basic custom actions for the healthcare chatbot demo.
"""

__version__ = "1.0.0-simple"
__author__ = "Healthcare Chatbot Team"
__description__ = "Simple Healthcare Chatbot Actions"

# Import only the actions that exist in our simplified version
from .actions import (
    ActionPerformTriage,
    ActionBookAppointment,
    ActionEmergencyProtocol
)

__all__ = [
    "ActionPerformTriage",
    "ActionBookAppointment", 
    "ActionEmergencyProtocol"
]