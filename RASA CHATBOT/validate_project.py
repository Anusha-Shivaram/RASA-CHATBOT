#!/usr/bin/env python3
"""
Healthcare Chatbot Project Validator
GitHub Repository: https://github.com/user/health88care-chatbot
MSc AI Assignment - Comprehensive Project Validation

This script validates the healthcare chatbot project structure and content
without requiring a full Rasa installation.
"""

import os
import yaml
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

def print_header(title: str):
    """Print formatted section header"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_success(message: str):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message: str):
    """Print error message"""
    print(f"❌ {message}")

def print_warning(message: str):
    """Print warning message"""
    print(f"⚠️  {message}")

def validate_file_structure():
    """Validate project file structure"""
    print_header("PROJECT STRUCTURE VALIDATION")
    
    required_files = [
        "domain.yml",
        "config.yml", 
        "data/nlu.yml",
        "data/stories.yml",
        "data/rules.yml",
        "actions/actions.py",
        "actions/__init__.py",
        "tests/test_nlu.yml",
        "tests/test_stories.yml",
        "ChatInterface.js",
        "ChatInterface.css",
        "README.md",
        "requirements.txt",
        "endpoints.yml",
        "credentials.yml"
    ]
    
    required_dirs = [
        "actions",
        "data", 
        "tests"
    ]
    
    # Check directories
    for directory in required_dirs:
        if os.path.exists(directory):
            print_success(f"Directory exists: {directory}/")
        else:
            print_error(f"Missing directory: {directory}/")
    
    # Check files
    for file_path in required_files:
        if os.path.exists(file_path):
            print_success(f"File exists: {file_path}")
        else:
            print_error(f"Missing file: {file_path}")

def validate_yaml_files():
    """Validate YAML file syntax"""
    print_header("YAML SYNTAX VALIDATION")
    
    yaml_files = [
        "domain.yml",
        "config.yml",
        "data/nlu.yml", 
        "data/stories.yml",
        "data/rules.yml",
        "tests/test_nlu.yml",
        "tests/test_stories.yml",
        "endpoints.yml",
        "credentials.yml"
    ]
    
    for yaml_file in yaml_files:
        if os.path.exists(yaml_file):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
                print_success(f"Valid YAML syntax: {yaml_file}")
            except yaml.YAMLError as e:
                print_error(f"Invalid YAML syntax in {yaml_file}: {e}")
            except Exception as e:
                print_error(f"Error reading {yaml_file}: {e}")
        else:
            print_warning(f"File not found: {yaml_file}")

def validate_domain_content():
    """Validate domain.yml content"""
    print_header("DOMAIN CONTENT VALIDATION")
    
    if not os.path.exists("domain.yml"):
        print_error("domain.yml not found")
        return
    
    try:
        with open("domain.yml", 'r', encoding='utf-8') as f:
            domain = yaml.safe_load(f)
        
        # Check required sections
        required_sections = ["intents", "entities", "slots", "responses", "actions"]
        for section in required_sections:
            if section in domain:
                count = len(domain[section]) if isinstance(domain[section], (list, dict)) else 1
                print_success(f"Domain has {section}: {count} items")
            else:
                print_error(f"Missing domain section: {section}")
        
        # Check specific healthcare intents
        healthcare_intents = [
            "greet", "report_symptom", "book_appointment", "emergency_help",
            "ask_health_advice", "request_human_handover"
        ]
        
        if "intents" in domain:
            existing_intents = domain["intents"]
            for intent in healthcare_intents:
                if intent in existing_intents:
                    print_success(f"Healthcare intent found: {intent}")
                else:
                    print_warning(f"Missing healthcare intent: {intent}")
    
    except Exception as e:
        print_error(f"Error validating domain.yml: {e}")

def validate_nlu_content():
    """Validate NLU training data"""
    print_header("NLU TRAINING DATA VALIDATION")
    
    if not os.path.exists("data/nlu.yml"):
        print_error("data/nlu.yml not found")
        return
    
    try:
        with open("data/nlu.yml", 'r', encoding='utf-8') as f:
            nlu_data = yaml.safe_load(f)
        
        if "nlu" not in nlu_data:
            print_error("No 'nlu' section found in nlu.yml")
            return
        
        # Count training examples by intent
        intent_counts = {}
        entity_counts = {}
        
        for item in nlu_data["nlu"]:
            if "intent" in item and "examples" in item:
                intent = item["intent"]
                examples = item["examples"].split('\n') if isinstance(item["examples"], str) else []
                examples = [ex.strip() for ex in examples if ex.strip() and not ex.strip().startswith('#')]
                
                intent_counts[intent] = len(examples)
                
                # Count entities in examples
                for example in examples:
                    if '[' in example and '](' in example:
                        # Simple entity counting
                        entity_count = example.count('[')
                        entity_counts[intent] = entity_counts.get(intent, 0) + entity_count
        
        # Report results
        total_examples = sum(intent_counts.values())
        print_success(f"Total training examples: {total_examples}")
        
        if total_examples >= 100:
            print_success("✨ Exceeds 100+ training examples requirement!")
        else:
            print_warning(f"Only {total_examples} examples (target: 100+)")
        
        # Show intent breakdown
        for intent, count in intent_counts.items():
            if count >= 5:
                print_success(f"Intent '{intent}': {count} examples")
            else:
                print_warning(f"Intent '{intent}': {count} examples (low)")
        
        # Entity statistics
        total_entities = sum(entity_counts.values())
        print_success(f"Total entity annotations: {total_entities}")
    
    except Exception as e:
        print_error(f"Error validating NLU data: {e}")

def validate_actions_code():
    """Validate custom actions code"""
    print_header("CUSTOM ACTIONS VALIDATION")
    
    if not os.path.exists("actions/actions.py"):
        print_error("actions/actions.py not found")
        return
    
    try:
        with open("actions/actions.py", 'r', encoding='utf-8') as f:
            actions_code = f.read()
        
        # Check for required imports
        required_imports = [
            "from rasa_sdk import Action",
            "from rasa_sdk.executor import CollectingDispatcher", 
            "from rasa_sdk.events import SlotSet"
        ]
        
        for import_stmt in required_imports:
            if import_stmt in actions_code:
                print_success(f"Found required import: {import_stmt.split()[-1]}")
            else:
                print_warning(f"Missing import: {import_stmt}")
        
        # Check for custom action classes
        healthcare_actions = [
            "ActionPerformTriage",
            "ActionBookAppointment", 
            "ActionProvideHealthAdvice",
            "ActionInitiateHandover",
            "ActionEmergencyProtocol"
        ]
        
        for action in healthcare_actions:
            if f"class {action}" in actions_code:
                print_success(f"Found healthcare action: {action}")
            else:
                print_warning(f"Missing action class: {action}")
        
        # Check for advanced features
        advanced_features = [
            "explainable", "triage", "GDPR", "HIPAA", 
            "emergency", "handover", "mock"
        ]
        
        found_features = []
        for feature in advanced_features:
            if feature.lower() in actions_code.lower():
                found_features.append(feature)
        
        if found_features:
            print_success(f"Advanced features found: {', '.join(found_features)}")
        else:
            print_warning("No advanced healthcare features detected")
    
    except Exception as e:
        print_error(f"Error validating actions code: {e}")

def validate_frontend_code():
    """Validate React frontend code"""
    print_header("FRONTEND CODE VALIDATION")
    
    if not os.path.exists("ChatInterface.js"):
        print_error("ChatInterface.js not found")
        return
    
    try:
        with open("ChatInterface.js", 'r', encoding='utf-8') as f:
            frontend_code = f.read()
        
        # Check for React components and features
        react_features = [
            "import React",
            "useState",
            "useEffect", 
            "ChatInterface",
            "sendMessage",
            "triage",
            "emergency",
            "handover"
        ]
        
        for feature in react_features:
            if feature in frontend_code:
                print_success(f"React feature found: {feature}")
            else:
                print_warning(f"Missing React feature: {feature}")
        
        # Check CSS file
        if os.path.exists("ChatInterface.css"):
            with open("ChatInterface.css", 'r', encoding='utf-8') as f:
                css_code = f.read()
            
            css_features = [
                ".chat-interface",
                ".message",
                ".emergency",
                ".triage",
                "responsive",
                "@media"
            ]
            
            for feature in css_features:
                if feature in css_code:
                    print_success(f"CSS feature found: {feature}")
                else:
                    print_warning(f"Missing CSS feature: {feature}")
    
    except Exception as e:
        print_error(f"Error validating frontend code: {e}")

def validate_test_coverage():
    """Validate test file coverage"""
    print_header("TEST COVERAGE VALIDATION")
    
    test_files = ["tests/test_nlu.yml", "tests/test_stories.yml"]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    test_data = yaml.safe_load(f)
                
                if "test_cases" in test_data:
                    test_count = len(test_data["test_cases"])
                    print_success(f"{test_file}: {test_count} test cases")
                elif "nlu" in test_data:
                    test_count = len(test_data["nlu"])
                    print_success(f"{test_file}: {test_count} NLU tests")
                else:
                    print_warning(f"{test_file}: Unknown test format")
            
            except Exception as e:
                print_error(f"Error reading {test_file}: {e}")
        else:
            print_error(f"Test file not found: {test_file}")

def validate_documentation():
    """Validate documentation quality"""
    print_header("DOCUMENTATION VALIDATION")
    
    if os.path.exists("README.md"):
        with open("README.md", 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        doc_sections = [
            "Installation", "Usage", "Testing", "Features",
            "Healthcare", "Triage", "GDPR", "HIPAA"
        ]
        
        for section in doc_sections:
            if section.lower() in readme_content.lower():
                print_success(f"Documentation section found: {section}")
            else:
                print_warning(f"Missing documentation section: {section}")
        
        # Check length
        word_count = len(readme_content.split())
        if word_count > 1000:
            print_success(f"Comprehensive documentation: {word_count} words")
        else:
            print_warning(f"Documentation might be too brief: {word_count} words")
    else:
        print_error("README.md not found")

def generate_test_report():
    """Generate final test report"""
    print_header("PROJECT VALIDATION SUMMARY")
    
    # Count files
    total_files = 0
    existing_files = 0
    
    all_files = [
        "domain.yml", "config.yml", "data/nlu.yml", "data/stories.yml", 
        "data/rules.yml", "actions/actions.py", "tests/test_nlu.yml",
        "tests/test_stories.yml", "ChatInterface.js", "ChatInterface.css",
        "README.md", "requirements.txt"
    ]
    
    for file_path in all_files:
        total_files += 1
        if os.path.exists(file_path):
            existing_files += 1
    
    completion_rate = (existing_files / total_files) * 100
    
    print(f"📊 Project Completion: {existing_files}/{total_files} files ({completion_rate:.1f}%)")
    
    if completion_rate >= 90:
        print_success("🎉 Excellent! Project is nearly complete")
    elif completion_rate >= 70:
        print_success("👍 Good progress! Minor files missing")
    elif completion_rate >= 50:
        print_warning("⚠️  Moderate progress. Several files need attention")
    else:
        print_error("❌ Significant work needed")
    
    print("\n📋 NEXT STEPS:")
    print("1. Fix any validation errors shown above")
    print("2. Install Rasa when ready: pip install rasa[full]==3.6.0")  
    print("3. Train model: rasa train")
    print("4. Run tests: rasa test")
    print("5. Start services: rasa run actions & rasa run")

if __name__ == "__main__":
    print("🏥 Healthcare Chatbot Project Validator")
    print("MSc AI Assignment - Comprehensive Validation")
    print("="*60)
    
    try:
        validate_file_structure()
        validate_yaml_files()
        validate_domain_content()
        validate_nlu_content()
        validate_actions_code()
        validate_frontend_code()
        validate_test_coverage()
        validate_documentation()
        generate_test_report()
        
        print("\n✅ Validation complete! Check results above.")
        
    except Exception as e:
        print_error(f"Validation failed: {e}")
        sys.exit(1)

