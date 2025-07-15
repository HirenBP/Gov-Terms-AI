import React from 'react';
import Icons from './Icons';

// Error Message Component
const ErrorMessage = ({ error, onRetry }) => (
  <div className="error-message">
    <strong>Connection Error:</strong> {error}
    <button 
      className="btn btn-secondary" 
      onClick={onRetry}
      style={{ marginLeft: '1rem' }}
    >
      <Icons.Refresh /> Retry
    </button>
  </div>
);

export default ErrorMessage;
