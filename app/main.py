

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import redis

app = FastAPI()
r = redis.Redis(host="redis", port=6379, decode_responses=True)

from fastapi.responses import HTMLResponse

# @app.get("/", response_class=HTMLResponse)
# def form_page():
#     return """
#     <html>
#         <body>
#             <h1>Отправить событие xxx</h1>
#             <form action="/send_form" method="post">
#                 <input name="message" type="text"/>
#                 <input type="submit" value="Отправить"/>
#             </form>
#         </body>
#     </html>
#     """

@app.get("/", response_class=HTMLResponse)
def form_page():
    return """
    <html>
    <head>
        <title>Отправить событие</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: #121212;
                color: #e0e0e0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: #1e1e1e;
                padding: 30px 40px;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.6);
                text-align: center;
            }
            input[type="text"] {
                padding: 10px;
                width: 250px;
                border: 1px solid #333;
                border-radius: 6px;
                background: #2c2c2c;
                color: #e0e0e0;
                margin-bottom: 20px;
                font-size: 16px;
            }
            input[type="submit"], .nav-button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                cursor: pointer;
                margin: 10px;
                text-decoration: none;
                display: inline-block;
            }
            input[type="submit"]:hover, .nav-button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Отправить событие</h1>
            <form action="/send_form" method="post">
                <input name="message" type="text" placeholder="Введите сообщение"/><br/>
                <input type="submit" value="Отправить"/>
            </form>
            <a class="nav-button" href="/last">Последнее сообщение</a>
            <a class="nav-button" href="/metrics">Метрики</a>
            <a class="nav-button" href="/history">История сообщений</a>
            <a class="nav-button" href="http://localhost:3000/goto/ek7KFcfNg?orgId=1" target="_blank">Открыть Grafana</a>
        </div>
    </body>
    </html>
    """





from fastapi import Form

# @app.post("/send_form")
# def send_form_message(message: str = Form(...)):
#     r.set("last_message", message)
#     r.publish("events", message)
#     return {"status": "sent", "message": message}

# @app.post("/send_form", response_class=HTMLResponse)
# def send_form_message(message: str = Form(...)):
#     r.set("last_message", message)
#     r.publish("events", message)
#     return f"""
#     <html>
#         <body>
#             <h1>Сообщение отправлено!</h1>
#             <p>Вы отправили: <strong>{message}</strong></p>
#             <a href="/">← Назад</a>
#         </body>
#     </html>
#     """

@app.post("/send_form", response_class=HTMLResponse)
def send_form_message(message: str = Form(...)):
    r.set("last_message", message)
    r.lpush("messages", message)
    r.publish("events", message)
    return f"""
    <html>
    <head>
        <title>Сообщение отправлено</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: #121212;
                color: #e0e0e0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                background: #1e1e1e;
                padding: 30px 40px;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.6);
                text-align: center;
            }}
            a {{
                text-decoration: none;
                color: #4CAF50;
                font-weight: bold;
                display: inline-block;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Сообщение отправлено!</h1>
            <p>Вы отправили: <strong>{message}</strong></p>
            <a href="/">← Назад</a>
        </div>
    </body>
    </html>
    """

@app.get("/history", response_class=HTMLResponse)
def show_history():
    messages = r.lrange("messages", 0, 9)  # 10 последних
    message_list = "".join(f"<li>{m}</li>" for m in messages)
    return f"""
    <html>
    <head>
        <title>История сообщений</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: #121212;
                color: #e0e0e0;
                padding: 40px;
            }}
            ul {{
                list-style: none;
                padding: 0;
            }}
            li {{
                padding: 10px;
                background: #1e1e1e;
                margin-bottom: 8px;
                border-radius: 6px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }}
            a {{
                text-decoration: none;
                color: #4CAF50;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>Последние сообщения</h1>
        <ul>{message_list}</ul>
        <a href="/">← Назад</a>
    </body>
    </html>
    """


@app.post("/send/{message}")
def send_message(message: str):
    r.set("last_message", message)  # Кэшируем
    r.publish("events", message)   # Публикуем
    return {"status": "sent", "message": message}

@app.get("/last", response_class=HTMLResponse)
def get_last_message():
    message = r.get("last_message")
    return f"""
    <html>
    <head>
        <title>Последнее сообщение</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: #121212;
                color: #e0e0e0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                background: #1e1e1e;
                padding: 30px 40px;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.6);
                text-align: center;
            }}
            a {{
                text-decoration: none;
                color: #4CAF50;
                font-weight: bold;
                display: inline-block;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Последнее сообщение</h1>
            <p><strong>{message or "Нет сообщений"}</strong></p>
            <a href="/">← Назад</a>
        </div>
    </body>
    </html>
    """


from prometheus_client import Counter, generate_latest, REGISTRY
from fastapi.responses import Response

REQUEST_COUNT = Counter("request_count", "Total HTTP requests", ["method", "endpoint"])

@app.middleware("http")
async def count_requests(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(request.method, request.url.path).inc()
    return response

@app.get("/metrics", response_class=HTMLResponse)
def metrics():
    raw = generate_latest(REGISTRY).decode("utf-8")
    lines = raw.strip().split("\n")
    pretty = "<br>".join(line.replace(" ", "&nbsp;") for line in lines)

    return f"""
    <html>
    <head>
        <title>Метрики</title>
        <style>
            body {{
                font-family: monospace;
                background: #121212;
                color: #e0e0e0;
                padding: 40px;
            }}
            a {{
                text-decoration: none;
                color: #4CAF50;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>Метрики приложения</h1>
        <pre>{pretty}</pre>
        <a href="/">← Назад</a>
    </body>
    </html>
    """

