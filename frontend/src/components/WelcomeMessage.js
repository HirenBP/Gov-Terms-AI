import React from 'react';

const starterPrompts = [
  'What does BPOR mean?',
  'What is ACMA?',
  'What does APS mean?',
  'What is AUSTRAC?',
  'What does FOI mean?'
];

// Welcome Message Component
const WelcomeMessage = ({ onPromptSelect, disabled = false }) => (
  <div className="welcome-message">
    <p>Let’s translate government jargon.</p>
    <p>Ask me about any Australian Government term, acronym or abbreviation.</p>
    <div className="starter-prompts" aria-label="Starter prompts">
      {starterPrompts.map((prompt) => (
        <button
          key={prompt}
          type="button"
          className="starter-prompt"
          onClick={() => onPromptSelect(prompt)}
          disabled={disabled}
        >
          {prompt}
        </button>
      ))}
    </div>
  </div>
);

export default WelcomeMessage;
