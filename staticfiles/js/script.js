// Get CSRF token from Django template
const getCSRFToken = () => {
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return csrfInput ? csrfInput.value : '';
};

document.addEventListener('DOMContentLoaded', function() {
    // Chat history array and storage functions
    let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
    
    function saveToHistory(sender, message) {
        chatHistory.push({
            sender: sender,
            message: message,
            timestamp: new Date().toISOString()
        });
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    }
    
    function loadChatHistory() {
        const chatContainer = document.getElementById('id_chat_item_container');
        chatContainer.innerHTML = '';
        chatHistory.forEach(item => {
            const messageClass = item.sender === 'You' ? 'user-message' : 'ai-message';
            chatContainer.innerHTML += `<div class="${messageClass}">${item.sender}: ${item.message}</div>`;
        });
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Clean response function
    function cleanResponse(text) {
        return text
            .replace(/\*\*/g, '')      
            .replace(/\*/g, '')        
            .replace(/#{1,6}/g, '')   
            .replace(/###/g, '') 
            .replace(/```[\s\S]*?```/g, '\n')  
            .replace(/`/g, '')         
            .replace(/\n{3,}/g, '\n\n') 
            .replace(/\n/g, '<br>')    
            .trim();
    }

    // Load existing chat history when page loads
    loadChatHistory();

    // Handle problem description form submission
    document.getElementById('problem-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const input = document.getElementById('problem-input').value;
        const chatContainer = document.getElementById('id_chat_item_container');
        
        if (!input) return;
        
        try {
            // Add user message to chat and history
            const userMessage = `You: ${input}`;
            chatContainer.innerHTML += `<div class="user-message">${userMessage}</div>`;
            saveToHistory('You', input);
            
            // Send to API with proper CSRF token
            const response = await fetch('/api/conversation/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ input: input })
            });
            
            const data = await response.json();
            
            // Add AI response to chat and history
            if (data.response) {
                const cleanMessage = cleanResponse(data.response);
                chatContainer.innerHTML += `<div class="ai-message">AI: ${cleanMessage}</div>`;
                saveToHistory('AI', cleanMessage);
            } else if (data.error) {
                const cleanError = cleanResponse(data.error);
                chatContainer.innerHTML += `<div class="error-message">Error: ${cleanError}</div>`;
                saveToHistory('System', cleanError);
            }
            
        } catch (error) {
            console.error('Error:', error);
            chatContainer.innerHTML += `<div class="error-message">Connection error</div>`;
        }
    });

    // Handle live chat message submission
    document.getElementById('id_message_send_button')?.addEventListener('click', async function() {
        const input = document.getElementById('id_message_send_input').value;
        const chatContainer = document.getElementById('id_chat_item_container');
        
        if (!input) return;
        
        try {
            // Add user message to chat and history
            const userMessage = `You: ${input}`;
            chatContainer.innerHTML += `<div class="user-message">${userMessage}</div>`;
            saveToHistory('You', input);
            
            // Send to API with proper CSRF token
            const response = await fetch('/api/conversation/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ input: input })
            });
            
            const data = await response.json();
            
            // Add AI response to chat and history
            if (data.response) {
                const cleanMessage = cleanResponse(data.response);
                chatContainer.innerHTML += `<div class="ai-message">AI: ${cleanMessage}</div>`;
                saveToHistory('AI', cleanMessage);
            } else if (data.error) {
                const cleanError = cleanResponse(data.error);
                chatContainer.innerHTML += `<div class="error-message">Error: ${cleanError}</div>`;
                saveToHistory('System', cleanError);
            }
            
            // Clear input
            document.getElementById('id_message_send_input').value = '';
            
        } catch (error) {
            console.error('Error:', error);
            chatContainer.innerHTML += `<div class="error-message">Connection error</div>`;
        }
    });

    // Refresh button functionality - UPDATED TO CLEAR CHAT
    document.getElementById('refresh-chat')?.addEventListener('click', function() {
        // Clear both the display AND the history
        const chatContainer = document.getElementById('id_chat_item_container');
        chatContainer.innerHTML = '';
        chatHistory = [];
        localStorage.removeItem('chatHistory');
    });
});