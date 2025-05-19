document.addEventListener('DOMContentLoaded', function () {
    let chatContent = document.getElementById('chat-content');
    const chatForm = document.getElementById('chat-message-form');
    const backBtn = document.getElementById('back-btn');
    const initialChatContentHTML = chatContent.innerHTML;

    let ticketSelector = document.getElementById('ticket-selector');
    let ticketSelectorContainer = document.getElementById('ticket-selector-container');
    let chatBoxAuth = document.querySelector('.chat-box-auth');
    let ticketInput = document.getElementById("ticket-input");
    let sendTicketBtn = document.getElementById("send-ticket-btn");
    const input = document.getElementById('chat-message-input');

    backBtn.style.display = 'none';

    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue;
    }

    function loadMessages(ticketId) {
        console.log("Loading messages for ticket:", ticketId);
        fetch(`/api/messages/?ticket_id=${ticketId}`, {
            headers: { "X-CSRFToken": getCSRFToken() }
        })
        .then(response => {
            if (!response.ok) throw new Error("Failed to fetch messages.");
            return response.json();
        })
        .then(messages => {
            chatContent.innerHTML = '';
            const chatWindow = document.createElement('div');
            chatWindow.className = 'chat-window';

            messages.forEach(msg => {
                const msgDiv = document.createElement('div');
                msgDiv.className = `chat-message ${msg.sender_username === CURRENT_USERNAME ? 'from-user' : 'from-admin'}`;
                msgDiv.innerHTML = `
                    <div class="chat-meta"><strong>${msg.sender_username}</strong> • <span class="chat-time">${msg.created_at}</span></div>
                    <div class="chat-text">${msg.message}</div>
                `;
                chatWindow.appendChild(msgDiv);
            });

            chatContent.appendChild(chatWindow);
            chatContent.scrollTop = chatContent.scrollHeight;
        })
        .catch(error => {
            console.error(error);
        });
    }

    function attachTicketSelectorListener() {
        ticketSelector = document.getElementById('ticket-selector');
        ticketSelector?.addEventListener('change', function () {
            const selectedId = ticketSelector.value;
            console.log("Ticket selected:", selectedId);
            if (selectedId) {
                loadMessages(selectedId);
                chatForm.style.display = 'flex';
                backBtn.style.display = 'inline-block';
                ticketSelectorContainer.style.display = 'none';
                chatBoxAuth.style.display = 'none';
            } else {
                chatContent.innerHTML = '';
                chatForm.style.display = 'none';
                backBtn.style.display = 'none';
                ticketSelectorContainer.style.display = 'block';
                chatBoxAuth.style.display = 'block';
            }
        });
    }

    function loadUserTickets() {
        fetch("/api/tickets/", {
            headers: { "X-CSRFToken": getCSRFToken() }
        })
        .then(response => response.json())
        .then(tickets => {
            ticketSelector.innerHTML = `<option value="">-- Select a Ticket --</option>`;

            if (tickets.length > 0) {
                tickets.forEach(ticket => {
                    const option = document.createElement('option');
                    option.value = ticket.id;
                    option.textContent = `#${ticket.id} - ${ticket.subject}`;
                    ticketSelector.appendChild(option);
                });

                ticketSelectorContainer.style.display = 'block';
                chatBoxAuth.style.display = 'block';
            } else {
                ticketSelectorContainer.style.display = 'none';
                chatBoxAuth.style.display = 'block';
            }

            attachTicketSelectorListener();
        })
        .catch(error => {
            console.error("Failed to load tickets:", error);
            ticketSelectorContainer.style.display = 'none';
            chatBoxAuth.style.display = 'block';
        });
    }

    function attachTicketCreationListener() {
        const sendTicketBtn = document.getElementById('send-ticket-btn');
        const ticketInput = document.getElementById('ticket-input');

        if (!sendTicketBtn || !ticketInput) return;

        sendTicketBtn.addEventListener('click', function () {
            console.log("Send ticket clicked");
            const subject = ticketInput.value.trim();

            if (!subject) {
                alert("Please enter a subject before submitting.");
                return;
            }

            fetch("/api/tickets/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(),
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
                ticketInput.value = "";

                fetch("/api/messages/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken(),
                    },
                    body: JSON.stringify({
                        ticket: data.id,
                        message: data.subject
                    })
                });

                loadUserTickets();
                ticketSelector.value = data.id;
                loadMessages(data.id);
                chatForm.style.display = 'flex';
                backBtn.style.display = 'inline-block';
                ticketSelectorContainer.style.display = 'none';
                chatBoxAuth.style.display = 'none';
            })
            .catch(error => {
                console.error("Error:", error.message);
                alert("Failed to submit ticket: " + error.message);
            });
        });
    }

    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const message = input.value.trim();
        const selectedTicketId = ticketSelector.value;

        if (!message || !selectedTicketId) return;

        fetch("/api/messages/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({
                ticket: selectedTicketId,
                message: message
            })
        })
        .then(response => {
            if (!response.ok) throw new Error("Failed to send message.");
            return response.json();
        })

        .then(data => {
            input.value = '';
            loadMessages(selectedTicketId);
        })
        .catch(error => {
            console.error(error);
            alert("Failed to send message: " + error.message);
        });
    });


    backBtn.addEventListener('click', function () {
        chatContent.innerHTML = initialChatContentHTML;

        chatForm.style.display = 'none';
        backBtn.style.display = 'none';

        reattachElementsAndListeners();
        loadUserTickets();
    });

    function reattachElementsAndListeners() {
        ticketSelector = document.getElementById('ticket-selector');
        ticketSelectorContainer = document.getElementById('ticket-selector-container');
        chatBoxAuth = document.querySelector('.chat-box-auth');
        ticketInput = document.getElementById("ticket-input");
        sendTicketBtn = document.getElementById("send-ticket-btn");

        attachTicketSelectorListener();
        attachTicketCreationListener();
    }

    // Initial event listener for ticket selector change (global)
    document.addEventListener('change', function (e) {
        if (e.target && e.target.id === 'ticket-selector') {
            const selectedId = e.target.value;
            console.log("Global event: Ticket selected:", selectedId);
            if (selectedId) {
                loadMessages(selectedId);
                chatForm.style.display = 'flex';
                backBtn.style.display = 'inline-block';
                ticketSelectorContainer.style.display = 'none';
                chatBoxAuth.style.display = 'none';
            }
        }
    });

    // Initial calls on page load
    attachTicketCreationListener();
    loadUserTickets();
});
