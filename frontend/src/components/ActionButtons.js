import React from 'react';
import Icons from './Icons';

// Action Buttons Component
const ActionButtons = ({ onSummarize }) => (
  <div className="action-buttons">
    <button className="btn btn-action" onClick={onSummarize}>
      <Icons.Summary /> Summary
    </button>
  </div>
);

export default ActionButtons;
