from llm import chatbot


def main():
    print("===== GROQ RAG CHATBOT =====")
    print("Type 'exit' to stop.")

    history = []

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in ("exit", "quit"):
            print("Chatbot: Goodbye!")
            break

        if not question:
            continue

        print("\nChatbot: ", end="", flush=True)

        answer = chatbot(question, history)

        history.append({
            "role": "user",
            "content": question
        })

        history.append({
            "role": "assistant",
            "content": answer
        })

        history = history[-6:]


if __name__ == "__main__":
    main()