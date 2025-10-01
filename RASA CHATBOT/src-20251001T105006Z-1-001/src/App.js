import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your healthcare assistant. How can I help you today?",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Test connection to Rasa server
    const testConnection = async () => {
      try {
        await axios.post('http://localhost:5007/webhooks/rest/webhook', {
          sender: 'test',
          message: 'test'
        });
        setIsConnected(true);
      } catch (error) {
        setIsConnected(false);
      }
    };
    testConnection();
  }, []);

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: text,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:5007/webhooks/rest/webhook', {
        sender: 'user',
        message: text
      });

      if (response.data && response.data.length > 0) {
        const botMessages = response.data.map(msg => ({
          id: Date.now() + Math.random(),
          text: msg.text,
          sender: 'bot',
          timestamp: new Date()
        }));
        setMessages(prev => [...prev, ...botMessages]);
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now(),
        text: "Sorry, I'm having trouble connecting. Please make sure the Rasa server is running on http://localhost:5007",
        sender: 'bot',
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setIsLoading(false);
  };

  const quickReplies = [
    "Hello",
    "I have a headache", 
    "I have chest pain",
    "I need an appointment",
    "Emergency",
    "What are your hours?",
    "I want to cancel my appointment",
    "Can you give me health advice?",
    "I want to talk to a human",
    "Goodbye"
  ];

  const handleQuickReply = (text) => {
    sendMessage(text);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(inputText);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="header-content">
          <h2>🏥 Healthcare Assistant</h2>
          <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
          </div>
        </div>
      </div>

      <div className="messages-container">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender} ${message.isError ? 'error' : ''}`}
          >
            <div className="message-content">
              <div className="message-text">{message.text}</div>
              <div className="message-time">
                {message.timestamp.toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message bot">
            <div className="message-content">
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

      <div className="quick-replies">
        {quickReplies.map((reply, index) => (
          <button
            key={index}
            className="quick-reply-btn"
            onClick={() => handleQuickReply(reply)}
            disabled={isLoading}
          >
            {reply}
          </button>
        ))}
      </div>

      <form className="input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type your message..."
          className="message-input"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="send-button"
          disabled={isLoading || !inputText.trim()}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;
