import {PageManager} from "./page-manager.js";

function createMessageHTML(message) {
    return `<span class="timestamp">${message.created_at}</span>
            <span class="username">${message.sender}</span>
            <span class="content">${message.content}</span>`
}

PageManager.getInstance().setOnPageLoad("chat", function () {
    document.getElementById("submit-create-room")
        .addEventListener("click", function (event) {
            console.log("create room")
            const roomName = document.getElementById("new-room-name").value;
            if (!roomName.trim()) {
                alert("Room name cannot be empty");
                return;
            }
            fetch("/api/chat/room/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: roomName,
                    is_direct: false
                })
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error("Failed to create room");
                    }
                })
                .then(data => {
                    console.log(data)
                    PageManager.getInstance().load("chat")
                })
                .catch(error => {
                    alert(error.message);
                })
        })

    // Open websocket and bind send-message button
    let ws = null;
    let roomId = null
    if (document.getElementById("room-id")) {
        roomId = document.getElementById("room-id").innerHTML;
        ws = new WebSocket(`wss://${window.location.host}/ws/chat/${roomId}/`);

        ws.onmessage = function (event) {
            const data = JSON.parse(event.data);
            const message = document.createElement("div");
            message.className = "message";
            message.innerHTML = createMessageHTML(data.message);
            document.getElementById("chat-log").appendChild(message);
            document.getElementById("chat-log").scrollTop = document.getElementById("chat-log").scrollHeight;
        }

        // Scroll smoothly to the bottom of the chat log
        document.getElementById("chat-log").scrollTop = document.getElementById("chat-log").scrollHeight;

        document.getElementById("send-message").addEventListener("click", function (event) {
            const message = document.getElementById("chat-input").value;
            if (!message.trim()) {
                alert("Message cannot be empty");
                return;
            }
            ws.send(JSON.stringify({
                message: message
            }))
            document.getElementById("chat-input").value = "";
            document.getElementById("chat-log").scrollTop = document.getElementById("chat-log").scrollHeight;
        })
    }


    for (let roomButton of document.getElementsByClassName("room-button")) {
        roomButton.addEventListener("click", function (event) {
            // Close current websocket
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.close();
            }
            PageManager.getInstance().load("chat", false, {query: `?room=${roomButton.getAttribute("data-room-id")}`})
        })
    }


})