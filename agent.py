import os
from groq import Groq

client = Groq(
    api_key="API_KEY",
)
# ... rest of your code


# Example usage:
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the polymorphic behavior of objects in object-oriented programming.",
        }
    ],
    model="moonshotai/kimi-k2-instruct-0905", # Example model
) 


print(chat_completion.choices[0].message.content)
