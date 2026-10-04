const form = document.getElementById("chatForm");

const input = document.getElementById("message");

const messages =
    document.getElementById("messages");

const clearButton =
    document.getElementById("clear");
const sendButton =
    document.getElementById("sendButton");
const welcomeHeading =
    document.querySelector(".topbar h1");
const navLinks =
    document.querySelectorAll("nav a[data-section]");
let isSending = false;

if (welcomeHeading) {
    const hour = new Date().getHours();
    const greeting = hour < 12 ? "Good morning" :
        hour < 18 ? "Good afternoon" : "Good evening";
    welcomeHeading.textContent = `${greeting}, Student 👋`;
}


// ---------------- ADD MESSAGE ----------------

function addMessage(text, type) {

    const message =
        document.createElement("div");

    message.className = `message ${type}`;


    if (type === "bot") {

        const icon =
            document.createElement("div");

        icon.className = "small-bot";

        icon.innerText = "✦";

        message.appendChild(icon);
    }


    const bubble =
        document.createElement("div");

    bubble.className = "bubble";

    bubble.innerText = text;

    message.appendChild(bubble);

    messages.appendChild(message);

    messages.scrollTop =
        messages.scrollHeight;
}


// ---------------- SEND MESSAGE ----------------

async function sendMessage(text) {

    text = text.trim();

    if (!text || isSending) {
        return;
    }

    isSending = true;

    addMessage(text, "user");
    input.value = "";
    sendButton.disabled = true;
    input.disabled = true;

    const loading =
        document.createElement("div");

    loading.className = "message bot";
    const loadingIcon = document.createElement("div");
    loadingIcon.className = "small-bot";
    loadingIcon.textContent = "✦";
    const loadingBubble = document.createElement("div");
    loadingBubble.className = "bubble typing";
    loadingBubble.textContent = "CampusAI is thinking...";
    loading.append(loadingIcon, loadingBubble);

    messages.appendChild(loading);

    messages.scrollTop =
        messages.scrollHeight;


    try {

        const response =
            await fetch("/api/chat", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    message: text
                })

            });


        const data = await response.json();

        loading.remove();

        if (!response.ok) {
            throw new Error(data.error || "Unable to send your message.");
        }

        addMessage(
            data.answer,
            "bot"
        );

        await loadStats();

    } catch (error) {
        loading.remove();
        addMessage(
            error.message || "Unable to reach CampusAI. Please try again.",
            "bot"
        );
    } finally {
        isSending = false;
        sendButton.disabled = false;
        input.disabled = false;
        input.focus();
    }
}


// ---------------- FORM ----------------

form.addEventListener(
    "submit",
    function(event) {
        event.preventDefault();
        sendMessage(input.value);
    }
);


// ---------------- QUICK BUTTONS ----------------

document
    .querySelectorAll("[data-question]")
    .forEach(button => {

        button.addEventListener(
            "click",
            function() {
                sendMessage(
                    button.dataset.question
                );

                document.getElementById("chat")
                    .scrollIntoView({ behavior: "smooth" });
            }
        );

    });


// ---------------- CLEAR CHAT ----------------

clearButton.addEventListener(
    "click",
    function() {
        messages.innerHTML = "";
        addMessage("Chat cleared. Ask me anything about your college.", "bot");
    }
);

const chatObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        navLinks.forEach((link) => {
            link.classList.toggle(
                "active",
                link.dataset.section === entry.target.id
            );
        });
    });
}, { rootMargin: "-25% 0px -60% 0px" });

["dashboard", "chat", "topics"].forEach((id) => {
    const section = document.getElementById(id);
    if (section) chatObserver.observe(section);
});


// ---------------- STATISTICS ----------------

async function loadStats() {

    try {

        const response =
            await fetch("/api/stats");

        const data =
            await response.json();


        document.getElementById(
            "queryCount"
        ).innerText = data.queries;


        document.getElementById(
            "answerCount"
        ).innerText = data.answered;

        document.getElementById(
            "topicCount"
        ).innerText = data.topics;
    } catch (error) {
        console.error("Unable to load dashboard statistics:", error);
    }
}


loadStats();