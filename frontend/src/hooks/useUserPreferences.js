import { useState, useEffect } from 'react';

const useUserPreferences = () => {
  // Initialize state from localStorage or defaults
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const saved = localStorage.getItem('govterms-theme');
    return saved ? JSON.parse(saved) : false;
  });

  const [fontSize, setFontSize] = useState(() => {
    const saved = localStorage.getItem('govterms-font-size');
    return saved || 'medium';
  });

  // Apply theme and font size to document
  useEffect(() => {
    const root = document.documentElement;
    
    // Apply theme
    if (isDarkMode) {
      root.classList.add('dark-theme');
    } else {
      root.classList.remove('dark-theme');
    }

    // Apply font size
    root.setAttribute('data-font-size', fontSize);
    
    // Save to localStorage
    localStorage.setItem('govterms-theme', JSON.stringify(isDarkMode));
    localStorage.setItem('govterms-font-size', fontSize);
  }, [isDarkMode, fontSize]);

  const toggleDarkMode = (darkMode) => {
    if (typeof darkMode === 'boolean') {
      setIsDarkMode(darkMode);
    } else {
      setIsDarkMode(prev => !prev);
    }
  };

  const changeFontSize = (action) => {
    setFontSize((prev) => {
      const sizes = ['small', 'medium', 'large'];
      const currentIndex = sizes.indexOf(prev);

      if (action === 'increase' && currentIndex < sizes.length - 1) {
        return sizes[currentIndex + 1];
      } else if (action === 'decrease' && currentIndex > 0) {
        return sizes[currentIndex - 1];
      }

      return prev; // No change if action is invalid or at boundary
    });
  };

  return {
    isDarkMode,
    fontSize,
    toggleDarkMode,
    changeFontSize
  };
};

export default useUserPreferences;
