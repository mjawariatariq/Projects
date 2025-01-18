const chatbox = document.querySelector("#chatbox");

// Chatbox ko neeche scroll karne ka function
function scrollToBottom() {
    chatbox.scrollTop = chatbox.scrollHeight;
}

// Page load hone par chatbox ko neeche scroll karwana
scrollToBottom();

const roomName = JSON.parse(document.getElementById('room_slug').textContent);
const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/" + roomName + "/");

// WebSocket connection open hone par message
chatSocket.onopen = function (e) {
    console.log("The connection was setup successfully !");
};
chatSocket.onclose = function (e) {
    console.log("Something unexpected happened !");
};

// Input field mein enter key press hone par send button ko trigger karna
document.querySelector("#my_input").focus();
document.querySelector("#my_input").onkeyup = function (e) {
    if (e.keyCode == 13) {
        e.preventDefault();
        document.querySelector("#submit_button").click();
    }
};

// Send button click hone par message send karna
document.querySelector("#submit_button").onclick = function (e) {
    var messageInput = document.querySelector(
        "#my_input"
    ).value;

    // Agar message empty hai to alert dikhana
    if (messageInput.length == 0) {
        alert("Add some Input First Or Press Send Button!")
    }
    else {
        // WebSocket ke through message send karna
        chatSocket.send(JSON.stringify({ message: messageInput, username: "{{request.user.username}}", room_name: "{{room_name}}" }));
    }

};

// WebSocket se aane wale message ko handle karna
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    var div = document.createElement("div");
    div.innerHTML = "<b>" + data.username + "</b> : " + data.message;

    // User ke according message ka alignment set karna
    if (data.username === "{{ request.user.username }}") {
        div.classList.add("chat-message", "text-right");
    } else {
        div.classList.add("chat-message", "text-left");
    }

    // Message input ko clear karna
    document.querySelector("#my_input").value = "";
    document.querySelector("#chatbox").appendChild(div);
    scrollToBottom();
};
