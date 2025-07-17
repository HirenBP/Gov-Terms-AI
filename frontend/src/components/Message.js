import React from 'react';
import ReactMarkdown from 'react-markdown';

// Message component to handle the source format from backend
const Message = ({ message }) => {
  const isUser = message.role === 'user';
  console.log('Message sources:', message.sources);
  console.log('Selected source:', message.selectedSource);
  console.log('Parsed response:', message.parsedResponse);
  
  // Find the source that matches the source_entity from Gemini's response
  let displaySource = null;
  
  // First try to match by source_entity if available
  if (message.parsedResponse && message.parsedResponse.source_entity && message.sources) {
    displaySource = message.sources.find(source => 
      source.entity === message.parsedResponse.source_entity
    );
  }
  
  // Fallback to selectedSource if entity matching fails or no source_entity
  if (!displaySource && message.selectedSource) {
    displaySource = message.selectedSource;
  }
  
  console.log('Display source:', displaySource);
  
  return (
    <div className={`message ${isUser ? 'user' : 'assistant'}`}>
      <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
        <div className="message-content">
          {isUser ? (
            message.text
          ) : (
            <ReactMarkdown>{message.text}</ReactMarkdown>
          )}
        </div>

        {message.timestamp && !isUser && (
          <div className="message-time">
            {new Date(message.timestamp).toLocaleTimeString()}
          </div>
        )}

        {displaySource && !message.isError && !isUser && (
            <div className="message-sources">
              <div className="sources-title"><strong>Source:</strong></div>
              <div className="source-item" key={displaySource.id || 0}>
                <div className="source-term"><strong>{displaySource.entity}</strong></div>
                {displaySource.url && (
                  <div className="source-url">
                    <a href={displaySource.url} target="_blank" rel="noopener noreferrer">Source Link</a>
                  </div>
                )}
                {displaySource.portfolio && <div className="source-portfolio">Portfolio: {displaySource.portfolio}</div>}
                <div className="source-score">Relevance: {(displaySource.score * 100).toFixed(1)}%</div>
              </div>
            </div>
        )}
      </div>
    </div>
  );
};

export default Message;
