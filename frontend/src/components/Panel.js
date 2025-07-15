import React from 'react';
import Icons from './Icons';

// Panel Component
const Panel = ({ isOpen, title, children, onClose }) => {
  if (!isOpen) return null;
  
  return (
    <>
      <div className="panel-overlay" onClick={onClose}></div>
      <div className={`panel ${isOpen ? 'open' : ''}`}>
        <div className="panel-header">
          <h2 className="panel-title">{title}</h2>
          <button className="btn btn-icon" onClick={onClose}>
            <Icons.Close />
          </button>
        </div>
        <div className="panel-content">
          {children}
        </div>
      </div>
    </>
  );
};

export default Panel;
