from agent1 import Agent1

agent = Agent1(
    provider= "openai",
    api_key= "your_api_key",
    model="gpt-4o-mini"
)

messages=[
    {"role":"user", "content":"Namaste"}
]

response=agent.request_and_response(messages)

print(response)
