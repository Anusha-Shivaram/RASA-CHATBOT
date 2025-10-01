# 🏥 Healthcare Chatbot - Complete Setup & Testing Guide

## ✅ Requirements Cross-Check

### MSc Assignment Requirements Status:
- ✅ **Rasa Open Source Implementation** - Complete with NLU, dialogue management
- ✅ **Custom Actions** - Triage, appointment booking, emergency protocol
- ✅ **NLU Training Data** - 40+ examples across 5 core intents
- ✅ **Dialogue Stories** - Happy path conversations implemented
- ✅ **ReactJS Frontend** - Custom UI component ready
- ✅ **Testing Framework** - HTTP API testing commands provided
- ✅ **Code Quality** - Well-commented, structured codebase
- ✅ **Innovation Features** - Triage logic, emergency detection

---

## 🚀 STEP 1: Installation & Setup

### Prerequisites
```powershell
# Ensure Python 3.8+ and Node.js are installed
python --version
node --version
```

### Install Dependencies
```powershell
# Install Rasa and dependencies
pip install rasa==3.6.0 rasa-sdk==3.6.0

# For React frontend (if testing browser)
npm install react react-dom axios
```

---

## 🎯 STEP 2: Start the Chatbot Servers

### Terminal 1: Start Action Server
```powershell
cd C:\Users\Talha\Desktop\Rasaa
rasa run actions
```
**Expected Output:** 
```
2025-09-27 14:45:32 INFO     rasa_sdk.endpoint  - Starting action endpoint server...
2025-09-27 14:45:32 INFO     rasa_sdk.endpoint  - Action endpoint is up and running on http://localhost:5005
```

### Terminal 2: Start Rasa HTTP Server
```powershell
cd C:\Users\Talha\Desktop\Rasaa
rasa run --enable-api --cors "*" --port 5007
```
**Expected Output:**
```
2025-09-27 14:45:45 INFO     rasa.core.agent  - Loading model models/...
2025-09-27 14:45:46 INFO     rasa.core.agent  - Agent loaded. Type a message and press enter (use '/stop' to exit).
2025-09-27 14:45:46 INFO     rasa.server  - Starting Rasa server on http://localhost:5007
```

---

## 🧪 STEP 3: Test All Functionalities via HTTP API

### Test 1: Greeting
```powershell
Invoke-RestMethod -Uri "http://localhost:5007/webhooks/rest/webhook" -Method Post -ContentType "application/json" -Body '{"sender": "test_user", "message": "hello"}'
```
**Expected Response:**
```
recipient_id text
------------ ----
test_user    Hello! I'm your healthcare assistant. How can I help you today?
```

### Test 2: Symptom Reporting & Triage
```powershell
Invoke-RestMethod -Uri "http://localhost:5007/webhooks/rest/webhook" -Method Post -ContentType "application/json" -Body '{"sender": "test_user", "message": "I have a headache"}'
```
**Expected Response:**
```
recipient_id text
------------ ----
test_user    Based on your symptoms, I recommend seeing a doctor.
```

### Test 3: Appointment Booking
```powershell
Invoke-RestMethod -Uri "http://localhost:5007/webhooks/rest/webhook" -Method Post -ContentType "application/json" -Body '{"sender": "test_user", "message": "I need an appointment"}'
```
**Expected Response:**
```
recipient_id text
------------ ----
test_user    I've scheduled an appointment for you. You'll receive confirmation shortly.
```

### Test 4: Emergency Protocol
```powershell
Invoke-RestMethod -Uri "http://localhost:5007/webhooks/rest/webhook" -Method Post -ContentType "application/json" -Body '{"sender": "test_user", "message": "emergency"}'
```
**Expected Response:**
```
recipient_id text
------------ ----
test_user    🚨 This is a medical emergency. Please call 911 immediately!
```

### Test 5: Goodbye
```powershell
Invoke-RestMethod -Uri "http://localhost:5007/webhooks/rest/webhook" -Method Post -ContentType "application/json" -Body '{"sender": "test_user", "message": "goodbye"}'
```
**Expected Response:**
```
recipient_id text
------------ ----
test_user    Thank you for using our healthcare service. Take care!
```

---

## 🌐 STEP 4: Browser Testing with React Frontend

### Setup React Development Server
```powershell
# Terminal 3: Start React Dev Server
cd C:\Users\Talha\Desktop\Rasaa
npx create-react-app healthcare-chatbot-ui --template minimal
cd healthcare-chatbot-ui
npm start
```

### Replace App.js with ChatInterface
```powershell
# Copy the ChatInterface.js content to src/App.js
# Copy the ChatInterface.css content to src/App.css
```

### Access in Browser
- Open: http://localhost:3000
- Test all functionalities through the UI
- Verify quick replies, rich cards, and handover indicators work

---

## 🔧 STEP 5: Troubleshooting Commands

### Clear Cache (if training issues)
```powershell
Remove-Item -Recurse -Force .rasa
rasa train --config config_simple.yml
```

### Kill Existing Processes (if port conflicts)
```powershell
taskkill /f /im python.exe
taskkill /f /im node.exe
```

### Check Port Usage
```powershell
netstat -an | findstr :5005  # Action server
netstat -an | findstr :5007  # HTTP server  
netstat -an | findstr :3000  # React dev server
```

### Validate Project Structure
```powershell
python validate_project.py
```

---

## 📊 STEP 6: Performance Testing & Validation

### NLU Testing
```powershell
rasa test nlu --config config_simple.yml
```

### Conversation Testing
```powershell
rasa test core --stories tests/test_stories.yml
```

### API Load Testing (Optional)
```powershell
# Multiple concurrent requests
for ($i=1; $i -le 10; $i++) {
    Invoke-RestMethod -Uri "http://localhost:5007/webhooks/rest/webhook" -Method Post -ContentType "application/json" -Body "{`"sender`": `"user$i`", `"message`": `"hello`"}"
}
```

---

## 🎯 Success Criteria

✅ **All 5 HTTP tests pass with expected responses**  
✅ **Action server running on port 5005**  
✅ **HTTP server running on port 5007**  
✅ **React frontend accessible on port 3000**  
✅ **No error messages in server logs**  
✅ **Conversation flows work end-to-end**

---

## 📝 Assignment Submission Checklist

- ✅ Complete Rasa project structure
- ✅ Working custom actions (3 core actions)
- ✅ NLU training data (40+ examples)
- ✅ Dialogue stories and rules
- ✅ ReactJS frontend component
- ✅ HTTP API functionality
- ✅ Testing documentation
- ✅ Code comments and documentation
- ✅ Innovation features (triage logic, emergency detection)

---

## 🚨 Quick Start Commands (Copy & Paste)

```powershell
# Terminal 1
cd C:\Users\Talha\Desktop\Rasaa
rasa run actions

# Terminal 2 (new window)
cd C:\Users\Talha\Desktop\Rasaa  
rasa run --enable-api --cors "*" --port 5007

# Terminal 3 (test)
Invoke-RestMethod -Uri "http://localhost:5007/webhooks/rest/webhook" -Method Post -ContentType "application/json" -Body '{"sender": "test", "message": "hello"}'
```

Your healthcare chatbot is now fully functional and ready for demonstration! 🎉
