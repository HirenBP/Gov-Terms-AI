import React, { useEffect, useId, useRef } from 'react';
import Icons from './Icons';

// Panel Component
const Panel = ({ isOpen, title, children, onClose }) => {
  const titleId = useId();
  const closeButtonRef = useRef(null);

  useEffect(() => {
    if (!isOpen) return undefined;

    closeButtonRef.current?.focus();
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;
  
  return (
    <>
      <div className="panel-overlay" onClick={onClose}></div>
      <div
        className={`panel ${isOpen ? 'open' : ''}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
      >
        <div className="panel-header">
          <h2 id={titleId} className="panel-title">{title}</h2>
          <button
            ref={closeButtonRef}
            className="btn btn-icon"
            onClick={onClose}
            aria-label={`Close ${title}`}
          >
            <Icons.Close aria-hidden="true" />
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
