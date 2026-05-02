This is Readme file

#Ollama
-------------------------------------------------
Quick sanity test (before using your agent)

Run this minimal check:

curl http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "messages": [{"role": "user", "content": "hello"}]
}'

If this fails → problem is Ollama setup, not your Python code.

Use smaller models if you're on CPU:
ollama pull llama3:8b