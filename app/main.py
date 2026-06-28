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
        <title>Asistente BimBam Buy</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: Arial, sans-serif; background: #f5f5f5; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
            .container { width: 100%; max-width: 700px; height: 90vh; background: white; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); display: flex; flex-direction: column; overflow: hidden; }
            .header { background: #e91e63; color: white; padding: 16px 20px; }
            .header h1 { font-size: 20px; }
            .header p { font-size: 13px; opacity: 0.85; margin-top: 4px; }
            #chat { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 12px; }
            .msg { display: flex; flex-direction: column; max-width: 80%; }
            .msg.user { align-self: flex-end; align-items: flex-end; }
            .msg.bot { align-self: flex-start; align-items: flex-start; }
            .bubble { padding: 10px 14px; border-radius: 18px; font-size: 14px; line-height: 1.5; }
            .msg.user .bubble { background: #e91e63; color: white; border-radius: 18px 18px 4px 18px; }
            .msg.bot .bubble { background: #f0f0f0; color: #333; border-radius: 18px 18px 18px 4px; }
            .msg.bot .bubble.thinking { color: #999; font-style: italic; }
            .input-area { padding: 16px; border-top: 1px solid #eee; display: flex; gap: 8px; }
            #question { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 24px; font-size: 14px; outline: none; }
            #question:focus { border-color: #e91e63; }
            button { background: #e91e63; color: white; border: none; padding: 12px 20px; border-radius: 24px; cursor: pointer; font-size: 14px; white-space: nowrap; }
            button:disabled { background: #ccc; cursor: not-allowed; }
            button:hover:not(:disabled) { background: #c2185b; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛍️ Asistente BimBam Buy</h1>
                <p>Pregúntame sobre envíos, pagos, garantías, reembolsos o afiliados.</p>
            </div>
            <div id="chat"></div>
            <div class="input-area">
                <input id="question" type="text" placeholder="Escribe tu pregunta..." onkeydown="if(event.key==='Enter' && !event.shiftKey) preguntar()"/>
                <button id="btn" onclick="preguntar()">Enviar</button>
            </div>
        </div>
        <script>
            async function preguntar() {
                const input = document.getElementById('question');
                const chat = document.getElementById('chat');
                const btn = document.getElementById('btn');
                const q = input.value.trim();
                if (!q) return;

                // Mensaje usuario
                const userMsg = document.createElement('div');
                userMsg.className = 'msg user';
                userMsg.innerHTML = `<div class="bubble">${q}</div>`;
                chat.appendChild(userMsg);

                // Mensaje pensando
                const botMsg = document.createElement('div');
                botMsg.className = 'msg bot';
                botMsg.innerHTML = `<div class="bubble thinking">⏳ Pensando...</div>`;
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
                    botMsg.innerHTML = `<div class="bubble">${data.answer}</div>`;
                } catch(e) {
                    botMsg.innerHTML = `<div class="bubble">❌ Error al conectar con el servidor.</div>`;
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
