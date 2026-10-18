from flask import Flask, render_template, request, Response, stream_with_context
from llm import stream_chatbot

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}

    question = data.get("message", "").strip()
    history = data.get("history", [])

    if not question:
        return {"error": "Please enter a message."}, 400

    if not isinstance(history, list):
        return {"error": "Invalid chat history."}, 400

    def generate():
        try:
            yield from stream_chatbot(question, history)
        except Exception:
            app.logger.exception("Chat generation failed")
            yield "\n\n[Error: Could not generate a response. Check the server terminal.]"

    return Response(
        stream_with_context(generate()),
        mimetype="text/plain; charset=utf-8",
        headers={"Cache-Control": "no-cache"}
    )


if __name__ == "__main__":
    print("Starting chatbot server...")
    app.run(host="127.0.0.1", port=5000, debug=True)