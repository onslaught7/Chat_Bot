import React, { useState } from "react";
import "./index.css";

function App() {
  const [messages, setMessages] = useState([]); // Stores chat history
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!question.trim()) return;

    const userMessage = { sender: "user", text: question };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch(`http://127.0.0.1:8000/query?question=${encodeURIComponent(question)}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      const data = await response.json();
      const botMessage = {
        sender: "bot",
        text: data.results ? data.results.join("\n") : "I couldn't find an answer.",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [...prev, { sender: "bot", text: "Error reaching the server." }]);
    }

    setLoading(false);
    setQuestion(""); // Clear input box after sending
  };

  return (
    <div className="chat-container">
      <h2>CDP Support Chatbot</h2>
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={msg.sender === "user" ? "user-msg" : "bot-msg"}>
            {msg.text.split("\n").map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>
        ))}
        {loading && <div className="bot-msg">Thinking...</div>}
      </div>
      <div className="input-box">
        <input
          type="text"
          placeholder="Ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()} // Send on Enter key press
        />
        <button onClick={handleSend} disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;
