from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="CRAN AI")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CRAN AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f5f7fa;
            color: #172033;
        }

        .header {
            height: 64px;
            background: #ffffff;
            border-bottom: 1px solid #e2e6ec;
            display: flex;
            align-items: center;
            padding: 0 28px;
            font-size: 20px;
            font-weight: bold;
        }

        .header span {
            color: #1769aa;
            margin-left: 8px;
        }

        .layout {
            display: flex;
            height: calc(100vh - 64px);
        }

        .sidebar {
            width: 240px;
            background: #111827;
            color: white;
            padding: 20px;
        }

        .new-chat {
            width: 100%;
            padding: 12px;
            border: 1px solid #374151;
            border-radius: 8px;
            background: #1f2937;
            color: white;
            cursor: pointer;
        }

        .main {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 40px 15%;
        }

        .welcome {
            text-align: center;
            margin-top: 15vh;
        }

        .welcome h1 {
            font-size: 32px;
        }

        .welcome p {
            color: #667085;
        }

        .input-area {
            padding: 20px 15%;
            background: #ffffff;
            border-top: 1px solid #e2e6ec;
        }

        .input-box {
            display: flex;
            gap: 10px;
        }

        textarea {
            flex: 1;
            resize: none;
            border: 1px solid #ccd3dd;
            border-radius: 12px;
            padding: 14px;
            font-size: 15px;
            min-height: 52px;
        }

        button.send {
            background: #1769aa;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0 22px;
            cursor: pointer;
        }

        .user {
            background: #e8f1f8;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 15px;
        }

        .assistant {
            background: white;
            padding: 18px;
            border-radius: 12px;
            margin-bottom: 15px;
            border: 1px solid #e5e7eb;
        }

        @media (max-width: 700px) {
            .sidebar {
                display: none;
            }

            .messages,
            .input-area {
                padding-left: 15px;
                padding-right: 15px;
            }
        }
    </style>
</head>

<body>

<div class="header">
    🇳🇦 CRAN <span>AI</span>
</div>

<div class="layout">

    <aside class="sidebar">
        <button class="new-chat" onclick="newChat()">
            + New Chat
        </button>

        <p style="margin-top:30px;color:#9ca3af;">
            Regulatory Intelligence Assistant
        </p>
    </aside>

    <main class="main">

        <div class="messages" id="messages">

            <div class="welcome" id="welcome">
                <h1>How can CRAN AI help?</h1>
                <p>
                    Ask questions about telecommunications,
                    broadcasting, spectrum, licensing and regulation.
                </p>
            </div>

        </div>

        <div class="input-area">
            <div class="input-box">
                <textarea
                    id="question"
                    placeholder="Ask a question about CRAN..."
                    onkeydown="handleKey(event)"
                ></textarea>

                <button class="send" onclick="sendMessage()">
                    Send
                </button>
            </div>

            <p style="font-size:12px;color:#8a94a6;text-align:center;">
                CRAN AI Prototype — Not an official CRAN service
            </p>
        </div>

    </main>

</div>

<script>

function handleKey(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function sendMessage() {

    const box = document.getElementById("question");
    const text = box.value.trim();

    if (!text) return;

    const messages = document.getElementById("messages");
    const welcome = document.getElementById("welcome");

    if (welcome) {
        welcome.remove();
    }

    const userMessage = document.createElement("div");
    userMessage.className = "user";
    userMessage.innerText = text;

    messages.appendChild(userMessage);

    box.value = "";

    const assistantMessage = document.createElement("div");
    assistantMessage.className = "assistant";

    assistantMessage.innerHTML =
        "<strong>CRAN AI</strong><br><br>" +
        "Thank you. The AI knowledge system is being connected. " +
        "In the completed prototype, I will search the CRAN knowledge base " +
        "and provide an answer with the relevant source documents.";

    messages.appendChild(assistantMessage);

    messages.scrollTop = messages.scrollHeight;
}

function newChat() {
    location.reload();
}

</script>

</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML
