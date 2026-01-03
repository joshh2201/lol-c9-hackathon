# LoL In-Game Assistant Frontend

Lightweight Clueless-style frontend for in-game assistant with MCP integration.

## Features

- 🎤 **Voice Input (TTS)** - Speech-to-text using Web Speech API
- ⌨️ **Text Input** - Type questions directly
- 🎨 **Minimal Overlay Design** - Non-intrusive in-game UI
- 🔌 **MCP Integration** - Ready for Model Context Protocol
- 📱 **Draggable Window** - Move anywhere on screen
- 🔄 **Minimize/Maximize** - Collapse when not needed

## Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the server:**
   ```bash
   npm start
   ```

3. **Open in browser:**
   - Navigate to `http://localhost:3001`
   - Or use as overlay in game capture software

## MCP Integration

The server (`server.js`) has a placeholder for MCP integration. Replace the `handleMCPRequest` function with your actual MCP client code:

```javascript
async function handleMCPRequest(message) {
    const mcpClient = require('./your-mcp-client');
    return await mcpClient.send({
        method: 'tools/call',
        params: {
            name: 'game_assistant',
            arguments: { query: message }
        }
    });
}
```

## Usage

- **Type a question** in the input field and press Enter or click Send
- **Click the microphone** button to use voice input
- **Drag the window** by clicking and dragging the header
- **Minimize** by clicking the `−` button in the header

## Browser Compatibility

- Chrome/Edge: Full support (including voice)
- Firefox: Full support (voice may vary)
- Safari: Limited voice support

## Customization

Edit `styles.css` to customize colors, size, and positioning.

