const input = document.getElementById("message");

input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

async function sendMessage() {

    let message = input.value.trim();

    if(message === "") return;

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `
        <div class="message user">
            ${message}
        </div>
    `;

    input.value = "";

    chatBox.innerHTML += `
        <div class="message bot typing" id="typing">
            Thinking...
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    const response = await fetch("/chat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            message:message
        })
    });

    const data = await response.json();

    document.getElementById("typing").remove();

    chatBox.innerHTML += `
        <div class="message bot">
            ${data.response.replace(/\\n/g, "<br>")}
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;
}
function quickAsk(text){
    document.getElementById("message").value = text;
    sendMessage();
}