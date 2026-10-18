const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const messages = document.getElementById("messages");
const welcome = document.getElementById("welcome");
const sendButton = document.getElementById("send-button");
const newChatButton = document.getElementById("new-chat");

let history = [];
let isSending = false;

function addMessage(role, content = "", isError = false) {
    const message = document.createElement("div");
    message.className = `message ${role}${isError ? " error" : ""}`;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = role === "user" ? "●" : "✦";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = content;

    message.append(avatar, bubble);
    messages.appendChild(message);

    message.scrollIntoView({
        behavior: "smooth",
        block: "end"
    });

    return bubble;
}

function scrollToBottom() {
    messages.lastElementChild?.scrollIntoView({
        behavior: "smooth",
        block: "end"
    });
}

async function sendMessage(text) {
    const question = text.trim();

    if (!question || isSending) return;

    isSending = true;
    sendButton.disabled = true;
    input.disabled = true;

    welcome.style.display = "none";

    addMessage("user", question);

    const assistantBubble = addMessage("assistant", "");
    const previousHistory = [...history];

    history.push({
        role: "user",
        content: question
    });

    input.value = "";
    input.style.height = "auto";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: question,
                history: previousHistory
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(
                errorData.error || `Server error: ${response.status}`
            );
        }

        if (!response.body) {
            throw new Error("Streaming is not supported by this response.");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let answer = "";

        while (true) {
            const { value, done } = await reader.read();

            if (done) break;

            answer += decoder.decode(value, { stream: true });
            assistantBubble.textContent = answer;
            scrollToBottom();
        }

        answer += decoder.decode();
        assistantBubble.textContent = answer;

        history.push({
            role: "assistant",
            content: answer
        });

        history = history.slice(-6);

    } catch (error) {
        assistantBubble.textContent =
            "Sorry, something went wrong. " + error.message;

        assistantBubble.parentElement.classList.add("error");

        console.error("Chat error:", error);

    } finally {
        isSending = false;
        sendButton.disabled = false;
        input.disabled = false;
        input.focus();
    }
}

form.addEventListener("submit", function (event) {
    event.preventDefault();
    sendMessage(input.value);
});

input.addEventListener("input", function () {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 150) + "px";
});

input.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        form.requestSubmit();
    }
});

document.querySelectorAll(".suggestion").forEach(button => {
    button.addEventListener("click", () => {
        sendMessage(button.dataset.question);
    });
});

newChatButton.addEventListener("click", () => {
    if (isSending) return;

    messages.replaceChildren();
    history = [];
    welcome.style.display = "block";
    input.value = "";
    input.focus();
});