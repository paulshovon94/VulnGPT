document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatHistory = document.getElementById('chatHistory');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    // Auto-resize textarea as user types
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = `${userInput.scrollHeight}px`;
    });

    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleSubmit();
    });

    // Handle enter key
    userInput.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            await handleSubmit();
        }
    });

    // Handle button click
    sendButton.addEventListener('click', async (e) => {
        e.preventDefault();
        await handleSubmit();
    });

    // Add this function to validate the limit input
    function validateLimit(input) {
        let value = parseInt(input.value);
        if (isNaN(value) || value < 1) {
            value = 1;
        } else if (value > 100) {
            value = 100;
        }
        input.value = value;
        return value;
    }

    // Add this event listener after your DOMContentLoaded
    document.getElementById('resultLimit').addEventListener('change', function() {
        validateLimit(this);
    });

    // Update the handleSubmit function to use the validated limit
    async function handleSubmit() {
        const message = userInput.value.trim();
        const limitInput = document.getElementById('resultLimit');
        const limit = validateLimit(limitInput);
        
        if (!message || userInput.disabled) return;

        try {
            setInputState(false);
            addMessage('user', message);
            userInput.value = '';
            userInput.style.height = 'auto';

            const loadingId = showLoadingMessage();

            const response = await fetch('/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    query: message,
                    limit: limit
                })
            });

            removeLoadingMessage(loadingId);

            if (!response.ok) throw new Error('Network response was not ok');
            
            const data = await response.json();
            addMessage('system', data.guidance);

        } catch (error) {
            console.error('Error:', error);
            addMessage('system', 'Sorry, there was an error processing your request.');
        } finally {
            setInputState(true);
            scrollToBottom();
        }
    }

    function addMessage(type, content) {
        const messageContainer = document.createElement('div');
        messageContainer.className = `message-container ${type}-container`;

        const messageContent = document.createElement('div');
        messageContent.className = `message ${type}-message`;
        messageContent.innerHTML = content.replace(/\n/g, '<br>');

        messageContainer.appendChild(messageContent);
        chatHistory.appendChild(messageContainer);
        scrollToBottom();
    }

    function showLoadingMessage() {
        const loadingContainer = document.createElement('div');
        loadingContainer.className = 'message-container system-container loading';
        loadingContainer.innerHTML = `
            <div class="message system-message">
                <div class="loading-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        chatHistory.appendChild(loadingContainer);
        scrollToBottom();
        return loadingContainer.id = 'loading-' + Date.now();
    }

    function removeLoadingMessage(loadingId) {
        const loadingElement = document.getElementById(loadingId);
        if (loadingElement) {
            loadingElement.remove();
        }
    }

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function setInputState(enabled) {
        userInput.disabled = !enabled;
        sendButton.disabled = !enabled;
        if (enabled) {
            userInput.focus();
        }
    }

    // Focus input on page load
    userInput.focus();
}); 