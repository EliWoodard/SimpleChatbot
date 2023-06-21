async function getBotResponse(userMessage) {
    try {
        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userMessage })
        });

        const data = await response.json();
        return data.response;

    } catch (error) {
        console.error('Error:', error);
        return "Sorry, I couldn't process your request.";
    }
}

// Export the function so that it can be used in main.js
window.getBotResponse = getBotResponse;
