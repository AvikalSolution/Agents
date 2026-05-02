from agent1 import Agent1

agent=Agent1(
        provider="ollama",
        model="gemma3:270m",
    )

messages=[
    {
    "role":"user", 
     "content":"Hey"
    }
]

response=agent._request_and_response_ollama(messages)

print(response)
