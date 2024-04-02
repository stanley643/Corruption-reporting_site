document.addEventListener("DOMContentLoaded", function() {
    // Get the chat form and input field
    const chatForm = document.getElementById('send-message-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');

    // Function to send messages via AJAX
    const sendMessage = function(messageContent) {
        var senderUsername = '{{ request.user.username }}'; // Assuming user is authenticated
        var chatRoomId = '{{ chat_room.id }}'; // Assuming chat room ID is passed in template
        var timestamp = new Date().toISOString(); // Current timestamp

        // AJAX request to send message
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/send-message/');
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function() {
            if (xhr.status === 200) {
                // Message sent successfully, update chat interface
                var message = {
                    content: messageContent,
                    sender: senderUsername,
                    timestamp: timestamp
                };
                displayMessage(message);
                messageInput.value = ''; // Clear input field
            }
        };
        xhr.send(JSON.stringify({content: messageContent, sender: senderUsername, chat_room_id: chatRoomId, timestamp: timestamp}));
    };

    // Function to display received messages
    function displayMessage(message) {
        var messageElement = document.createElement('div');
        messageElement.textContent = message.content + ' - ' + message.sender + ' (' + message.timestamp + ')';
        chatMessages.appendChild(messageElement);
    }

    // Event listener for form submission
    chatForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission behavior

        // Get the message content
        const message = messageInput.value.trim();

        // Check if message is not empty
        if (message !== '') {
            // Send the message
            sendMessage(message);
        }
    });
});

