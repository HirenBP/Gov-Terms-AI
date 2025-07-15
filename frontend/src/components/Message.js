import React from 'react';
import ReactMarkdown from 'react-markdown';

// Message component to handle the source format from backend
const Message = ({ message }) => {
  const isUser = message.role === 'user';
  console.log('Message sources:', message.sources);
  
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

        {message.sources && message.sources.length > 0 &&
          message.text &&
          message.text.trim() !== "I apologize, but the term you're asking about is not defined in the knowledge I currently have." && (
            <div className="message-sources">
              <div className="sources-title"><strong>Source:</strong></div>
              {(() => {
                const src = message.sources[0];
                return (
                  <div className="source-item" key={src.id || 0}>
                    <div className="source-term"><strong>{src.entity}</strong></div>
                    {src.url && (
                      <div className="source-url">
                        <a href={src.url} target="_blank" rel="noopener noreferrer">Source Link</a>
                      </div>
                    )}
                    {src.portfolio && <div className="source-portfolio">Portfolio: {src.portfolio}</div>}
                    <div className="source-score">Relevance: {(src.score * 100).toFixed(1)}%</div>
                  </div>
                );
              })()}
            </div>
        )}
      </div>
    </div>
  );
};

export default Message;
