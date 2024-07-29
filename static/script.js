async function sendMessage() {
    const messageInput = document.getElementById('message');
    const message = messageInput.value.trim();

    if (message === '') return;

    addMessageToChat(message, 'user');
    messageInput.value = '';

    try {
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        if (response.ok) {
            const data = await response.json();
            addMessageToChat(data.reply, 'bot');
        } else {
            console.error('Error sending message:', response.statusText);
        }
    } catch (error) {
        console.error('Error sending message:', error);
    }
}

function addMessageToChat(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);

    const iconElement = document.createElement('div');
    iconElement.classList.add('message-icon');
    iconElement.innerHTML = sender === 'user' ? 'U' : 'B'; // U for User, B for Bot

    const textElement = document.createElement('div');
    textElement.classList.add('message-text');
    textElement.textContent = message;

    messageElement.appendChild(iconElement);
    messageElement.appendChild(textElement);

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}
