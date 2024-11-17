document.addEventListener('DOMContentLoaded', () => {
    const chatHistory = document.getElementById('chatHistory');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    // Auto-resize textarea as user types
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = userInput.scrollHeight + 'px';
    });

    // Handle enter key (send on Enter, new line on Shift+Enter)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendButton.addEventListener('click', sendMessage);

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessageToChat(message, 'user');

        // Clear input
        userInput.value = '';
        userInput.style.height = 'auto';

        // Disable input while processing
        setInputState(false);

        try {
            const response = await fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: message }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Add system response to chat
            addMessageToChat(data.guidance, 'system');
        } catch (error) {
            addMessageToChat('Sorry, there was an error processing your request.', 'system');
            console.error('Error:', error);
        } finally {
            setInputState(true);
        }
    }

    function addMessageToChat(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${type}-message`);
        messageDiv.textContent = message;
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function setInputState(enabled) {
        userInput.disabled = !enabled;
        sendButton.disabled = !enabled;
    }
}); 