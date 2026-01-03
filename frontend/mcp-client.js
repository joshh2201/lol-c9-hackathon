class MCPClient {
  constructor() {
    this.ws = null;
    this.serverUrl = 'http://localhost:3001';
    this.isConnected = false;
    this.messageQueue = [];
  }

  async connect() {
    return new Promise((resolve, reject) => {
      // For now, we'll use HTTP fetch to the server
      // The server will handle MCP protocol communication
      this.isConnected = true;
      resolve();
    });
  }

  async sendMessage(message) {
    if (!this.isConnected) {
      throw new Error('Not connected to MCP server');
    }

    try {
      const response = await fetch(`${this.serverUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          timestamp: Date.now(),
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.response || data.message || 'No response received';
    } catch (error) {
      console.error('Error sending message to MCP:', error);
      throw error;
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.isConnected = false;
  }
}
