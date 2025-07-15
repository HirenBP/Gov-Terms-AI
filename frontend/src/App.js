import React, { useEffect, useState, useRef, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import { getBackendStatus, sendChatMessage } from './utils/api';
import useUserPreferences from './hooks/useUserPreferences';
import './App.css';
import {
  ChatHeader,
  ChatFooter,
  ActionButtons,
  Message,
  TypingIndicator,
  Panel,
  Modal,
  AboutPanel,
  HelpPanel,
  ErrorMessage,
  WelcomeMessage,
  UserPreferences
} from './components';



// Main App Component
const App = () => {
  // User Preferences Hook
  const { isDarkMode, fontSize, toggleDarkMode, changeFontSize } = useUserPreferences();
  
  // State
  const [chatHistory, setChatHistory] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);
  const [aboutPanelOpen, setAboutPanelOpen] = useState(false);
  const [helpPanelOpen, setHelpPanelOpen] = useState(false);
  const [summaryModalOpen, setSummaryModalOpen] = useState(false);
  const [summary, setSummary] = useState('');
  const [isGeneratingSummary, setIsGeneratingSummary] = useState(false);
  const [settingsPanelOpen, setSettingsPanelOpen] = useState(false);
  
  // Refs
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const floatingMenuRef = useRef(null);
  const headerRef = useRef(null);
  
  useEffect(() => {
    const checkConnection = async () => {
      try {
        const { available } = await getBackendStatus();
        setIsConnected(available);
        setError(null);
      } catch (error) {
        setIsConnected(false);
        setError('Unable to connect to backend service');
      }
    };
    checkConnection();
  }, []);

  // Close floating menu when clicking outside of it and outside the header
  const handleDocumentClick = useCallback((event) => {
    if (
      settingsPanelOpen &&
      floatingMenuRef.current &&
      !floatingMenuRef.current.contains(event.target) &&
      headerRef.current &&
      !headerRef.current.contains(event.target)
    ) {
      setSettingsPanelOpen(false);
    }
  }, [settingsPanelOpen]);

  useEffect(() => {
    if (settingsPanelOpen) {
      document.addEventListener('mousedown', handleDocumentClick);
    } else {
      document.removeEventListener('mousedown', handleDocumentClick);
    }
    return () => {
      document.removeEventListener('mousedown', handleDocumentClick);
    };
  }, [settingsPanelOpen, handleDocumentClick]);

  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();//Scroll to bottom whenever chatiHisotry is updated
  }, [chatHistory]);
  
  const handleRetry = async () => {
    try {
      const { available } = await getBackendStatus();
      setIsConnected(available);
      setError(null);
    } catch (error) {
      setIsConnected(false);
      setError('Unable to connect to backend service');
    }
  };
  
