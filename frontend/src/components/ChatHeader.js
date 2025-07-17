import React, { useState } from 'react';
import Icons from './Icons';
import UserPreferences from './UserPreferences';
import useUserPreferences from '../hooks/useUserPreferences';

// Chat Box Header Component
const ChatHeader = ({ isConnected, onShowAbout, onShowHelp }) => {
  const [isAccessibilityMenuVisible, setAccessibilityMenuVisible] = useState(false);
  const { isDarkMode, toggleDarkMode, changeFontSize } = useUserPreferences();



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

  // Close menu when input is focused (user starts typing), but only if menu is open
  React.useEffect(() => {
    if (!isAccessibilityMenuVisible) return;
    const handler = () => setAccessibilityMenuVisible(false);
    window.addEventListener('input-focus', handler);
    return () => window.removeEventListener('input-focus', handler);
  }, [isAccessibilityMenuVisible]);

  return (
    <div className="chat-header">
      <div className="header-title">
        <img
        src="/robot.svg"
        alt="Gov Terms AI Robot"
        style={{ height: 40, marginRight: 12, verticalAlign: 'middle' }}
      />
        <h1>Gov Terms AI</h1>
      </div>
      <div className="header-actions">
        <div className="connection-status">
          <div className={`status-indicator ${isConnected ? 'connected' : ''}`}></div>
        </div>
        
        <button className="btn btn-icon" onClick={handleAbout} title="About">
          <Icons.Info />
        </button>
        
        <button className="btn btn-icon" onClick={handleHelp} title="Help">
          <Icons.Help />
        </button>

        {/* Accessibility Icon */}
        <button className="btn btn-icon" onClick={toggleAccessibilityMenu} title="Accessibility">
          <Icons.Theme />
        </button>

        {/* Floating Menu as dropdown in header */}
        {isAccessibilityMenuVisible && (
          <div className="user-preferences-menu">
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
