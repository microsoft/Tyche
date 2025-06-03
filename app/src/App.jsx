import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMessage = { user: "user", message: input };
    setMessages([...messages, { sender: "user", text: input }]);
    setInput("");
    setLoading(true);
    try {
      const res = await axios.post("/api/chat", userMessage);
      // Expecting res.data to be an array of { agent, answer }
      if (Array.isArray(res.data)) {
        setMessages((msgs) => [
          ...msgs,
          ...res.data.map((item) => ({
            sender: item.agent || "ai",
            text: item.answer
          }))
        ]);
      } else {
        setMessages((msgs) => [
          ...msgs,
          { sender: "ai", text: res.data.answer || "No answer returned." }
        ]);
      }
    } catch (err) {
      setMessages((msgs) => [
        ...msgs,
        { sender: "ai", text: "Error: Could not get answer." }
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
          <div key={idx} className={msg.sender === "user" ? "user-msg" : "ai-msg"}>
            <b>{msg.sender === "user" ? "You" : "AI"}:</b> {msg.text}
          </div>
        ))}
        {loading && <div className="ai-msg">AI is typing...</div>}
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
