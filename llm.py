import os

from dotenv import load_dotenv
from groq import Groq
from retrivel import retrieve_documents

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY missing. Check your .env file.")

client = Groq(api_key=api_key)


def stream_chatbot(question, history=None):
    documents = retrieve_documents(question)

    if documents:
        context = "\n\n".join(
            f"Title: {doc.get('title', 'Untitled')}\n"
            f"Content: {doc.get('content', '')}"
            for doc in documents
        )
    else:
        context = "No relevant information was found in the database."

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI chatbot. Answer clearly using "
                "the database context when relevant. If the answer is "
                "not available, say so instead of inventing facts.\n\n"
                f"Database context:\n{context}"
            )
        }
    ]

    if history:
        for item in history[-6:]:
            if item.get("role") in ("user", "assistant"):
                messages.append({
                    "role": item["role"],
                    "content": str(item.get("content", ""))
                })

    messages.append({
        "role": "user",
        "content": question
    })

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None
    )

    for chunk in completion:
        content = chunk.choices[0].delta.content or ""
        if content:
            yield content