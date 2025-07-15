import React from 'react';
import Icons from './Icons';
import './UserPreferences.css';

const UserPreferences = ({ isDarkMode, onToggleDarkMode, onIncreaseFontSize, onDecreaseFontSize }) => {
  return (
    <div className="user-preferences-menu">
      <button
        className="preferences-btn"
        onClick={onToggleDarkMode}
        aria-label="Toggle Dark Mode"
        title="Toggle Dark Mode"
      >
        {isDarkMode ? <Icons.Sun /> : <Icons.Moon />}
      </button>
      <button
        className="preferences-btn"
        onClick={onIncreaseFontSize}
        aria-label="Increase Font Size"
        title="Increase Font Size"
      >
        <Icons.Plus />
      </button>
      <button
        className="preferences-btn"
        onClick={onDecreaseFontSize}
        aria-label="Decrease Font Size"
        title="Decrease Font Size"
      >
        <Icons.Minus />
      </button>
    </div>
  );
};

export default UserPreferences;
