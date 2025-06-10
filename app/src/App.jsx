import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  // Helper function to format agent responses
  const formatMessage = (text) => {
    if (!text) return "";
    
    // Split by lines and process each line
    const lines = text.split('\n');
    const formattedLines = lines.map((line, index) => {
      const trimmedLine = line.trim();
      
      // Skip empty lines
      if (!trimmedLine) return null;
      
      // Handle bullet points (lines starting with -)
      if (trimmedLine.startsWith('- ')) {
        return (
          <li key={index} className="bullet-point">
            {trimmedLine.substring(2)}
          </li>
        );
      }
      // Handle nested bullet points (lines starting with spaces and -)
      if (/^\s+- /.test(line)) {
        return (
          <li key={index} className="bullet-point nested">
            {trimmedLine.substring(2)}
          </li>
        );
      }
      
      // Handle numbered points (lines starting with numbers)
      if (/^\d+\./.test(trimmedLine)) {
        return (
          <li key={index} className="numbered-point">
            {trimmedLine}
          </li>
        );
      }
      
      // Handle lettered points (lines starting with letters)
      if (/^[a-z]\. /.test(trimmedLine)) {
        return (
          <li key={index} className="lettered-point">
            {trimmedLine}
          </li>
        );
      }
      
      // Handle roman numerals
      if (/^(i|ii|iii|iv|v)\. /.test(trimmedLine)) {
        return (
          <li key={index} className="roman-point">
            {trimmedLine}
          </li>
        );
      }
      
      // Handle headers (lines that contain colons at the end or are section markers)
      if (trimmedLine.endsWith(':') || /^[A-Z\s]+:$/.test(trimmedLine) || 
          trimmedLine.startsWith('###') || trimmedLine.toUpperCase() === trimmedLine && trimmedLine.length > 3) {
        return (
          <h4 key={index} className="message-header">
            {trimmedLine.replace(/^###\s*/, '').replace(/:$/, '')}
          </h4>
        );
      }
      
      // Handle emphasis (text in quotes or parentheses)
      if ((trimmedLine.startsWith('"') && trimmedLine.endsWith('"')) ||
          (trimmedLine.startsWith('(') && trimmedLine.endsWith(')'))) {
        return (
          <p key={index} className="message-text emphasis">
            {trimmedLine}
          </p>
        );
      }
      
      // Regular text
      return (
        <p key={index} className="message-text">
          {trimmedLine}
        </p>
      );
    }).filter(Boolean);
    
    // Group consecutive list items into appropriate list elements
    const groupedElements = [];
    let currentBulletList = [];
    let currentNumberedList = [];
    
    formattedLines.forEach((element, index) => {
      if (element.type === 'li' && element.props.className.includes('bullet-point')) {
        if (currentNumberedList.length > 0) {
          groupedElements.push(
            <ol key={`ol-${index}`} className="numbered-list">
              {currentNumberedList}
            </ol>
          );
          currentNumberedList = [];
        }
        currentBulletList.push(element);
      } else if (element.type === 'li' && 
                (element.props.className.includes('numbered-point') || 
                 element.props.className.includes('lettered-point') ||
                 element.props.className.includes('roman-point'))) {
        if (currentBulletList.length > 0) {
          groupedElements.push(
            <ul key={`ul-${index}`} className="bullet-list">
              {currentBulletList}
            </ul>
          );
          currentBulletList = [];
        }
        currentNumberedList.push(element);
      } else {
        if (currentBulletList.length > 0) {
          groupedElements.push(
            <ul key={`ul-${index}`} className="bullet-list">
              {currentBulletList}
            </ul>
          );
          currentBulletList = [];
        }
        if (currentNumberedList.length > 0) {
          groupedElements.push(
            <ol key={`ol-${index}`} className="numbered-list">
              {currentNumberedList}
            </ol>
          );
          currentNumberedList = [];
        }
        groupedElements.push(element);
      }
    });
    
    // Handle any remaining list items
    if (currentBulletList.length > 0) {
      groupedElements.push(
        <ul key="ul-final" className="bullet-list">
          {currentBulletList}
        </ul>
      );
    }
    if (currentNumberedList.length > 0) {
      groupedElements.push(
        <ol key="ol-final" className="numbered-list">
          {currentNumberedList}
        </ol>
      );
    }
    
    return groupedElements;
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMessage = { user: "user", message: input };
    setMessages([...messages, { sender: "user", text: input }]);
    setInput("");
    setLoading(true);
    try {
      const res = await axios.post("/api/chat", userMessage);
      // Expecting new structure: { items: [ { text: ... } ], ... }
      if (res.data && Array.isArray(res.data.items) && res.data.items.length > 0) {
        setMessages((msgs) => [
          ...msgs,
          {
            sender: "ai",
            text: res.data.items[0].text || "No answer returned.",
            isFormatted: true
          }
        ]);
      } else {
        setMessages((msgs) => [
          ...msgs,
          { sender: "ai", text: "No answer returned.", isFormatted: false }
        ]);
      }
    } catch (err) {
      setMessages((msgs) => [
        ...msgs,
        { sender: "ai", text: "Error: Could not get answer.", isFormatted: false }
      ]);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="chat-container">
      <h2>AI Chat</h2>
      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.sender === "user" ? "user-msg" : "ai-msg"}`}>
            <div className="message-header-info">
              <strong className="sender-name">
                {msg.sender === "user" ? "You" : msg.agent || "AI"}
              </strong>
            </div>
            <div className="message-content">
              {msg.isFormatted ? formatMessage(msg.text) : <p>{msg.text}</p>}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message ai-msg">
            <div className="message-header-info">
              <strong className="sender-name">AI</strong>
            </div>
            <div className="message-content">
              <p className="typing-indicator">Thinking...</p>
            </div>
          </div>
        )}
      </div>
      <form className="chat-form" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}

export default App;
