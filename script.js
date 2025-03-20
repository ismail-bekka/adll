function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim();
    let chatBox = document.getElementById("chat-box");

    if (userInput === "") return;

    chatBox.innerHTML += `
        <div class="user-message">
            <span>${userInput}</span>
            <img src="/static/user.png">
        </div>
    `;
    document.getElementById("user-input").value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `
            <div class="bot-message">
                <img src="/static/bot.png">
                <span>${data.response}</span>
            </div>
        `;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function clearChat() {
    document.getElementById("chat-box").innerHTML = `
        <div class="bot-message">
            <img src="/static/bot.png">
            <span>تم مسح المحادثة! كيف يمكنني مساعدتك الآن؟ 😊</span>
        </div>
    `;
}
