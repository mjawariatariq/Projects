document.addEventListener("DOMContentLoaded", function () {
    const chatbox = document.querySelector("#chatbox");
  
    // Properly render and escape room_name in JS
    const roomName = document.getElementById("room_name").dataset.roomName;
  
    // Log room name after it's initialized
    console.log("Room Name: ", roomName); // This should print the actual room name
  
    // Function to scroll the chatbox to the bottom
    function scrollToBottom() {
      chatbox.scrollTop = chatbox.scrollHeight;
    }
    scrollToBottom();
  
    // WebSocket connection
    const chatSocket = new WebSocket(
      "ws://" + window.location.host + "/ws/" + roomName + "/"
    );
  
    chatSocket.onopen = function (e) {
      console.log("The connection was setup successfully!");
    };
  
    chatSocket.onclose = function (e) {
      console.log("Something unexpected happened!");
    };
  
    document.querySelector("#submit_button").onclick = function (e) {
      var messageInput = document.querySelector("#my_input").value;
      if (messageInput.length == 0) {
        alert("Add some input first or press the send button!");
      } else {
        chatSocket.send(
          JSON.stringify({
            message: messageInput,
            username: "{{ request.user.username }}",
            room_name: roomName,
          })
        );
      }
    };
  
    // Handle incoming WebSocket messages
    chatSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      var div = document.createElement("div");
      div.innerHTML = "<b>" + data.username + "</b> : " + data.message;
  
      if (data.username === "{{ request.user.username }}") {
        div.classList.add("chat-message", "text-right");
      } else {
        div.classList.add("chat-message", "text-left");
      }
  
      document.querySelector("#my_input").value = "";
      document.querySelector("#chatbox").appendChild(div);
      scrollToBottom();
    };
  });
  
