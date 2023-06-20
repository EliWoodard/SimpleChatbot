document.addEventListener('DOMContentLoaded', function() {
    var userInput = document.getElementById('user-input');
    var chatLog = document.getElementById('chat-log');
  
    userInput.addEventListener('keypress', async function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            if (userInput.value.trim() !== '') {
                var userMessage = userInput.value;
  
                // Call the getBotResponse function and handle the bot's response
                var botResponse = await window.getBotResponse(userMessage);
  
                // Display user message
                var userDiv = document.createElement("div");
                userDiv.textContent = 'You: ' + userMessage;
                chatLog.appendChild(userDiv);
  
                // Display bot's response
                var botDiv = document.createElement("div");
                botDiv.textContent = 'Bot: ' + botResponse;
                chatLog.appendChild(botDiv);
  
                userInput.value = '';
            }
        }
    });
});
