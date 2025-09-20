document.addEventListener('DOMContentLoaded', () => {
    // Multilingual support
    const langSelect = document.getElementById('language-select');
    if (langSelect) {
        langSelect.addEventListener('change', (e) => {
            const lang = e.target.value;
            fetch(`/lang/${lang}`)
                .then(res => res.json())
                .then(data => {
                    // Translate all elements with data-i18n attribute
                    document.querySelectorAll('[data-i18n]').forEach(el => {
                        const key = el.getAttribute('data-i18n');
                        if(data[key]) el.textContent = data[key];
                    });
                    // Placeholder translation for chatbot input
                    const chatInput = document.getElementById('chatbot-input');
                    if(chatInput && data['chatbot_placeholder']){
                        chatInput.placeholder = data['chatbot_placeholder'];
                    }
                });
        });
    }

    // Chatbot logic
    const chatForm = document.getElementById('chatbot-form');
    const chatInput = document.getElementById('chatbot-input');
    const chatMessages = document.getElementById('chatbot-messages');

    if(chatForm && chatInput && chatMessages){
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if(message === '') return;
            appendMessage(message, 'farmer');
            chatInput.value = '';
            fetch('/chatbot', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            })
            .then(res => res.json())
            .then(data => {
                appendMessage(data.reply, 'bot');
                chatMessages.scrollTop = chatMessages.scrollHeight;
            })
            .catch(() => {
                appendMessage("Sorry, I am unable to respond right now.", 'bot');
            });
        });
    }

    function appendMessage(text, sender){
        const div = document.createElement('div');
        div.classList.add('message', sender);
        div.textContent = text;
        chatMessages.appendChild(div);
    }
});
