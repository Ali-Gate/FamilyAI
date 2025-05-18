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

document.addEventListener("DOMContentLoaded", function () {
    const sendTicketBtn = document.getElementById("send-ticket-btn");
    const ticketInput = document.getElementById("ticket-input");

    sendTicketBtn.addEventListener("click", function () {
        const subject = ticketInput.value.trim();

        if (!subject) {
            alert("Please enter a subject before submitting.");
            return;
        }

        fetch("/api/tickets/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),  // see helper function below
            },
            body: JSON.stringify({ subject })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.detail || "Error creating ticket.");
                });
            }
            return response.json();
        })
        .then(data => {
            console.log("Ticket created:", data);
            // You can render ticket info or transition to chat interface here
            ticketInput.value = "";
        })
        .catch(error => {
            console.error("Error:", error.message);
            alert("Failed to submit ticket: " + error.message);
        });
    });

    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue;
    }
});