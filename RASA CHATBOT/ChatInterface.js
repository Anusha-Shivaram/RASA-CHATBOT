// Healthcare Chatbot React Interface Component
// GitHub Repository: https://github.com/user/healthcare-chatbot
// MSc AI Assignment - Advanced ReactJS Frontend with Rich UI Features

import React, { useState, useEffect, useRef } from 'react';
import './ChatInterface.css'; // Assuming CSS file exists

const ChatInterface = () => {
  // State management for chat functionality
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [userSession, setUserSession] = useState(null);
  const [handoverStatus, setHandoverStatus] = useState(false);
  const [quickReplies, setQuickReplies] = useState([]);
  const [triageStatus, setTriageStatus] = useState(null);
  const messagesEndRef = useRef(null);

  // Initialize chat session
  useEffect(() => {
    initializeChat();
    scrollToBottom();
  }, [messages]);

  const initializeChat = async () => {
    try {
      // Initialize session with Rasa server
      const sessionId = generateSessionId();
      setUserSession(sessionId);
      setIsConnected(true);
      
      // Add welcome message
      addMessage({
        type: 'bot',
        text: '👋 Welcome to Healthcare Assistant! I can help you with symptom assessment, health advice, and appointment scheduling. How can I assist you today?',
        timestamp: new Date(),
        messageId: generateMessageId()
      });

      // Set initial quick replies
      setQuickReplies([
        { text: '🩺 Report Symptoms', payload: '/report_symptom' },
        { text: '📅 Book Appointment', payload: '/book_appointment' },
        { text: '💡 Health Advice', payload: '/ask_health_advice' },
        { text: '👨‍⚕️ Speak to Human', payload: '/request_human_handover' }
      ]);

    } catch (error) {
      console.error('Failed to initialize chat:', error);
      setIsConnected(false);
    }
  };

  const generateSessionId = () => {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  };

  const generateMessageId = () => {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  };

  const addMessage = (message) => {
    setMessages(prev => [...prev, { ...message, id: generateMessageId() }]);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Send message to Rasa server
  const sendMessage = async (text, payload = null) => {
    if (!text.trim() && !payload) return;

    const userMessage = {
      type: 'user',
      text: text || payload,
      timestamp: new Date(),
      messageId: generateMessageId()
    };

    addMessage(userMessage);
    setInputText('');
    setIsLoading(true);
    setQuickReplies([]);

    try {
      // Mock Rasa API call - replace with actual Rasa endpoint
      const response = await fetch('/webhooks/rest/webhook', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sender: userSession,
          message: payload || text
        })
      });

      if (response.ok) {
        const botResponses = await response.json();
        processBotResponses(botResponses);
      } else {
        throw new Error('Failed to get response from server');
      }

    } catch (error) {
      console.error('Error sending message:', error);
      addMessage({
        type: 'bot',
        text: '❌ Sorry, I encountered an error. Please try again or contact support.',
        timestamp: new Date(),
        messageId: generateMessageId(),
        isError: true
      });
    } finally {
      setIsLoading(false);
    }
  };

  const processBotResponses = (responses) => {
    responses.forEach((response, index) => {
      setTimeout(() => {
        // Handle different response types
        if (response.text) {
          addMessage({
            type: 'bot',
            text: response.text,
            timestamp: new Date(),
            messageId: generateMessageId(),
            buttons: response.buttons || null,
            attachment: response.attachment || null
          });
        }

        // Handle quick replies
        if (response.quick_replies) {
          setQuickReplies(response.quick_replies);
        }

        // Handle custom payloads
        if (response.custom) {
          handleCustomPayload(response.custom);
        }

        // Handle buttons
        if (response.buttons) {
          // Buttons are handled in message rendering
        }

      }, index * 500); // Stagger multiple responses
    });
  };

  const handleCustomPayload = (customData) => {
    // Handle triage status updates
    if (customData.triage_priority) {
      setTriageStatus({
        priority: customData.triage_priority,
        recommendation: customData.triage_recommendation,
        timestamp: new Date()
      });
    }

    // Handle handover status
    if (customData.handover_initiated) {
      setHandoverStatus(true);
      addMessage({
        type: 'system',
        text: '🔄 Connecting you with a healthcare professional...',
        timestamp: new Date(),
        messageId: generateMessageId(),
        isHandover: true
      });
    }

    // Handle appointment confirmations
    if (customData.appointment_confirmed) {
      addMessage({
        type: 'bot',
        text: `✅ Appointment confirmed! ID: ${customData.appointment_id}`,
        timestamp: new Date(),
        messageId: generateMessageId(),
        isAppointment: true,
        appointmentData: customData
      });
    }
  };

  const handleQuickReply = (quickReply) => {
    sendMessage(quickReply.title, quickReply.payload);
  };

  const handleButtonClick = (button) => {
    sendMessage(button.title, button.payload);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(inputText);
    }
  };

  const renderMessage = (message) => {
    const messageClass = `message ${message.type}`;
    const isEmergency = message.text?.includes('EMERGENCY') || message.text?.includes('🚨');
    const isHandover = message.isHandover || handoverStatus;

    return (
      <div key={message.id} className={messageClass}>
        <div className={`message-content ${isEmergency ? 'emergency' : ''} ${isHandover ? 'handover' : ''}`}>
          
          {/* Message text with rich formatting */}
          <div className="message-text">
            {formatMessageText(message.text)}
          </div>

          {/* Render buttons if present */}
          {message.buttons && (
            <div className="message-buttons">
              {message.buttons.map((button, index) => (
                <button
                  key={index}
                  className="message-button"
                  onClick={() => handleButtonClick(button)}
                >
                  {button.title}
                </button>
              ))}
            </div>
          )}

          {/* Render attachment if present */}
          {message.attachment && renderAttachment(message.attachment)}

          {/* Timestamp */}
          <div className="message-timestamp">
            {formatTimestamp(message.timestamp)}
          </div>

          {/* Triage indicator */}
          {message.type === 'bot' && triageStatus && (
            <div className={`triage-indicator priority-${triageStatus.priority}`}>
              Priority: {triageStatus.priority.toUpperCase()}
            </div>
          )}
        </div>
      </div>
    );
  };

  const formatMessageText = (text) => {
    if (!text) return '';
    
    // Convert markdown-like formatting to HTML
    let formattedText = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
      .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
      .replace(/\\n/g, '<br/>') // Line breaks
      .replace(/\n/g, '<br/>') // Line breaks
      .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'); // Links

    return <div dangerouslySetInnerHTML={{ __html: formattedText }} />;
  };

  const renderAttachment = (attachment) => {
    switch (attachment.type) {
      case 'image':
        return <img src={attachment.payload.src} alt="Attachment" className="message-image" />;
      case 'card':
        return renderCard(attachment.payload);
      case 'carousel':
        return renderCarousel(attachment.payload);
      default:
        return null;
    }
  };

  const renderCard = (cardData) => (
    <div className="message-card">
      {cardData.image_url && <img src={cardData.image_url} alt={cardData.title} />}
      <div className="card-content">
        <h4>{cardData.title}</h4>
        <p>{cardData.subtitle}</p>
        {cardData.buttons && (
          <div className="card-buttons">
            {cardData.buttons.map((button, index) => (
              <button key={index} onClick={() => handleButtonClick(button)}>
                {button.title}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );

  const renderCarousel = (carouselData) => (
    <div className="message-carousel">
      {carouselData.elements.map((element, index) => (
        <div key={index} className="carousel-item">
          {renderCard(element)}
        </div>
      ))}
    </div>
  );

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const renderConnectionStatus = () => (
    <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
      <span className="status-indicator"></span>
      {isConnected ? 'Connected' : 'Disconnected'}
      {handoverStatus && <span className="handover-status">🔄 Human Agent</span>}
    </div>
  );

  const renderTriagePanel = () => {
    if (!triageStatus) return null;

    const priorityColors = {
      low: '#28a745',
      medium: '#ffc107',
      high: '#fd7e14',
      emergency: '#dc3545'
    };

    return (
      <div className="triage-panel" style={{ borderColor: priorityColors[triageStatus.priority] }}>
        <h4>🩺 Triage Assessment</h4>
        <div className="triage-priority" style={{ color: priorityColors[triageStatus.priority] }}>
          Priority: {triageStatus.priority.toUpperCase()}
        </div>
        <div className="triage-recommendation">
          {triageStatus.recommendation}
        </div>
        <div className="triage-disclaimer">
          <small>*This assessment is for guidance only. Consult healthcare professionals for medical decisions.*</small>
        </div>
      </div>
    );
  };

  return (
    <div className="chat-interface">
      {/* Chat Header */}
      <div className="chat-header">
        <div className="header-title">
          <h2>🏥 Healthcare Assistant</h2>
          <p>AI-Powered Triage & Appointment Booking</p>
        </div>
        {renderConnectionStatus()}
      </div>

      {/* Triage Status Panel */}
      {renderTriagePanel()}

      {/* Messages Container */}
      <div className="messages-container">
        {messages.map(renderMessage)}
        
        {/* Loading indicator */}
        {isLoading && (
          <div className="message bot">
            <div className="message-content loading">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Replies */}
      {quickReplies.length > 0 && (
        <div className="quick-replies">
          {quickReplies.map((reply, index) => (
            <button
              key={index}
              className="quick-reply-button"
              onClick={() => handleQuickReply(reply)}
            >
              {reply.text}
            </button>
          ))}
        </div>
      )}

      {/* Input Area */}
      <div className="chat-input-container">
        <div className="input-wrapper">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={handoverStatus ? "Connected to human agent..." : "Type your message here..."}
            className="chat-input"
            disabled={isLoading || !isConnected}
            rows="1"
          />
          <button
            onClick={() => sendMessage(inputText)}
            disabled={!inputText.trim() || isLoading || !isConnected}
            className="send-button"
          >
            {isLoading ? '⏳' : '📤'}
          </button>
        </div>
        
        {/* Emergency Button */}
        <button
          className="emergency-button"
          onClick={() => sendMessage('This is an emergency', '/emergency_help')}
        >
          🚨 Emergency
        </button>
      </div>

      {/* Privacy Notice */}
      <div className="privacy-notice">
        <small>
          🔒 Your privacy is protected. This conversation follows GDPR/HIPAA guidelines. 
          For emergencies, call 911 immediately.
        </small>
      </div>

      {/* Feedback Widget */}
      <div className="feedback-widget">
        <button 
          className="feedback-button"
          onClick={() => sendMessage('I want to provide feedback', '/provide_feedback')}
        >
          💭 Feedback
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;

