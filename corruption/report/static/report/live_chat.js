// JavaScript code to handle sending and receiving messages
function sendMessage() {
    // Get message content from input field
    var message = document.getElementById('message-input').value;
    var postId = document.getElementById('post-id').value;

    // Send AJAX request to send_message view
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/send_message/');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Clear input field after successful sending
            document.getElementById('message-input').value = '';
        }
    };
    xhr.send('post_id=' + postId + '&message=' + encodeURIComponent(message));
}

function loadMessages(postId) {
    // Send AJAX request to get_messages view
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_messages/' + postId);
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Parse JSON response and update chat interface
            var messages = JSON.parse(xhr.responseText);
            var chatMessages = document.getElementById('chat-messages');
            chatMessages.innerHTML = '';
            messages.forEach(function(message) {
                var p = document.createElement('p');
                p.innerHTML = '<strong>' + message.user + ':</strong> ' + message.content;
                chatMessages.appendChild(p);
            });
        }
    };
    xhr.send();
}


document.addEventListener("DOMContentLoaded", function() {
    // Get the chat form and input field
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');

    // Function to send messages via AJAX
    const sendMessage = function(message) {
        // Send the message to the server via AJAX
        // Replace this with your actual AJAX implementation
        // For example:
        // fetch('/send-message/', {
        //     method: 'POST',
        //     body: JSON.stringify({ message: message }),
        //     headers: {
        //         'Content-Type': 'application/json'
        //     }
        // }).then(response => {
        //     // Handle response
        // });
        
        // For demonstration purposes, we'll just append the message to the chatbox
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        
        // Clear the input field after sending the message
        messageInput.value = '';
    };

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

document.getElementById('send-message-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var messageContent = document.getElementById('message-input').value;
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
            document.getElementById('message-input').value = ''; // Clear input field
        }
    };
    xhr.send(JSON.stringify({content: messageContent, sender: senderUsername, chat_room_id: chatRoomId, timestamp: timestamp}));
});

function displayMessage(message) {
    var messageElement = document.createElement('div');
    messageElement.textContent = message.content + ' - ' + message.sender + ' (' + message.timestamp + ')';
    document.getElementById('chat-messages').appendChild(messageElement);
}
