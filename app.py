from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import re

app = FastAPI(title="CRAN AI")


# ---------------------------------------------------------
# CRAN KNOWLEDGE BASE
# Based on publicly available information from CRAN's
# official website: https://www.cran.na/
# ---------------------------------------------------------

KNOWLEDGE = [
    {
        "keywords": ["what is cran", "who is cran", "about cran", "cran"],
        "answer": """CRAN stands for the Communications Regulatory Authority of Namibia.

CRAN is Namibia's independent communications regulator. It regulates telecommunications services and networks, broadcasting services, postal services, and the use and allocation of radio spectrum.

CRAN was established under section 4 of the Communications Act, No. 8 of 2009, and was established on 18 May 2011.

Its mandate includes regulating, supervising and promoting communications services in Namibia.""",
        "sources": [
            ("CRAN — About Us", "https://www.cran.na/about-us/")
        ]
    },

    {
        "keywords": ["mandate", "responsible for", "regulate", "regulation"],
        "answer": """CRAN's regulatory mandate covers several major areas of Namibia's communications sector.

These include:

• Telecommunications services and networks
• Broadcasting services
• Postal services
• Radio frequency spectrum
• Licensing and related regulatory procedures
• Consumer protection and complaints

CRAN's stated core purpose is to regulate the ICT industry while supporting socio-economic development in Namibia.""",
        "sources": [
            ("CRAN — About Us", "https://www.cran.na/about-us/"),
            ("CRAN — Home", "https://www.cran.na/")
        ]
    },

    {
        "keywords": ["licence", "license", "licensing", "apply", "application"],
        "answer": """CRAN handles licensing for telecommunications and broadcasting services in Namibia.

According to CRAN's published licensing procedure, applications are assessed after the required application fee is paid. The application may then be published in the Government Gazette for public comment for 14 days. CRAN considers the application, supporting documentation and public comments before making a decision.

CRAN also publishes application forms for telecommunications service licences, broadcasting service licences and spectrum-use licences.""",
        "sources": [
            ("CRAN — Licensing", "https://www.cran.na/licensing/"),
            ("CRAN — Licensing Forms", "https://www.cran.na/licensing-forms/")
        ]
    },

    {
        "keywords": ["spectrum", "radio frequency", "frequency", "radio"],
        "answer": """CRAN is responsible for the use and allocation of radio frequency spectrum in Namibia.

A spectrum licence may be required in addition to a telecommunications or broadcasting service licence when the service or network uses radio waves.

CRAN publishes spectrum-related notices, frequency plans, licence information and other spectrum regulatory documents on its website.""",
        "sources": [
            ("CRAN — Licensing", "https://www.cran.na/licensing/"),
            ("CRAN — Spectrum Notices", "https://www.cran.na/spectrum-notices/")
        ]
    },

    {
        "keywords": ["consumer", "complaint", "complaints", "customer"],
        "answer": """CRAN provides consumer-related services and complaints information.

CRAN states that its regulatory role includes ensuring that consumers receive the benefits of competitive electronic communication services and are protected from exploitation or abuse.

The CRAN website provides consumer complaints information and a consumer form for submitting complaints.""",
        "sources": [
            ("CRAN — Home", "https://www.cran.na/"),
            ("CRAN — About Us", "https://www.cran.na/about-us/")
        ]
    },

    {
        "keywords": ["regulations", "regulatory documents", "rules", "law"],
        "answer": """CRAN publishes regulatory documents and final regulations covering areas of the communications sector.

Its published regulations include material concerning:

• Telecommunications licensing
• Spectrum licensing
• Numbering
• Quality of service
• Telecommunications equipment type approval
• Broadcasting
• Frequency channel plans
• Universal service
• Infrastructure sharing and other regulatory matters

The CRAN website provides a searchable collection of final regulations and related documents.""",
        "sources": [
            ("CRAN — Final Regulations", "https://www.cran.na/final-regulations/")
        ]
    },

    {
        "keywords": ["quality", "quality of service", "qos"],
        "answer": """CRAN publishes Quality of Service standards applicable to telecommunications licensees.

The CRAN final regulations section lists regulations prescribing Quality of Service Standards applicable to telecommunications licensees, including the 2025 regulation published as GN 162 of 2025, GG 8611.""",
        "sources": [
            ("CRAN — Final Regulations", "https://www.cran.na/final-regulations/")
        ]
    },

    {
        "keywords": ["postal", "post", "mail"],
        "answer": """Postal services fall within CRAN's regulatory mandate.

CRAN's official description of its mandate states that it regulates telecommunications services and networks, broadcasting services, postal services and the use and allocation of radio spectrum in Namibia.""",
        "sources": [
            ("CRAN — About Us", "https://www.cran.na/about-us/")
        ]
    },

    {
        "keywords": ["cyber", "cybersecurity", "security", "nam-csirt"],
        "answer": """CRAN's organisation includes the Namibia Cyber Security Incident Response Team, known as NAM-CSIRT.

CRAN provides cybersecurity-related information and updates through its website and identifies NAM-CSIRT as part of its organisational structure.""",
        "sources": [
            ("CRAN — Departments", "https://www.cran.na/about-us/departments/"),
            ("CRAN — Home", "https://www.cran.na/")
        ]
    },

    {
        "keywords": ["contact", "address", "phone", "email", "where is cran"],
        "answer": """CRAN's main reception is at Freedom Plaza, Courtside Building, 3rd Floor, at the corner of Fidel Castro Street and Rev. Michael Scott Street in Windhoek, Namibia.

Telephone: +264 61 222 666
Email: communications@cran.na

CRAN lists office hours as Monday to Friday, 08:00–13:00 and 14:00–17:00.""",
        "sources": [
            ("CRAN — Contact Us", "https://www.cran.na/contacts/")
        ]
    },

    {
        "keywords": ["strategic plan", "strategy", "2026", "2030"],
        "answer": """CRAN publishes strategic planning documents on its website.

Its current published strategic-plan section includes the CRAN (USF and NAM-CSIRT) Integrated Strategic Business Plan 2026–2030 as well as the CRAN Integrated Strategic Business Plan 2023–2026.""",
        "sources": [
            ("CRAN — Strategic Plans", "https://www.cran.na/strategic-plans/")
        ]
    },

    {
        "keywords": ["broadcasting", "broadcast", "radio station", "television", "tv"],
        "answer": """Broadcasting is one of the sectors regulated by CRAN.

CRAN publishes broadcasting licensing information, broadcasting-related regulatory documents and broadcasting frequency information.

The regulator's licensing resources include a Broadcasting Service Licence application form.""",
        "sources": [
            ("CRAN — About Us", "https://www.cran.na/about-us/"),
            ("CRAN — Licensing Forms", "https://www.cran.na/licensing-forms/")
        ]
    },

    {
        "keywords": ["type approval", "equipment", "device", "approved equipment"],
        "answer": """CRAN publishes regulations concerning telecommunications equipment requiring type approval.

The CRAN final regulations section lists regulations concerning telecommunications equipment requiring type approval, including regulations published in 2023 and related amendments.""",
        "sources": [
            ("CRAN — Final Regulations", "https://www.cran.na/final-regulations/")
        ]
    },
]


