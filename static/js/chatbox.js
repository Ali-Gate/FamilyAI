document.addEventListener('DOMContentLoaded', function () {
    const sendBtn = document.getElementById('send-ticket-btn');
    const chatContent = document.getElementById('chat-content');
    const chatForm = document.getElementById('chat-message-form');
    const input = document.getElementById('chat-message-input');

    const currentTime = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    if (sendBtn) {
        sendBtn.addEventListener('click', function () {
            // Simulate ticket creation
            const chatWindow = document.createElement('div');
            chatWindow.className = 'chat-window fade-in';
            chatWindow.innerHTML = `
                <div class="chat-message from-user">
                    <div class="chat-meta"><strong>johndoe</strong> • <span class="chat-time">${currentTime()}</span></div>
                    <div class="chat-text">Hi, I need help with my account.</div>
                </div>
                <div class="chat-message from-admin">
                    <div class="chat-meta"><strong>support-agent</strong> • <span class="chat-time">${currentTime()}</span></div>
                    <div class="chat-text">Sure, I'd be happy to help! Can you tell me more?</div>
                </div>
            `;
            chatContent.innerHTML = '';
            chatContent.appendChild(chatWindow);
            chatContent.scrollTop = chatContent.scrollHeight;

            // Show the input form now that chat has started
            chatForm.style.display = 'flex';
        });
    }

    // Handle message sending
    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const message = input.value.trim();
        if (!message) return;

        const msgDiv = document.createElement('div');
        msgDiv.className = 'chat-message from-user';
        msgDiv.innerHTML = `
            <div class="chat-meta"><strong>johndoe</strong> • <span class="chat-time">${currentTime()}</span></div>
            <div class="chat-text">${message}</div>
        `;
        const chatWindow = chatContent.querySelector('.chat-window');
        chatWindow.appendChild(msgDiv);
        chatContent.scrollTop = chatContent.scrollHeight;
        input.value = '';
    });
});