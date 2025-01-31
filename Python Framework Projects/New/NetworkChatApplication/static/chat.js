if (!window.chatScriptInitialized) {
    window.chatScriptInitialized = true;

    // Get the chatbox element
    const chatbox = document.querySelector("#chatbox");

    // Function to scroll the chatbox to the bottom
    function scrollToBottom() {
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    // Scroll to bottom on page load
    scrollToBottom();

    // Get room name and username from the template
    const roomName = JSON.parse(document.getElementById('room_slug').textContent);
    const username = JSON.parse(document.getElementById('username').textContent);

    // Create WebSocket connection
    const chatSocket = new WebSocket(`ws://${window.location.host}/ws/${roomName}/`);

    // Handle WebSocket connection open
    chatSocket.onopen = function () {
        console.log("WebSocket connection established successfully!");
    };

    // Handle WebSocket connection close
    chatSocket.onclose = function () {
        console.log("WebSocket connection closed.");
    };

    // Handle WebSocket errors
    chatSocket.onerror = function (e) {
        console.error("WebSocket error:", e); // Log WebSocket errors
    };

    // Handle Enter key press in the input field
    document.querySelector("#my_input").focus();
    document.querySelector("#my_input").onkeyup = function (e) {
        if (e.keyCode === 13) {  // Enter key
            e.preventDefault();
            document.querySelector("#submit_button").click();
        }
    };

    // Handle Send button click
    document.querySelector("#submit_button").onclick = function (e) {
        const messageInput = document.querySelector("#my_input").value.trim();

        if (messageInput.length === 0) {
            alert("Please enter a message before sending.");
        } else {
            // Send message via WebSocket
            chatSocket.send(JSON.stringify({
                message: messageInput,
                username: username,
                room_name: roomName,
            }));

            // Clear input field after sending the message
            document.querySelector("#my_input").value = "";
        }
    };

    // Handle incoming WebSocket messages
    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        // Create a new message div
        const div = document.createElement("div");

        // Add the message with sender's name
        div.innerHTML = `<b>${data.username}</b>: ${data.message}`;

        // Align messages based on the user
        if (data.username === username) {
            div.classList.add("chat-message", "text-right");
        } else {
            div.classList.add("chat-message", "text-left");
        }

        // Append the new message to the chatbox and scroll to the bottom
        document.querySelector("#chatbox").appendChild(div);
        scrollToBottom();
    };

    // Handle any additional issues with the chat
    window.addEventListener("beforeunload", function () {
        // Ensure WebSocket is closed when the page is being unloaded (optional)
        if (chatSocket.readyState === WebSocket.OPEN) {
            chatSocket.close();
        }
    });
}
