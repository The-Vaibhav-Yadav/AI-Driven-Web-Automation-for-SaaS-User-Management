import aiohttp

class OllamaChat:
    def __init__(self, model="gemma:2b", host="http://localhost:11434"):
        self.model = model
        self.model_name = model
        self.provider = "ollama"
        self.url = f"{host}/api/generate"

    async def ainvoke(self, messages, *args, **kwargs):
        def extract_content(msg):
            # Handles dicts and LangChain-style objects
            if isinstance(msg, dict):
                return f"{msg['role']}: {msg['content']}"
            elif hasattr(msg, 'type') and hasattr(msg, 'content'):
                return f"{msg.type}: {msg.content}"
            else:
                raise ValueError(f"Unsupported message format: {msg}")

        prompt = "\n".join([extract_content(m) for m in messages]) + "\nassistant:"

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"Error from Ollama API: {await resp.text()}")
                data = await resp.json()
                return {"role": "assistant", "content": data["response"]}

