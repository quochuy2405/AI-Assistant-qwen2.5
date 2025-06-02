// Chat Application JavaScript
class ChatApp {
    constructor() {
        this.apiBase = 'http://localhost:8000';
        this.isStreaming = true;
        this.isLoading = false;
        
        this.initializeElements();
        this.bindEvents();
        this.loadStats();
        
        console.log('🚀 AI KOC Support Chat initialized');
    }
    
    initializeElements() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.streamingToggle = document.getElementById('streamingToggle');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        
        // Stats elements
        this.totalDocs = document.getElementById('totalDocs');
        this.totalTopics = document.getElementById('totalTopics');
        this.responseTime = document.getElementById('responseTime');
        this.accuracy = document.getElementById('accuracy');
    }
    
    bindEvents() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter key to send message
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.autoResizeTextarea();
        });
        
        // Streaming toggle
        this.streamingToggle.addEventListener('change', (e) => {
            this.isStreaming = e.target.checked;
            console.log('Streaming mode:', this.isStreaming ? 'ON' : 'OFF');
        });
        
        // Quick question buttons
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const question = e.target.getAttribute('data-question');
                this.messageInput.value = question;
                this.sendMessage();
            });
        });
    }
    
    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isLoading) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.autoResizeTextarea();
        
        // Disable input while processing
        this.setLoading(true);
        
        try {
            if (this.isStreaming) {
                await this.sendStreamingMessage(message);
            } else {
                await this.sendNonStreamingMessage(message);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('❌ Lỗi kết nối. Vui lòng thử lại!', 'bot');
        } finally {
            this.setLoading(false);
        }
    }
    
    async sendStreamingMessage(message) {
        const startTime = Date.now();
        
        // Add typing indicator
        const typingElement = this.addTypingIndicator();
        
        try {
            const response = await fetch(`${this.apiBase}/chat/completions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'koc-assistant',
                    messages: [{ role: 'user', content: message }],
                    stream: true
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            // Remove typing indicator
            typingElement.remove();
            
            // Create bot message element for streaming
            const messageElement = this.addMessage('', 'bot');
            const textElement = messageElement.querySelector('.message-text');
            
            // Process SSE stream
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            let fullResponse = '';
            
            while (true) {
                const { value, done } = await reader.read();
                if (done) break;
                
                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop(); // Keep incomplete line in buffer
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        
                        if (data === '[DONE]') {
                            break;
                        }
                        
                        try {
                            const parsed = JSON.parse(data);
                            if (parsed.choices?.[0]?.delta?.content) {
                                const content = parsed.choices[0].delta.content;
                                fullResponse += content;
                                
                                // Update message with formatted markdown-like content
                                textElement.innerHTML = this.formatMessage(fullResponse);
                                this.scrollToBottom();
                            }
                        } catch (e) {
                            // Skip invalid JSON
                        }
                    }
                }
            }
            
            // Update timing
            const duration = Date.now() - startTime;
            this.updateMessageTime(messageElement, `${(duration / 1000).toFixed(1)}s`);
            
        } catch (error) {
            typingElement?.remove();
            throw error;
        }
    }
    
    async sendNonStreamingMessage(message) {
        const startTime = Date.now();
        
        // Add typing indicator
        const typingElement = this.addTypingIndicator();
        
        try {
            const response = await fetch(`${this.apiBase}/chat/completions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'koc-assistant',
                    messages: [{ role: 'user', content: message }],
                    stream: false
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            const botMessage = data.choices[0].message.content;
            
            // Remove typing indicator
            typingElement.remove();
            
            // Add bot response
            const messageElement = this.addMessage(botMessage, 'bot');
            
            // Update timing
            const duration = Date.now() - startTime;
            this.updateMessageTime(messageElement, `${(duration / 1000).toFixed(1)}s`);
            
        } catch (error) {
            typingElement?.remove();
            throw error;
        }
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const now = new Date();
        const timeStr = now.toLocaleTimeString('vi-VN', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas ${sender === 'bot' ? 'fa-robot' : 'fa-user'}"></i>
            </div>
            <div class="message-content">
                <div class="message-text">${this.formatMessage(content)}</div>
                <div class="message-time">${timeStr}</div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        return messageDiv;
    }
    
    addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message';
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="typing-indicator">
                    AI đang trả lời
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
        
        return typingDiv;
    }
    
    formatMessage(content) {
        if (!content) return '';
        
        // Convert markdown-like formatting to HTML
        let formatted = content
            // Bold text **text**
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            // Headers
            .replace(/^### (.*?)$/gm, '<h4>$1</h4>')
            .replace(/^## (.*?)$/gm, '<h3>$1</h3>')
            // Line breaks
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n/g, '<br>')
            // Bullet points
            .replace(/• (.*?)(?=<br>|$)/g, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/g, '<ul>$1</ul>')
            // Fix nested lists
            .replace(/<\/ul><ul>/g, '');
        
        return formatted;
    }
    
    updateMessageTime(messageElement, timeStr) {
        const timeElement = messageElement.querySelector('.message-time');
        if (timeElement) {
            timeElement.textContent = timeStr;
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        this.sendButton.disabled = loading;
        this.messageInput.disabled = loading;
        
        if (loading) {
            this.sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        } else {
            this.sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        }
    }
    
    async loadStats() {
        try {
            const response = await fetch(`${this.apiBase}/stats`);
            if (response.ok) {
                const stats = await response.json();
                
                this.totalDocs.textContent = stats.total_documents || 0;
                this.totalTopics.textContent = stats.supported_topics || 0;
                this.responseTime.textContent = stats.response_time || '< 1s';
                this.accuracy.textContent = stats.accuracy || '95%';
            }
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }
}

// Test API Functions
async function testHealth() {
    try {
        const response = await fetch('http://localhost:8000/health');
        const data = await response.json();
        
        showNotification('✅ Health Check OK', 'success');
        console.log('Health:', data);
    } catch (error) {
        showNotification('❌ Health Check Failed', 'error');
        console.error('Health error:', error);
    }
}

async function testModels() {
    try {
        const response = await fetch('http://localhost:8000/models');
        const data = await response.json();
        
        showNotification(`✅ Found ${data.data.length} model(s)`, 'success');
        console.log('Models:', data);
    } catch (error) {
        showNotification('❌ Models Test Failed', 'error');
        console.error('Models error:', error);
    }
}

async function testStats() {
    try {
        const response = await fetch('http://localhost:8000/stats');
        const data = await response.json();
        
        showNotification('✅ Stats Loaded', 'success');
        console.log('Stats:', data);
        
        // Update stats in sidebar
        document.getElementById('totalDocs').textContent = data.total_documents;
        document.getElementById('totalTopics').textContent = data.supported_topics;
        document.getElementById('responseTime').textContent = data.response_time;
        document.getElementById('accuracy').textContent = data.accuracy;
    } catch (error) {
        showNotification('❌ Stats Test Failed', 'error');
        console.error('Stats error:', error);
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        z-index: 10000;
        font-size: 14px;
        animation: slideInRight 0.3s ease-out;
    `;
    notification.textContent = message;
    
    // Add animation CSS if not exists
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideInRight 0.3s ease-out reverse';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Initialize chat app when DOM loads
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});

// Handle connection status
window.addEventListener('online', () => {
    const statusIndicator = document.querySelector('.status-indicator');
    const statusText = document.querySelector('.status span');
    
    statusIndicator.className = 'status-indicator online';
    statusText.textContent = 'Online';
    
    showNotification('🌐 Đã kết nối', 'success');
});

window.addEventListener('offline', () => {
    const statusIndicator = document.querySelector('.status-indicator');
    const statusText = document.querySelector('.status span');
    
    statusIndicator.className = 'status-indicator offline';
    statusIndicator.style.background = '#f44336';
    statusText.textContent = 'Offline';
    
    showNotification('📶 Mất kết nối', 'error');
}); 