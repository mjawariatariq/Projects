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
                        username: "{{ request.user.username }}",
                    })
                );
                messageInput.value = "";  // Clear the input after sending
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
});
