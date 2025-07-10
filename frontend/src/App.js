import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

const botAvatar = (
  <div className="avatar bot-avatar">
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
      <circle cx="16" cy="16" r="16" fill="#2563eb"/>
      <path d="M12 14c0-.55.45-1 1-1s1 .45 1 1-.45 1-1 1-1-.45-1-1zm6 0c0-.55.45-1 1-1s1 .45 1 1-.45 1-1 1-1-.45-1-1zm-3 4c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2z" fill="#fff"/>
    </svg>
  </div>
);

const userAvatar = (
  <div className="avatar user-avatar">
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
      <circle cx="16" cy="16" r="16" fill="#64748b"/>
      <path d="M16 16c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="#fff"/>
    </svg>
  </div>
);

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! I'm your MOSDAC assistant. Ask me anything about satellite data, portal features, or data access." }
  ]);
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const chatEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (isOpen && !isMinimized && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen, isMinimized]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    
    const userMessage = { sender: "user", text: input };
    setMessages((msgs) => [...msgs, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/query", { query: input });
      setMessages((msgs) => [
        ...msgs,
        { sender: "bot", text: res.data.answer }
      ]);
    } catch (err) {
      setMessages((msgs) => [
        ...msgs,
        { sender: "bot", text: "Sorry, I'm having trouble connecting to my knowledge base. Please try again in a moment." }
      ]);
    }
    setLoading(false);
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    setIsMinimized(false);
  };

  const minimizeChat = () => {
    setIsMinimized(true);
  };

  const maximizeChat = () => {
    setIsMinimized(false);
  };

  return (
    <div className="app">
      {/* MOSDAC Website Screenshot - Full Display */}
      <div className="website-screenshot">
        <img src="/image.png" alt="MOSDAC Portal" className="fullscreen-screenshot" />
      </div>

      {/* Floating Chatbot */}
      <div className={`chatbot-widget ${isOpen ? 'open' : ''} ${isMinimized ? 'minimized' : ''}`}>
        {/* Chat Button */}
        {!isOpen && (
          <button className="chat-toggle-btn" onClick={toggleChat}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z" fill="currentColor"/>
              <circle cx="8" cy="10" r="1" fill="#fff"/>
              <circle cx="12" cy="10" r="1" fill="#fff"/>
              <circle cx="16" cy="10" r="1" fill="#fff"/>
            </svg>
          </button>
        )}

        {/* Chat Window */}
        {isOpen && (
          <div className="chat-window">
            {/* Chat Header */}
            <div className="chat-header">
              <div className="chat-header-info">
                {botAvatar}
                <div>
                  <h4>MOSDAC Assistant</h4>
                  <span className="status-indicator">Online</span>
                </div>
              </div>
              <div className="chat-controls">
                <button className="control-btn" onClick={minimizeChat} title="Minimize">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M4 8h8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  </svg>
                </button>
                <button className="control-btn" onClick={toggleChat} title="Close">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M12 4L4 12M4 4l8 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                  </svg>
                </button>
              </div>
            </div>

            {/* Chat Messages */}
            {!isMinimized && (
              <>
                <div className="chat-messages">
                  {messages.map((msg, idx) => (
                    <div
                      key={idx}
                      className={`message ${msg.sender === "user" ? "user-message" : "bot-message"}`}
                    >
                      {msg.sender === "bot" && botAvatar}
                      <div className="message-content">
                        <ReactMarkdown>{msg.text}</ReactMarkdown>
                      </div>
                      {msg.sender === "user" && userAvatar}
                    </div>
                  ))}
                  {loading && (
                    <div className="message bot-message">
                      {botAvatar}
                      <div className="message-content">
                        <div className="typing-indicator">
                          <span></span>
                          <span></span>
                          <span></span>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={chatEndRef} />
                </div>

                {/* Chat Input */}
                <form className="chat-input" onSubmit={sendMessage}>
                  <input
                    ref={inputRef}
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask me about MOSDAC..."
                    disabled={loading}
                  />
                  <button type="submit" disabled={loading || !input.trim()}>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <path d="M18 10L2 18l4-8-4-8 16 8z" fill="currentColor"/>
                    </svg>
                  </button>
                </form>
              </>
            )}

            {/* Minimized State */}
            {isMinimized && (
              <div className="chat-minimized" onClick={maximizeChat}>
                <div className="minimized-content">
                  <span>MOSDAC Assistant</span>
                  <div className="unread-indicator">1</div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;