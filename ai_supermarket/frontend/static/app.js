// JavaScript for WatsonX Orchestrate Agent UI

const API_BASE = window.location.origin;
let config = {
    api_url: '',
    api_key: '',
    agent_id: 'supermarket_inventory_manager_agent'
};

// DOM Elements
const configBtn = document.getElementById('configBtn');
const configModal = document.getElementById('configModal');
const closeConfig = document.getElementById('closeConfig');
const saveConfig = document.getElementById('saveConfig');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const messages = document.getElementById('messages');
const clearChat = document.getElementById('clearChat');
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');
const actionButtons = document.querySelectorAll('.action-btn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadConfig();
    setupEventListeners();
    checkHealth();
});

// Event Listeners
function setupEventListeners() {
    configBtn.addEventListener('click', () => openConfigModal());
    closeConfig.addEventListener('click', () => closeConfigModal());
    saveConfig.addEventListener('click', () => saveConfiguration());
    sendBtn.addEventListener('click', () => sendMessage());
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    clearChat.addEventListener('click', () => clearChatMessages());
    
    actionButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.action;
            executeQuickAction(action);
        });
    });
    
    // Close modal on outside click
    configModal.addEventListener('click', (e) => {
        if (e.target === configModal) {
            closeConfigModal();
        }
    });
}

// Configuration Modal
function openConfigModal() {
    document.getElementById('apiUrl').value = config.api_url || '';
    document.getElementById('apiKey').value = config.api_key || '';
    document.getElementById('agentId').value = config.agent_id || '';
    configModal.classList.add('show');
}

function closeConfigModal() {
    configModal.classList.remove('show');
    const statusDiv = document.getElementById('configStatus');
    statusDiv.classList.remove('show');
}

async function saveConfiguration() {
    const apiUrl = document.getElementById('apiUrl').value.trim();
    const apiKey = document.getElementById('apiKey').value.trim();
    const agentId = document.getElementById('agentId').value.trim();
    
    const statusDiv = document.getElementById('configStatus');
    
    if (!apiUrl || !apiKey || !agentId) {
        showConfigStatus('warning', 'Please fill in all fields');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/config`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                api_url: apiUrl,
                api_key: apiKey,
                agent_id: agentId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            config = { api_url: apiUrl, api_key: apiKey, agent_id: agentId };
            localStorage.setItem('agentConfig', JSON.stringify(config));
            showConfigStatus('success', 'Configuration saved successfully!');
            updateStatus('Ready', 'success');
            setTimeout(() => {
                closeConfigModal();
            }, 1500);
        } else {
            showConfigStatus('error', data.error || 'Failed to save configuration');
        }
    } catch (error) {
        showConfigStatus('error', `Error: ${error.message}`);
    }
}

function showConfigStatus(type, message) {
    const statusDiv = document.getElementById('configStatus');
    statusDiv.className = `config-status ${type} show`;
    statusDiv.textContent = message;
}

// Load Configuration
async function loadConfig() {
    const saved = localStorage.getItem('agentConfig');
    if (saved) {
        config = JSON.parse(saved);
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/config`);
        const data = await response.json();
        if (data.api_url) {
            config.api_url = data.api_url;
        }
        if (data.agent_id) {
            config.agent_id = data.agent_id;
        }
    } catch (error) {
        console.error('Failed to load config from server:', error);
    }
    
    if (config.api_url && config.api_key) {
        updateStatus('Ready', 'success');
    } else {
        updateStatus('Configuration needed', 'warning');
    }
}

