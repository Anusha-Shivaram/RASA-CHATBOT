# Healthcare Chatbot Makefile
# GitHub Repository: https://github.com/user/healthcare-chatbot
# MSc AI Assignment - Project Management Automation

.PHONY: help setup install train test run clean lint format validate

# Default target
help:
	@echo "🏥 Healthcare Chatbot - Available Commands:"
	@echo ""
	@echo "📦 Setup & Installation:"
	@echo "  setup          - Complete project setup (install + train)"
	@echo "  install        - Install all dependencies"
	@echo "  install-python - Install Python dependencies only"
	@echo "  install-react  - Install React dependencies only"
	@echo ""
	@echo "🤖 Model Management:"
	@echo "  train          - Train complete Rasa model"
	@echo "  train-nlu      - Train NLU model only"
	@echo "  train-core     - Train Core model only"
	@echo ""
	@echo "🧪 Testing & Validation:"
	@echo "  test           - Run all tests"
	@echo "  test-nlu       - Test NLU accuracy"
	@echo "  test-core      - Test dialogue flows"
	@echo "  validate       - Validate training data"
	@echo ""
	@echo "🚀 Running Services:"
	@echo "  run            - Start all services (actions + rasa + react)"
	@echo "  run-actions    - Start Rasa action server only"
	@echo "  run-rasa       - Start Rasa server only"
	@echo "  run-react      - Start React development server only"
	@echo ""
	@echo "🛠️ Development Tools:"
	@echo "  lint           - Run code linting"
	@echo "  format         - Format code"
	@echo "  clean          - Clean generated files"
	@echo ""
	@echo "📊 Analysis:"
	@echo "  interactive    - Start interactive learning"
	@echo "  shell          - Start Rasa shell"
	@echo "  visualize      - Visualize training stories"

# Setup and Installation
setup: install train
	@echo "✅ Setup complete! Ready to run the chatbot."

install: install-python install-react
	@echo "✅ All dependencies installed successfully."

install-python:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Python dependencies installed."

install-react:
	@echo "📦 Installing React dependencies..."
	npm install
	@echo "✅ React dependencies installed."

# Model Training
train:
	@echo "🤖 Training complete Rasa model..."
	rasa train
	@echo "✅ Model training complete."

train-nlu:
	@echo "🧠 Training NLU model..."
	rasa train nlu
	@echo "✅ NLU training complete."

train-core:
	@echo "💬 Training Core model..."
	rasa train core
	@echo "✅ Core training complete."

# Testing and Validation
test: test-nlu test-core
	@echo "✅ All tests completed."

test-nlu:
	@echo "🧪 Testing NLU accuracy..."
	rasa test nlu --cross-validation
	@echo "📊 NLU test results available in results/"

test-core:
	@echo "🧪 Testing dialogue flows..."
	rasa test core --stories tests/test_stories.yml
	@echo "📊 Core test results available in results/"

validate:
	@echo "✅ Validating training data..."
	rasa data validate
	@echo "✅ Data validation complete."

# Running Services
run:
	@echo "🚀 Starting all services..."
	@echo "This will start three processes:"
	@echo "1. Rasa Action Server (port 5055)"
	@echo "2. Rasa Server (port 5005)"  
	@echo "3. React Dev Server (port 3000)"
	@echo ""
	@echo "Use Ctrl+C to stop all services."
	@make run-actions & make run-rasa & make run-react

run-actions:
	@echo "🎬 Starting Rasa Action Server..."
	rasa run actions --debug

run-rasa:
	@echo "🤖 Starting Rasa Server..."
	rasa run --enable-api --cors "*" --debug

run-react:
	@echo "⚛️ Starting React Development Server..."
	npm start

# Development Tools
lint:
	@echo "🔍 Running code linting..."
	flake8 actions/ --max-line-length=100
	eslint ChatInterface.js
	@echo "✅ Linting complete."

format:
	@echo "✨ Formatting code..."
	black actions/
	prettier --write ChatInterface.js ChatInterface.css
	@echo "✅ Code formatting complete."

clean:
	@echo "🧹 Cleaning generated files..."
	rm -rf models/
	rm -rf results/
	rm -rf .rasa/
	rm -rf node_modules/
	rm -rf build/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup complete."

# Analysis Tools
interactive:
	@echo "🔄 Starting interactive learning session..."
	rasa interactive

shell:
	@echo "💬 Starting Rasa shell..."
	rasa shell

visualize:
	@echo "📊 Visualizing training stories..."
	rasa visualize

# Production Deployment (optional)
build-react:
	@echo "🏗️ Building React production bundle..."
	npm run build
	@echo "✅ React build complete."

# Docker commands (optional)
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t healthcare-chatbot .
	@echo "✅ Docker image built."

docker-run:
	@echo "🐳 Running Docker container..."
	docker run -p 5005:5005 -p 5055:5055 healthcare-chatbot

# Health checks
health-check:
	@echo "🩺 Running health checks..."
	@echo "Checking Rasa server..."
	curl -f http://localhost:5005/version || echo "❌ Rasa server not responding"
	@echo "Checking Action server..."
	curl -f http://localhost:5055/health || echo "❌ Action server not responding"
	@echo "✅ Health check complete."

# Quick start for demo
demo: setup
	@echo "🎭 Starting demo mode..."
	@echo "This will:"
	@echo "1. Train the model if needed"
	@echo "2. Start all services"
	@echo "3. Open the chatbot in your browser"
	@make run

# Development workflow
dev: validate train test
	@echo "🔧 Development workflow complete."
	@echo "Ready for development. Run 'make run' to start services."

# Production workflow  
prod: clean install train test build-react
	@echo "🚀 Production build complete."
	@echo "Ready for deployment."

