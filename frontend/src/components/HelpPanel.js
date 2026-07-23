import React from 'react';

// Help Panel Content Component
const HelpPanel = () => (
  <div>
    <h3>How to Use</h3>
    <ul>
      <li>Enter a government term, acronym or abbreviation in the message box.</li>
      <li>Add context, such as an agency or policy area, if the term could have several meanings.</li>
      <li>Ask a follow-up question if you want a simpler explanation or more detail.</li>
    </ul>
    
    <h3>Example Questions</h3>
    <ul>
      <li>“What does BPOR mean?”</li>
      <li>“What is ACMA?”</li>
      <li>“Explain AUSTRAC in plain language.”</li>
    </ul>
    
    <h3>Features</h3>
    <ul>
      <li><strong>Sources:</strong> Review the documents referenced in an answer.</li>
      <li><strong>Summary:</strong> Create a short summary of your current conversation.</li>
      <li><strong>Accessibility:</strong> Change the theme or text size from the header.</li>
    </ul>

    <h3>If Something Goes Wrong</h3>
    <p>If the backend is unavailable, use the retry option and wait for the header status to show “Connected to backend” before sending a message.</p>
  </div>
);

export default HelpPanel;
