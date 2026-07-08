from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from app.agent import cargar_agente
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Agente BimBam Buy", version="1.0.0")
agente = cargar_agente()

class Pregunta(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok", "agente": "BimBam Buy RAG"}

@app.post("/ask")
def preguntar(body: Pregunta):
    respuesta = agente.invoke({"query": body.question})
    return {"question": body.question, "answer": respuesta["result"]}

@app.get("/", response_class=HTMLResponse)
def chat_ui():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BimBam Buy — Asistente</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background: #0a0a0a;
            color: #e0e0e0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .wrapper {
            width: 100%;
            max-width: 640px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 24px 16px 16px;
        }

        .header {
            text-align: center;
            margin-bottom: 32px;
        }

        .header h1 {
            font-size: 18px;
            font-weight: 500;
            color: #ffffff;
            letter-spacing: 0.5px;
        }

        .header p {
            font-size: 12px;
            color: #555;
            margin-top: 6px;
            letter-spacing: 0.3px;
        }

        .dot {
            display: inline-block;
            width: 6px;
            height: 6px;
            background: #22c55e;
            border-radius: 50%;
            margin-right: 6px;
            vertical-align: middle;
        }

        #chat {
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
            padding-right: 4px;
            scrollbar-width: thin;
            scrollbar-color: #222 transparent;
        }

        #chat::-webkit-scrollbar { width: 4px; }
        #chat::-webkit-scrollbar-thumb { background: #222; border-radius: 4px; }

        .msg { display: flex; flex-direction: column; max-width: 85%; }
        .msg.user { align-self: flex-end; align-items: flex-end; }
        .msg.bot { align-self: flex-start; align-items: flex-start; }

        .bubble {
            padding: 10px 14px;
            border-radius: 16px;
            font-size: 14px;
            line-height: 1.6;
        }

        .msg.user .bubble {
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            color: #ffffff;
            border-radius: 16px 16px 4px 16px;
        }

        .msg.bot .bubble {
            background: #111;
            border: 1px solid #1e1e1e;
            color: #d0d0d0;
            border-radius: 16px 16px 16px 4px;
        }

        .msg.bot .bubble.thinking {
            color: #444;
            font-style: italic;
            font-size: 13px;
        }

        .label {
            font-size: 10px;
            color: #333;
            margin-bottom: 4px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        .input-area {
            margin-top: 20px;
            display: flex;
            gap: 8px;
            align-items: center;
            background: #111;
            border: 1px solid #1e1e1e;
            border-radius: 16px;
            padding: 10px 10px 10px 16px;
        }

        #question {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: #e0e0e0;
            font-size: 14px;
            font-family: inherit;
        }

        #question::placeholder { color: #333; }

        button {
            background: #1a1a1a;
            border: 1px solid #2a2a2a;
            color: #888;
            width: 34px;
            height: 34px;
            border-radius: 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.15s;
            flex-shrink: 0;
        }

        button:hover:not(:disabled) {
            background: #222;
            color: #fff;
            border-color: #333;
        }

        button:disabled { opacity: 0.3; cursor: not-allowed; }

        button svg { width: 16px; height: 16px; }

        .empty-state {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 24px;
            color: #2a2a2a;
        }

        .empty-state p { font-size: 13px; color: #333; }

        .suggestions {
            display: flex;
            flex-direction: column;
            gap: 8px;
            width: 100%;
        }

        .suggestion {
            background: #0f0f0f;
            border: 1px solid #1a1a1a;
            border-radius: 10px;
            padding: 10px 14px;
            font-size: 13px;
            color: #444;
            cursor: pointer;
            text-align: left;
            transition: all 0.15s;
            font-family: inherit;
        }

        .suggestion:hover {
            border-color: #2a2a2a;
            color: #888;
            background: #111;
        }
    </style>
</head>
<body>
<div class="wrapper">
    <div class="header">
        <h1><span class="dot"></span>BimBam Buy</h1>
        <p>Asistente de documentación interna</p>
    </div>

    <div id="chat">
        <div class="empty-state" id="empty">
            <p>¿En qué puedo ayudarte?</p>
            <div class="suggestions">
                <button class="suggestion" onclick="sendSuggestion(this)">¿Cuál es la política de reembolsos?</button>
                <button class="suggestion" onclick="sendSuggestion(this)">¿Cuáles son los tiempos de envío?</button>
                <button class="suggestion" onclick="sendSuggestion(this)">¿Cómo funciona el programa de afiliados?</button>
                <button class="suggestion" onclick="sendSuggestion(this)">¿Qué métodos de pago aceptan?</button>
            </div>
        </div>
    </div>

    <div class="input-area">
        <input id="question" type="text" placeholder="Escribe tu pregunta..." onkeydown="if(event.key==='Enter') preguntar()"/>
        <button id="btn" onclick="preguntar()">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
        </button>
    </div>
</div>

<script>
    function sendSuggestion(el) {
        document.getElementById('question').value = el.textContent;
        preguntar();
    }

    async function preguntar() {
        const input = document.getElementById('question');
        const chat = document.getElementById('chat');
        const btn = document.getElementById('btn');
        const empty = document.getElementById('empty');
        const q = input.value.trim();
        if (!q) return;

        if (empty) empty.remove();

        const userMsg = document.createElement('div');
        userMsg.className = 'msg user';
        userMsg.innerHTML = `<div class="label">Tú</div><div class="bubble">${q}</div>`;
        chat.appendChild(userMsg);

        const botMsg = document.createElement('div');
        botMsg.className = 'msg bot';
        botMsg.innerHTML = `<div class="label">Asistente</div><div class="bubble thinking">pensando...</div>`;
        chat.appendChild(botMsg);

        input.value = '';
        btn.disabled = true;
        chat.scrollTop = chat.scrollHeight;

        try {
            const res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: q})
            });
            const data = await res.json();
            botMsg.querySelector('.bubble').className = 'bubble';
            botMsg.querySelector('.bubble').textContent = data.answer;
        } catch(e) {
            botMsg.querySelector('.bubble').className = 'bubble';
            botMsg.querySelector('.bubble').textContent = 'Error al conectar con el servidor.';
        } finally {
            btn.disabled = false;
            chat.scrollTop = chat.scrollHeight;
            input.focus();
        }
    }
</script>
</body>
</html>
    """
