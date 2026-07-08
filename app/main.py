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
    <title>BimBam Buy</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background: #1c1c1e;
            color: #f5f5f7;
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', sans-serif;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            -webkit-font-smoothing: antialiased;
        }

        .wrapper {
            width: 100%;
            max-width: 680px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 48px 24px 24px;
        }

        .header {
            text-align: center;
            margin-bottom: 48px;
        }

        .logo {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #2c2c2e, #3a3a3c);
            border-radius: 14px;
            margin: 0 auto 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            border: 1px solid #3a3a3c;
        }

        .header h1 {
            font-size: 22px;
            font-weight: 600;
            color: #f5f5f7;
            letter-spacing: -0.3px;
        }

        .header p {
            font-size: 13px;
            color: #6e6e73;
            margin-top: 6px;
            font-weight: 400;
        }

        #chat {
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
            scrollbar-width: none;
        }

        #chat::-webkit-scrollbar { display: none; }

        .msg { display: flex; flex-direction: column; max-width: 80%; }
        .msg.user { align-self: flex-end; align-items: flex-end; }
        .msg.bot { align-self: flex-start; align-items: flex-start; }

        .bubble {
            padding: 12px 16px;
            font-size: 15px;
            line-height: 1.5;
            font-weight: 400;
        }

        .msg.user .bubble {
            background: #0a84ff;
            color: #ffffff;
            border-radius: 20px 20px 6px 20px;
        }

        .msg.bot .bubble {
            background: #2c2c2e;
            color: #e5e5ea;
            border-radius: 20px 20px 20px 6px;
            border: 1px solid #3a3a3c;
        }

        .msg.bot .bubble.thinking {
            color: #48484a;
            font-style: normal;
        }

        .empty-state {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 32px;
        }

        .empty-state p {
            font-size: 15px;
            color: #48484a;
            font-weight: 400;
        }

        .suggestions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            width: 100%;
        }

        .suggestion {
            background: #2c2c2e;
            border: 1px solid #3a3a3c;
            border-radius: 14px;
            padding: 14px 16px;
            font-size: 13px;
            color: #98989d;
            cursor: pointer;
            text-align: left;
            font-family: inherit;
            font-weight: 400;
            line-height: 1.4;
            transition: all 0.2s ease;
        }

        .suggestion:hover {
            background: #3a3a3c;
            color: #f5f5f7;
            border-color: #48484a;
        }

        .input-area {
            margin-top: 24px;
            display: flex;
            align-items: center;
            gap: 10px;
            background: #2c2c2e;
            border: 1px solid #3a3a3c;
            border-radius: 20px;
            padding: 10px 10px 10px 18px;
            transition: border-color 0.2s;
        }

        .input-area:focus-within {
            border-color: #48484a;
        }

        #question {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: #f5f5f7;
            font-size: 15px;
            font-family: inherit;
            font-weight: 400;
        }

        #question::placeholder { color: #48484a; }

        button#btn {
            background: #0a84ff;
            border: none;
            color: #fff;
            width: 34px;
            height: 34px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            flex-shrink: 0;
        }

        button#btn:hover:not(:disabled) {
            background: #409cff;
            transform: scale(1.05);
        }

        button#btn:disabled {
            background: #3a3a3c;
            cursor: not-allowed;
            transform: none;
        }

        button#btn svg { width: 15px; height: 15px; }
    </style>
</head>
<body>
<div class="wrapper">
    <div class="header">
        <div class="logo">🛍️</div>
        <h1>BimBam Buy</h1>
        <p>Asistente de documentación interna</p>
    </div>

    <div id="chat">
        <div class="empty-state" id="empty">
            <p>¿En qué puedo ayudarte hoy?</p>
            <div class="suggestions">
                <button class="suggestion" onclick="sendSuggestion(this)">¿Cuál es la política de reembolsos?</button>
                <button class="suggestion" onclick="sendSuggestion(this)">¿Cuáles son los tiempos de envío?</button>
                <button class="suggestion" onclick="sendSuggestion(this)">¿Cómo funciona el programa de afiliados?</button>
                <button class="suggestion" onclick="sendSuggestion(this)">¿Qué métodos de pago aceptan?</button>
            </div>
        </div>
    </div>

    <div class="input-area">
        <input id="question" type="text" placeholder="Mensaje" onkeydown="if(event.key==='Enter') preguntar()"/>
        <button id="btn" onclick="preguntar()">
            <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
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
        userMsg.innerHTML = `<div class="bubble">${q}</div>`;
        chat.appendChild(userMsg);

        const botMsg = document.createElement('div');
        botMsg.className = 'msg bot';
        botMsg.innerHTML = `<div class="bubble thinking">●  ●  ●</div>`;
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
            botMsg.querySelector('.bubble').textContent = 'Error al conectar.';
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
