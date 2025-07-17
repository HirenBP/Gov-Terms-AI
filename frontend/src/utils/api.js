const API_BASE_URL = process.env.REACT_APP_API_BASE_URL

/**
 * Send chat message to the simplified backend
 * @param {string} message - User's message/query
 * @param {Array} chatHistory - Previous conversation (not used by new backend but kept for compatibility)
 * @returns {Promise<Object>} Response from backend
 */
export const sendChatMessage = async (message, chatHistory = []) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/query`, { // Correct endpoint for current backend
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: message,  // Backend expects 'query' field
        chat_history: chatHistory, // Include chat history if needed
        max_sources: 3   // Optional parameter for max sources
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Process sources to include all backend details
    const processedSources = data.sources.map((source) => {
      console.log('Processing source score:', source.score);
      console.log('Processing source:', source);
      return {
        score: source.score,
        text: source.text,
        entity: source.entity,
        portfolio: source.portfolio,
        url: source.url,
      };
    });

    return {
      response: data.ai_response,
      sources: processedSources, // All sources for debugging
      selectedSource: data.selected_source, // The source Gemini actually used
      query: data.query,
      timestamp: data.timestamp,
    };
  } catch (error) {
    console.error('API call failed:', error);
    throw new Error(error.message || 'Failed to send message');
  }
};

/**
 * Check if backend is available
 * @returns {Promise<boolean>} True if backend is reachable
 */

/**
 * Check backend availability and log the backend URL
 * @returns {Promise<{available: boolean, backendUrl: string}>}
 */
export const getBackendStatus = async () => {
  const backendUrl = API_BASE_URL;
  try {
    const response = await fetch(`${backendUrl}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const available = response.ok;
    if (available) {
      console.log(`Backend connected: ${backendUrl}`);
    } else {
      console.log(`Backend unavailable: ${backendUrl}`);
    }
    return { available, backendUrl };
  } catch (error) {
    console.error('Backend availability check failed:', error);
    return { available: false, backendUrl };
  }
};