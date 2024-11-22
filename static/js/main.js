document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatHistory = document.getElementById('chatHistory');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    // Auto-resize textarea as user types
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        const height = Math.min(userInput.scrollHeight, 200);
        userInput.style.height = `${height}px`;
    });

    // Handle Enter key
    userInput.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            await handleSubmit();
        }
    });

    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await handleSubmit();
    });

    async function handleSubmit() {
        const message = userInput.value.trim();
        if (!message || userInput.disabled) return;

        try {
            // Disable input while processing
            setInputState(false);

            // Add user message
            addMessage('user', message);

            // Clear input and reset height
            userInput.value = '';
            userInput.style.height = 'auto';

            // Show loading state
            const loadingId = showLoadingMessage();

            // Send to backend
            const response = await fetch('/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: message })
            });

            // Remove loading message
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

        // Format the content if it contains newlines
        const formattedContent = content.replace(/\n/g, '<br>');
        messageContent.innerHTML = formattedContent;

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