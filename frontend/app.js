class InGameAssistant {
    constructor() {
        this.mcpClient = new MCPClient();
        this.isMinimized = false;
        this.isListening = false;
        this.recognition = null;
        
        this.init();
    }
    
    init() {
        this.setupElements();
        this.setupEventListeners();
        this.setupSpeechRecognition();
        this.connectToMCP();
    }
    
    setupElements() {
        this.container = document.getElementById('assistant-container');
        this.window = document.querySelector('.assistant-window');
        this.chatArea = document.getElementById('chat-area');
        this.textInput = document.getElementById('text-input');
        this.sendBtn = document.getElementById('send-btn');
        this.voiceBtn = document.getElementById('voice-btn');
        this.toggleBtn = document.getElementById('toggle-btn');
        this.voiceStatus = document.getElementById('voice-status');
        this.statusIndicator = document.querySelector('.status-indicator');
        this.statusDot = document.querySelector('.status-dot');
        this.statusText = document.querySelector('.status-text');
    }
    
    setupEventListeners() {
        // Send button
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Enter key
        this.textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Voice button
        this.voiceBtn.addEventListener('click', () => this.toggleVoiceInput());
        
        // Toggle minimize
        this.toggleBtn.addEventListener('click', () => this.toggleMinimize());
        
        // Make window draggable
        this.makeDraggable();
    }
    
    setupSpeechRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
            
            this.recognition.onstart = () => {
                this.isListening = true;
                this.voiceBtn.classList.add('listening');
                this.voiceStatus.textContent = '🎤 Listening...';
            };
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.textInput.value = transcript;
                this.stopVoiceInput();
                this.sendMessage();
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.voiceStatus.textContent = `Error: ${event.error}`;
                this.stopVoiceInput();
            };
            
            this.recognition.onend = () => {
                this.stopVoiceInput();
            };
        } else {
            this.voiceBtn.style.display = 'none';
            console.warn('Speech recognition not supported');
        }
    }
    
    toggleVoiceInput() {
        if (this.isListening) {
            this.stopVoiceInput();
        } else {
            this.startVoiceInput();
        }
    }
    
    startVoiceInput() {
        if (this.recognition) {
            this.recognition.start();
        }
    }
    
    stopVoiceInput() {
        if (this.recognition) {
            this.recognition.stop();
        }
        this.isListening = false;
        this.voiceBtn.classList.remove('listening');
        this.voiceStatus.textContent = '';
    }
    
    async sendMessage() {
        const message = this.textInput.value.trim();
        if (!message) return;
        
        // Clear input
        this.textInput.value = '';
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Update status
        this.updateStatus('thinking', 'Processing...');
        
        try {
            // Send to MCP
            const response = await this.mcpClient.sendMessage(message);
            this.addMessage(response, 'assistant');
            this.updateStatus('ready', 'Ready');
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('Sorry, I encountered an error. Please try again.', 'error');
            this.updateStatus('error', 'Error');
            setTimeout(() => this.updateStatus('ready', 'Ready'), 2000);
        }
    }
    
    addMessage(text, type) {
        // Remove welcome message if present
        const welcomeMsg = this.chatArea.querySelector('.welcome-message');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = text;
        this.chatArea.appendChild(messageDiv);
        
        // Scroll to bottom
        this.chatArea.scrollTop = this.chatArea.scrollHeight;
    }
    
    toggleMinimize() {
        this.isMinimized = !this.isMinimized;
        this.window.classList.toggle('minimized', this.isMinimized);
        this.toggleBtn.textContent = this.isMinimized ? '+' : '−';
    }
    
    makeDraggable() {
        const header = document.querySelector('.assistant-header');
        let isDragging = false;
        let currentX;
        let currentY;
        let initialX;
        let initialY;
        
        header.addEventListener('mousedown', (e) => {
            if (e.target === this.toggleBtn) return;
            
            isDragging = true;
            initialX = e.clientX - this.container.offsetLeft;
            initialY = e.clientY - this.container.offsetTop;
        });
        
        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            
            e.preventDefault();
            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;
            
            this.container.style.left = currentX + 'px';
            this.container.style.right = 'auto';
            this.container.style.bottom = 'auto';
            this.container.style.top = currentY + 'px';
        });
        
        document.addEventListener('mouseup', () => {
            isDragging = false;
        });
    }
    
    connectToMCP() {
        this.updateStatus('connecting', 'Connecting...');
        this.mcpClient.connect()
            .then(() => {
                this.updateStatus('ready', 'Ready');
            })
            .catch((error) => {
                console.error('Failed to connect to MCP:', error);
                this.updateStatus('error', 'Connection Error');
            });
    }
    
    updateStatus(state, text) {
        this.statusDot.className = `status-dot ${state}`;
        this.statusText.textContent = text;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.assistant = new InGameAssistant();
});

