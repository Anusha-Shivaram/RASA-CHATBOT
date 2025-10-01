#!/bin/bash
# Healthcare Chatbot Testing Script
# GitHub Repository: https://github.com/user/healthcare-chatbot
# MSc AI Assignment - Comprehensive Testing Commands

echo "🏥 Healthcare Chatbot - Comprehensive Testing Suite"
echo "=================================================="

# Phase 1: Setup Verification
echo "📋 Phase 1: Setup Verification"
echo "------------------------------"
echo "1. Checking Python version..."
python --version

echo "2. Installing dependencies..."
pip install -r requirements.txt

echo "3. Verifying Rasa installation..."
rasa --version

# Phase 2: Data Validation
echo ""
echo "✅ Phase 2: Data Validation"
echo "---------------------------"
echo "4. Validating training data..."
rasa data validate

echo "5. Checking data consistency..."
rasa data validate --max-history 5

# Phase 3: Model Training
echo ""
echo "🤖 Phase 3: Model Training"
echo "--------------------------"
echo "6. Training complete model..."
rasa train

# Phase 4: NLU Testing
echo ""
echo "🧠 Phase 4: NLU Testing (Target: >90% Accuracy)"
echo "------------------------------------------------"
echo "7. Running NLU cross-validation tests..."
rasa test nlu --cross-validation --runs 3

echo "8. Testing NLU against test data..."
rasa test nlu --nlu tests/test_nlu.yml

echo "9. Generating detailed NLU report..."
rasa test nlu --cross-validation --percentages 80 20

# Phase 5: Core Testing
echo ""
echo "💬 Phase 5: Core/Dialogue Testing"
echo "----------------------------------"
echo "10. Testing dialogue flows..."
rasa test core --stories tests/test_stories.yml

echo "11. End-to-end conversation testing..."
rasa test --stories tests/test_stories.yml

# Phase 6: Performance Analysis
echo ""
echo "📊 Phase 6: Performance Analysis"
echo "--------------------------------"
echo "12. Analyzing test results..."
if [ -d "results" ]; then
    echo "NLU Results:"
    find results -name "*report*" -type f | head -5
    echo ""
    echo "Core Results:"
    find results -name "*core*" -type f | head -5
else
    echo "No results directory found. Tests may not have completed successfully."
fi

# Phase 7: Server Health Check
echo ""
echo "🩺 Phase 7: Server Health Check"
echo "-------------------------------"
echo "13. Starting action server in background..."
rasa run actions &
ACTION_PID=$!
sleep 5

echo "14. Testing action server health..."
curl -f http://localhost:5055/health || echo "❌ Action server not responding"

echo "15. Starting Rasa server in background..."
rasa run --enable-api --cors "*" &
RASA_PID=$!
sleep 10

echo "16. Testing Rasa API endpoint..."
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "test_user", "message": "hello"}' || echo "❌ Rasa server not responding"

# Cleanup background processes
kill $ACTION_PID $RASA_PID 2>/dev/null

echo ""
echo "✅ Testing Complete!"
echo "==================="
echo "Check the results/ directory for detailed test reports."
echo "Key files to review:"
echo "- results/intent_report.json (NLU accuracy)"
echo "- results/story_report.json (Dialogue success)"
echo "- results/failed_test_stories.yml (Failed cases)"
echo ""
echo "Next steps:"
echo "1. Review test results"
echo "2. Fix any failed tests"
echo "3. Run 'make run' to start all services"
echo "4. Test the React frontend at http://localhost:3000"

