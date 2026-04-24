import { useState, useRef, useEffect } from 'react';

const COMMON_SYMPTOMS = [
  "I have a fever",
  "My head hurts",
  "I can't stop coughing",
  "I have a blocked nose",
  "I feel very tired",
  "My throat hurts"
];

const COMMON_DISEASES = [
  "Cold",
  "Covid",
  "Flu",
  "Allergy",
  "Asthma"
];

export default function ChatInterface({ mode, onBack }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: mode === 'knows' 
        ? "Hello! Please tell me the name of the disease you are suffering from." 
        : "Hello! Please describe your symptoms in detail using simple English so I can help diagnose you."
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleClearChat = () => {
    setMessages([
      {
        id: Date.now(),
        sender: 'bot',
        text: mode === 'knows' 
          ? "Hello! Please tell me the name of the disease you are suffering from." 
          : "Hello! Please describe your symptoms in detail using simple English so I can help diagnose you."
      }
    ]);
  };

  const handleChipClick = (text) => {
    setInput(text);
  };

  const handleSubmit = async (e) => {
    if (e && e.preventDefault) e.preventDefault();
    if (!input.trim()) return;

    const currentInput = input;
    const userMessage = { id: Date.now(), sender: 'user', text: currentInput };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: currentInput,
          knows_disease: mode === 'knows'
        })
      });

      const data = await response.json();
      
      const botMessage = {
        id: Date.now() + 1,
        sender: 'bot',
        disease: data.disease,
        text: data.treatment,
        disclaimer: data.disclaimer
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        sender: 'bot',
        text: "I'm sorry, I'm having trouble connecting to the server right now. Please try again later."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const chips = mode === 'knows' ? COMMON_DISEASES : COMMON_SYMPTOMS;

  return (
    <div className="chat-container">
      <div className="chat-header">
        <button className="back-btn" onClick={onBack} title="Go Back">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
        </button>
        <div className="header-info">
          <h2>Aura Health AI</h2>
          <p><span className="status-dot"></span> Online</p>
        </div>
        <button className="glass-button" style={{marginLeft: 'auto', padding: '8px 16px', fontSize: '0.85rem'}} onClick={handleClearChat}>
          Clear Chat
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message-wrapper ${msg.sender} animate-fade-in`}>
            <div className="message-bubble">
              {msg.disease && msg.disease !== 'Unknown' && msg.disease !== 'Error' && (
                <div className="disease-tag">
                  Diagnosis: {msg.disease}
                </div>
              )}
              <div className="treatment-text">{msg.text}</div>
              {msg.disclaimer && (
                <div className="disclaimer-text">{msg.disclaimer}</div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message-wrapper bot animate-fade-in">
            <div className="message-bubble typing-indicator">
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <div className="symptom-chips">
          {chips.map((chip, idx) => (
            <button key={idx} className="chip-btn" onClick={() => handleChipClick(chip)}>
              {chip}
            </button>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            className="glass-input"
            placeholder={mode === 'knows' ? "e.g., I have a cold..." : "e.g., I have a headache and fever..."}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
          />
          <button type="submit" className="glass-button send-btn" disabled={isLoading || !input.trim()}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
}
