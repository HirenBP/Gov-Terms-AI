import React, { useEffect, useRef, useState } from 'react';
import Icons from './Icons';
import UserPreferences from './UserPreferences';
import useUserPreferences from '../hooks/useUserPreferences';

// Chat Box Header Component
const ChatHeader = ({ connectionStatus, onShowAbout, onShowHelp }) => {
  const [isAccessibilityMenuVisible, setAccessibilityMenuVisible] = useState(false);
  const accessibilityButtonRef = useRef(null);
  const accessibilityMenuRef = useRef(null);
  const { isDarkMode, toggleDarkMode, changeFontSize } = useUserPreferences();
  const connectionLabels = {
    connecting: 'Connecting to backend…',
    connected: 'Connected to backend',
    disconnected: 'Backend unavailable'
  };
  const connectionLabel = connectionLabels[connectionStatus] || connectionLabels.disconnected;

  const handleAbout = () => {
    setAccessibilityMenuVisible(false);
    if (onShowAbout) onShowAbout();
  };
  const handleHelp = () => {
    setAccessibilityMenuVisible(false);
    if (onShowHelp) onShowHelp();
  };

  // Close menu when About or Help is clicked
  const toggleAccessibilityMenu = () => {
    setAccessibilityMenuVisible((prev) => !prev);
  };

  // Close the menu when the user interacts anywhere outside the button or menu.
  useEffect(() => {
    if (!isAccessibilityMenuVisible) return undefined;

    const handleOutsideInteraction = (event) => {
      const clickedButton = accessibilityButtonRef.current?.contains(event.target);
      const clickedMenu = accessibilityMenuRef.current?.contains(event.target);

      if (!clickedButton && !clickedMenu) {
        setAccessibilityMenuVisible(false);
      }
    };

    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        setAccessibilityMenuVisible(false);
        accessibilityButtonRef.current?.focus();
      }
    };
    const handleInputFocus = () => setAccessibilityMenuVisible(false);

    document.addEventListener('pointerdown', handleOutsideInteraction);
    document.addEventListener('keydown', handleKeyDown);
    window.addEventListener('input-focus', handleInputFocus);

    return () => {
      document.removeEventListener('pointerdown', handleOutsideInteraction);
      document.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('input-focus', handleInputFocus);
    };
  }, [isAccessibilityMenuVisible]);

  return (
    <div className="chat-header">
      <div className="header-title">
        {/* Use the SVG robot icon so it inherits color/size and matches .bot-icon CSS */}
        <Icons.Bot className="bot-icon" size={40} style={{ marginRight: 12, verticalAlign: 'middle' }} aria-hidden="true" />
        <h1>IM2026 Gov Terms AI 2.0</h1>
      </div>
      <div className="header-actions">
        <div
          className="connection-status"
          role="status"
          aria-live="polite"
          title={connectionLabel}
        >
          <span
            className={`status-indicator ${connectionStatus}`}
            aria-hidden="true"
          />
          <span className="connection-status-text">{connectionLabel}</span>
        </div>
        
        <button className="btn btn-icon header-action-button" onClick={handleAbout} title="About">
          <Icons.Info aria-hidden="true" />
          <span>About</span>
        </button>
        
        <button className="btn btn-icon header-action-button" onClick={handleHelp} title="Help">
          <Icons.Help aria-hidden="true" />
          <span>Help</span>
        </button>

        {/* Accessibility Icon */}
        <button
          ref={accessibilityButtonRef}
          className="btn btn-icon header-action-button"
          onClick={toggleAccessibilityMenu}
          title="Accessibility"
          aria-expanded={isAccessibilityMenuVisible}
        >
          <Icons.Theme aria-hidden="true" />
          <span>Accessibility</span>
        </button>

        {/* Floating Menu as dropdown in header */}
        {isAccessibilityMenuVisible && (
          <div ref={accessibilityMenuRef} className="user-preferences-menu">
            <UserPreferences 
              isDarkMode={isDarkMode}
              onToggleDarkMode={toggleDarkMode}
              onIncreaseFontSize={() => changeFontSize('increase')}
              onDecreaseFontSize={() => changeFontSize('decrease')}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatHeader;
