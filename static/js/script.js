function typeMessage(message, element) {
    let i = 0;
    let intervalId = setInterval(() => {
        if (i < message.length) {
            element.textContent += message.charAt(i);
            i++;
        } else {
            clearInterval(intervalId);
        }
    }, 10); // La vitesse de "frappe" est définie à 50 ms par caractère
}

document.getElementById('userInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById('sendBtn').click();
    }
});

document.getElementById('sendBtn').addEventListener('click', function() {
    var userInput = document.getElementById('userInput').value;
    document.getElementById('userInput').value = '';

    var userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('message', 'user-message');
    userMessageDiv.textContent = userInput;
    document.getElementById('mistralChat').appendChild(userMessageDiv);
    document.getElementById('openaiChat').appendChild(userMessageDiv.cloneNode(true));

    fetch('/get-response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        var mistralResponseDiv = document.createElement('div');
        mistralResponseDiv.classList.add('message', 'mistral-message');
        document.getElementById('mistralChat').appendChild(mistralResponseDiv);

        var openaiResponseDiv = document.createElement('div');
        openaiResponseDiv.classList.add('message', 'openai-message');
        document.getElementById('openaiChat').appendChild(openaiResponseDiv);

        // Utilisez la fonction typeMessage pour "taper" les réponses
        typeMessage(data.mistral_response, mistralResponseDiv);
        typeMessage(data.openai_response, openaiResponseDiv);

        // Faire défiler vers le dernier message
        mistralResponseDiv.scrollIntoView();
        openaiResponseDiv.scrollIntoView();
    }).catch(error => {
        console.error('Error:', error);
    });
});