def find_answer(question: str):
    question_lower = question.lower()

    best_match = None
    best_score = 0

    for item in KNOWLEDGE:
        score = 0

        for keyword in item["keywords"]:
            if keyword in question_lower:
                # Longer phrases get more weight.
                score += len(keyword.split())

        if score > best_score:
            best_score = score
            best_match = item

    if best_match and best_score > 0:
        return best_match

    return {
        "answer": """I couldn't find a sufficiently specific answer in the current CRAN knowledge base.

For a production version of CRAN AI, the system would search CRAN's complete collection of regulatory documents, licences, notices, policies and publications before answering.

For now, try asking about CRAN's mandate, licensing, spectrum, broadcasting, consumer complaints, regulations, quality of service, cybersecurity or strategic plans.""",
        "sources": [
            ("CRAN official website", "https://www.cran.na/")
        ]
    }


class Question(BaseModel):
    question: str


# ---------------------------------------------------------
# API
# ---------------------------------------------------------

@app.post("/ask")
def ask(question: Question):
    result = find_answer(question.question)

    return {
        "answer": result["answer"],
        "sources": [
            {
                "title": title,
                "url": url
            }
            for title, url in result["sources"]
        ]
    }


# ---------------------------------------------------------
# WEB INTERFACE
# ---------------------------------------------------------

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

        button.send:disabled {
            background: #8aaac2;
            cursor: wait;
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
            line-height: 1.6;
        }

        .sources {
            margin-top: 18px;
            padding-top: 12px;
            border-top: 1px solid #e5e7eb;
            font-size: 13px;
        }

        .sources a {
            color: #1769aa;
            text-decoration: none;
        }

        .sources a:hover {
            text-decoration: underline;
        }

        .thinking {
            color: #667085;
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

            .input-box {
                flex-direction: column;
            }

            button.send {
                height: 48px;
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

        <p style="margin-top:25px;color:#6b7280;font-size:12px;line-height:1.5;">
            Prototype using publicly available CRAN information.
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

                <button class="send" id="sendButton" onclick="sendMessage()">
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


async function sendMessage() {

    const box = document.getElementById("question");
    const text = box.value.trim();

    if (!text) return;

    const messages = document.getElementById("messages");
    const welcome = document.getElementById("welcome");
    const button = document.getElementById("sendButton");

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
        "<span class='thinking'>Searching the CRAN knowledge base...</span>";

    messages.appendChild(assistantMessage);

    button.disabled = true;

    messages.scrollTop = messages.scrollHeight;

    try {

        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: text
            })
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        let html =
            "<strong>CRAN AI</strong><br><br>" +
            escapeHtml(data.answer).replace(/\\n/g, "<br>");

        if (data.sources && data.sources.length > 0) {

            html += "<div class='sources'>" +
                    "<strong>Sources</strong><br>";

            data.sources.forEach(function(source) {

                html +=
                    "• <a href='" +
                    source.url +
                    "' target='_blank'>" +
                    escapeHtml(source.title) +
                    "</a><br>";

            });

            html += "</div>";
        }

        assistantMessage.innerHTML = html;

    } catch (error) {

        assistantMessage.innerHTML =
            "<strong>CRAN AI</strong><br><br>" +
            "Sorry, I couldn't process the question. " +
            "Please try again.";

    }

    button.disabled = false;

    messages.scrollTop = messages.scrollHeight;
}


function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
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