const handleSendMessage = async (e) => {
  e.preventDefault();
  if (!userInput.trim() || isLoading) return;

  const messageText = userInput.trim();
  setUserInput('');

  // Add user message
  const userMessage = { 
    role: 'user', 
    text: messageText,
    timestamp: new Date().toISOString()
  };
  setChatHistory(prev => [...prev, userMessage]);

  setIsLoading(true);
  setError(null);

  try {
    // Convert chat history to backend format (content instead of text)
    const backendChatHistory = chatHistory.map(msg => ({
      role: msg.role,
      content: msg.text
    }));

    const response = await sendChatMessage(messageText, backendChatHistory);

    // Ensure response.response is a string
    let responseText = response.response;
    if (typeof responseText !== 'string') {
      if (responseText && typeof responseText === 'object') {
        responseText = responseText.msg || responseText.message || JSON.stringify(responseText);
      } else {
        responseText = 'Sorry, I received an unexpected response format. Please try again.';
      }
    }

    // Ensure sources are properly mapped
    const assistantMessage = {
      role: 'assistant',
      text: responseText,
      sources: response.sources || [], // Default to an empty array if sources are undefined
      timestamp: new Date().toISOString()
    };

    setChatHistory(prev => [...prev, assistantMessage]);

  } catch (error) {
    console.error('Chat error:', error);
    setError(error.message || 'An error occurred');

    const errorMessage = {
      role: 'assistant',
      text: 'Sorry, I encountered an error processing your request. Please try again.',
      timestamp: new Date().toISOString(),
      isError: true
    };
    setChatHistory(prev => [...prev, errorMessage]);

  } finally {
    setIsLoading(false);
  }
};
  
  const handleSummarize = async () => {
    if (chatHistory.length === 0) {
      setSummary('No conversation to summarize yet. Start chatting to generate a summary!');
      setSummaryModalOpen(true);
      return;
    }
    
    setIsGeneratingSummary(true);
    setSummaryModalOpen(true);
    
    try {
      // Generate summary locally from displayed chat history
      const messageCount = chatHistory.length;
      const userQuestions = chatHistory.filter(msg => msg.role === 'user').length;
      const lastUserMessage = chatHistory.filter(msg => msg.role === 'user').pop()?.text || '';
      
      const localSummary = `**Conversation Summary**

**Messages:** ${messageCount} total (${userQuestions} questions asked)

**Latest Topic:** ${lastUserMessage.length > 100 ? lastUserMessage.substring(0, 100) + '...' : lastUserMessage}

**Key Points Discussed:**
${chatHistory
  .filter(msg => msg.role === 'assistant' && msg.text.length > 50)
  .slice(-3)
  .map((msg, index) => `${index + 1}. ${msg.text.substring(0, 150)}...`)
  .join('\n')}

This conversation focused on Australian government terminology and definitions.`;
      
      setSummary(localSummary);
    } catch (error) {
      setSummary('Failed to generate summary. Please try again.');
    } finally {
      setIsGeneratingSummary(false);
    }
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };
  
  return (
    <div className="app">
        {/* Background */}
        <div className="app-background"></div>
        
        {/* Main Chat Widget */}
        <div className="chat-widget">
          <div ref={headerRef}>
            <ChatHeader 
              isConnected={isConnected}
              onShowAbout={() => setAboutPanelOpen(true)}
              onShowHelp={() => setHelpPanelOpen(true)}
              onToggleAccessibility={() => setSettingsPanelOpen(!settingsPanelOpen)}
            />
          </div>
          
          <div className="chat-body">
            <div className="chat-messages">
              {error && (
                <ErrorMessage error={error} onRetry={handleRetry} />
              )}
              
              {chatHistory.length === 0 && !isLoading && (
                <WelcomeMessage />
              )}
              
              {chatHistory.map((message, index) => (
                <Message key={index} message={message} />
              ))}
              
              {isLoading && <TypingIndicator />}
              
              <div ref={messagesEndRef} />
            </div>
            
            {/* Action Buttons */}
            <ActionButtons 
              onSummarize={handleSummarize}
            />
            
            {/* Input Area */}
            <div className="input-area">
              <form onSubmit={handleSendMessage} className="input-container">
                <div className="input-wrapper">
                  <textarea
                    ref={inputRef}
                    className="chat-input"
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your message..."
                    disabled={isLoading || !isConnected}
                    rows="1"
                  />
                </div>
                <button 
                  type="submit" 
                  className="btn btn-primary btn-send"
                  disabled={isLoading || !userInput.trim() || !isConnected}
                >
                  Send
                </button>
              </form>
            </div>
          </div>
          
          <ChatFooter />
        </div>
        
        {/* About Panel */}
        <Panel 
          isOpen={aboutPanelOpen}
          title="About Gov Terms AI"
          onClose={() => setAboutPanelOpen(false)}
        >
          <AboutPanel />
        </Panel>
        
        {/* Help Panel */}
        <Panel 
          isOpen={helpPanelOpen}
          title="Help & Tips"
          onClose={() => setHelpPanelOpen(false)}
        >
          <HelpPanel />
        </Panel>
        
        {/* Summary Modal */}
        <Modal 
          isOpen={summaryModalOpen}
          title="Conversation Summary"
          onClose={() => setSummaryModalOpen(false)}
        >
          {isGeneratingSummary ? (
            <div className="loading">
              <div className="spinner"></div>
              <span>Generating summary...</span>
            </div>
          ) : (
            <div className="summary-markdown">
              <ReactMarkdown>{summary}</ReactMarkdown>
            </div>
          )}
        </Modal>
        
        {/* Floating Accessibility Menu with outside click handler */}
        {settingsPanelOpen && (
          <div
            ref={floatingMenuRef}
            style={{ position: 'fixed', top: 20, right: 20, zIndex: 1000 }}
            tabIndex={-1}
          >
            <UserPreferences 
              isDarkMode={isDarkMode}
              onToggleDarkMode={toggleDarkMode}
              onIncreaseFontSize={() => changeFontSize('increase')}
              onDecreaseFontSize={() => changeFontSize('decrease')}
            />
          </div>
        )}
      </div>
    );
  }

export default App;
