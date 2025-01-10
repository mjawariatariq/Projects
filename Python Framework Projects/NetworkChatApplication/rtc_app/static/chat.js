document.addEventListener('DOMContentLoaded', function () {
    let chatSocket;
    let retryCount = 0;
    const MAX_BACKOFF_TIME = 30000;
    const WS_URL = "ws://" + window.location.host + "/ws/chat/" + roomName + "/";

    // Function to establish WebSocket connection
    function connectWebSocket() {
        chatSocket = new WebSocket(WS_URL);

        chatSocket.onopen = function () {
            retryCount = 0;
        };

        chatSocket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            const div = document.createElement("div");
            div.innerHTML = `<strong>${escapeHTML(data.username)}:</strong> ${escapeHTML(data.message)}`;
            document.querySelector("#chat-log").appendChild(div);
        };

        chatSocket.onclose = function (event) {
            const retryDelay = Math.min(1000 * Math.pow(2, retryCount), MAX_BACKOFF_TIME);
            setTimeout(() => {
                retryCount++;
                connectWebSocket();
            }, retryDelay);
        };

        chatSocket.onerror = function (event) {
            console.error("WebSocket encountered an error:", event);
        };
    }

    connectWebSocket();

    const messageInput = document.querySelector("#chat-message-input");
    const sendButton = document.querySelector("#send-message");

    // Send message when send button is clicked
    if (sendButton) {
        sendButton.onclick = function () {
            if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
                const message = messageInput.value;
                chatSocket.send(
                    JSON.stringify({
                        message: message,
                        username: "{{ request.user.username }}",  // Ensure this renders the correct username
                    })
                );
                messageInput.value = "";  // Clear the input after sending

                // Show success message after sending
                showPopupMessage("Message sent successfully!", "success");
            } else {
                console.error("WebSocket is not open. Unable to send message.");
                alert("WebSocket connection lost. Attempting to reconnect...");
            }
        };
    }

    // Function to escape HTML content to prevent XSS attacks
    function escapeHTML(str) {
        const div = document.createElement("div");
        div.innerText = str;
        return div.innerHTML;
    }

    // Function to show a popup message
    function showPopupMessage(message, type) {
        const popup = document.createElement("div");
        popup.classList.add("popup-message", type); // Add type for different styles (success, error)
        popup.innerHTML = message;
        document.body.appendChild(popup);

        // Automatically hide the popup after a few seconds
        setTimeout(function () {
            popup.style.display = "none";
        }, 3000); // Hide after 3 seconds
    }

    // Form submission handling for AJAX (if needed)
    document.getElementById('chat-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevents the form from submitting normally

        let formData = new FormData(this);  // Form data including message and file (if any)
        let statusMessage = document.getElementById('status-message');  // Element to show status

        // Send the form data using Fetch API (AJAX)
        fetch("{% url 'send_message' room_name=room_name %}", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
            }
        })
        .then(response => response.json())  // Parse the response as JSON
        .then(data => {
            if (data.status === "Message sent") {
                showPopupMessage("Message sent successfully!", "success");  // Display success message
            } else {
                showPopupMessage("Error sending message.", "error");  // Display error message
            }
        })
        .catch(error => {
            showPopupMessage("An error occurred.", "error");  // Display error message on failure
        });
    });

    // Wait for the DOM to be ready
    document.addEventListener('DOMContentLoaded', function () {
        const clearChatButton = document.getElementById('clear-chat-button');
        const chatLog = document.getElementById('chat-log');

        // Event listener for clearing the chat
        clearChatButton.addEventListener('click', function () {
            // Confirm before clearing the chat
            const confirmation = confirm("Are you sure you want to clear the chat?");
            
            if (confirmation) {
                chatLog.innerHTML = ''; // Clears the chat log
                showPopupMessage("Chat cleared successfully!", "success"); // Show success message
            }
        });
    });
});