// Health Check
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/api/health`);
        const data = await response.json();
        if (data.status === 'healthy') {
            updateStatus('Connected', 'success');
        }
    } catch (error) {
        updateStatus('Connection error', 'error');
    }
}

// Status Update
function updateStatus(text, type = 'success') {
    statusText.textContent = text;
    const icon = statusIndicator.querySelector('i');
    icon.className = 'fas fa-circle';
    
    if (type === 'success') {
        icon.style.color = '#10b981';
    } else if (type === 'warning') {
        icon.style.color = '#f59e0b';
    } else {
        icon.style.color = '#ef4444';
    }
}

// Send Message
async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    if (!config.api_url || !config.api_key) {
        addMessage('bot', 'Please configure your API settings first by clicking the Configuration button.');
        return;
    }
    
    // Add user message
    addMessage('user', message);
    chatInput.value = '';
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<span class="loading"></span>';
    updateStatus('Processing...', 'warning');
    
    try {
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                api_url: config.api_url,
                api_key: config.api_key,
                agent_id: config.agent_id
            })
        });
        
        const data = await response.json();
        
        if (data.success && !data.response?.error) {
            const responseText = formatResponse(data.response);
            addMessage('bot', responseText);
            updateStatus('Ready', 'success');
        } else {
            const errorMsg = data.response?.error || data.error || 'Unknown error occurred';
            addMessage('bot', `Error: ${errorMsg}`, true);
            updateStatus('Error', 'error');
            
            // Show helpful message for 401 errors
            if (errorMsg.includes('401') || errorMsg.includes('Unauthorized')) {
                addMessage('bot', '💡 Tip: Check your API key in the Configuration. Make sure it\'s not empty and is valid.', false);
            }
        }
    } catch (error) {
        addMessage('bot', `Network error: ${error.message}`, true);
        updateStatus('Connection error', 'error');
    } finally {
        sendBtn.disabled = false;
        sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
    }
}

// Quick Actions
async function executeQuickAction(action) {
    if (!config.api_url || !config.api_key) {
        addMessage('bot', 'Please configure your API settings first by clicking the Configuration button.');
        return;
    }
    
    const actionNames = {
        'check_low_stock': 'Check Low Stock',
        'get_lowest_sales': 'Get Lowest Sales',
        'get_top_sales': 'Get Top Sales',
        'analyze_christmas': 'Analyze Christmas Trends',
        'reorder_low_stock': 'Reorder Low Stock',
        'full_workflow': 'Full Workflow'
    };
    
    const actionName = actionNames[action] || action;
    addMessage('user', `Execute: ${actionName}`);
    updateStatus('Processing...', 'warning');
    
    try {
        const response = await fetch(`${API_BASE}/api/quick-action`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: action,
                api_url: config.api_url,
                api_key: config.api_key,
                agent_id: config.agent_id
            })
        });
        
        const data = await response.json();
        
        if (data.success && !data.response?.error) {
            const responseText = formatResponse(data.response);
            addMessage('bot', responseText);
            updateStatus('Ready', 'success');
        } else {
            const errorMsg = data.response?.error || data.error || 'Unknown error occurred';
            addMessage('bot', `Error: ${errorMsg}`, true);
            updateStatus('Error', 'error');
            
            // Show helpful message for 401 errors
            if (errorMsg.includes('401') || errorMsg.includes('Unauthorized')) {
                addMessage('bot', '💡 Tip: Check your API key in the Configuration. Make sure it\'s not empty and is valid.', false);
            }
        }
    } catch (error) {
        addMessage('bot', `Network error: ${error.message}`, true);
        updateStatus('Connection error', 'error');
    }
}

// Add Message to Chat
function addMessage(role, content, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    if (role === 'bot') {
        const icon = document.createElement('i');
        icon.className = 'fas fa-robot';
        contentDiv.appendChild(icon);
    }
    
    if (typeof content === 'string') {
        const p = document.createElement('p');
        if (isError) {
            p.className = 'error-message';
        }
        p.textContent = content;
        contentDiv.appendChild(p);
    } else {
        const pre = document.createElement('pre');
        pre.textContent = JSON.stringify(content, null, 2);
        contentDiv.appendChild(pre);
    }
    
    messageDiv.appendChild(contentDiv);
    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;
}

// Format Response
function formatResponse(response) {
    if (typeof response === 'string') {
        return response;
    }
    
    if (response.error) {
        return `Error: ${response.error}`;
    }
    
    // Try to extract meaningful information
    if (response.message) {
        return response.message;
    }
    
    if (response.output) {
        return response.output;
    }
    
    // Return formatted JSON
    return JSON.stringify(response, null, 2);
}

// Clear Chat
function clearChatMessages() {
    messages.innerHTML = `
        <div class="message bot-message">
            <div class="message-content">
                <i class="fas fa-robot"></i>
                <p>Chat cleared. How can I help you?</p>
            </div>
        </div>
    `;
}

