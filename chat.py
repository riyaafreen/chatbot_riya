from groq import Groq

client = Groq(api_key="YOUR_API_KEY")

messages = [
    {
        "role": "system",
        "content": "you are a funny bestfriend who always speak freely and cracks jokes, you are also a good listener and always give good advice"
    }
]

while True:
    user_input = input("You: ")
    if user_input.lower() == "bye":
       print("AI: Bye bestie!")
       break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.1-8b-instant",
        temperature=0.9,
        max_tokens=50
    )

    response = chat_completion.choices[0].message.content

    print("AI:", response)

    messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )