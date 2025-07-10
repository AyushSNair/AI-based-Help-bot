import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

const botAvatar = (
  <div className="avatar bot-avatar">
    <svg width="36" height="36" viewBox="0 0 36 36" fill="none"><circle cx="18" cy="18" r="18" fill="#0072c6"/><text x="50%" y="55%" textAnchor="middle" fill="#fff" fontSize="18" fontFamily="Arial" dy=".3em">🤖</text></svg>
  </div>
);
const userAvatar = (
  <div className="avatar user-avatar">
    <svg width="36" height="36" viewBox="0 0 36 36" fill="none"><circle cx="18" cy="18" r="18" fill="#fbb034"/><text x="50%" y="55%" textAnchor="middle" fill="#fff" fontSize="18" fontFamily="Arial" dy=".3em">🧑</text></svg>
  </div>
);

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! Ask me anything about the MOSDAC portal or satellite data." }
  ]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMessage = { sender: "user", text: input };
    setMessages((msgs) => [...msgs, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/query", { query: input });
      setMessages((msgs) => [
        ...msgs,
        { sender: "bot", text: res.data.answer }
      ]);
    } catch (err) {
      setMessages((msgs) => [
        ...msgs,
        { sender: "bot", text: "Sorry, there was an error contacting the backend." }
      ]);
    }
    setLoading(false);
  };

  return (
    <div className="modern-bg">
      <div className="chat-container glass">
        <h1>MOSDAC AI Help Bot</h1>
        <div className="chat-box">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`chat-row ${msg.sender === "user" ? "chat-row-user" : "chat-row-bot"}`}
            >
              {msg.sender === "bot" && botAvatar}
              <div
                className={`chat-bubble modern-bubble ${msg.sender === "user" ? "user-bubble" : "bot-bubble"}`}
                style={{ animationDelay: `${idx * 60}ms` }}
              >
                <ReactMarkdown>{msg.text}</ReactMarkdown>
              </div>
              {msg.sender === "user" && userAvatar}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
        <form className="chat-input-row floating-input" onSubmit={sendMessage}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your question and press Enter..."
            disabled={loading}
          />
          <button type="submit" disabled={loading || !input.trim()}>
            {loading ? "..." : "Send"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;