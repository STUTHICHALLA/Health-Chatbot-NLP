import { useState } from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';

function App() {
  const [chatMode, setChatMode] = useState(null); // null | 'knows' | 'symptoms'

  return (
    <div className="app-container glass-container animate-fade-in">
      {!chatMode ? (
        <div className="landing-page">
          <div className="hero-icon">
            🩺
          </div>
          <h1>Aura Health AI</h1>
          <p>
            Your intelligent personal health assistant. Powered by Natural Language Processing to diagnose your symptoms and provide immediate treatment recommendations.
          </p>
          <div className="action-buttons">
            <button 
              className="glass-button btn-primary"
              onClick={() => setChatMode('knows')}
            >
              I know my disease
            </button>
            <button 
              className="glass-button btn-secondary"
              onClick={() => setChatMode('symptoms')}
            >
              I want to check my symptoms
            </button>
          </div>
        </div>
      ) : (
        <ChatInterface 
          mode={chatMode} 
          onBack={() => setChatMode(null)} 
        />
      )}
    </div>
  );
}

export default App;
