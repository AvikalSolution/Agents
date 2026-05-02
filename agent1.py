import requests
from typing import List, Dict,Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI=None

class Agent1:
    #######################Constructor#################
    def __init__(
        self,
        provider: str = "openai", # "openai" or "ollama"
        model: str = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.7
    ):

        self.provider= provider.lower()
        self.temperature= temperature

        if self.provider=="openai":
            if OpenAI is None:
                raise ImportError("Install openai: pip install openai or uv add openai")
            
            self.model= model or "gpt-4o-mini"
            self.client= OpenAI(api_key=api_key)
        
        elif self.provider=="ollama":
            self.model=model or "llama3"
            self.base_url= base_url or "http://localhost:11434"

        else:
            raise ValueError("Unsupported provider: choose 'openai' or 'ollama'")
        
    ########### Request and Response to llm model ####################
    def request_and_response(self,messages:list[Dict]) -> str:
        
        if self.provider=="openai":
            return self._request_and_response_openai(messages)
        elif self.provider=="ollama":
            return self._request_and_response_ollama(messages)
        
    ########## Request and Response to openai #################
    def  _request_and_response_openai(self,messages:list[dict]) ->str:
        _response= self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )
        
        return _response.choice[0].message.content.strip()

    ########## Request and Response to ollma #################
    def _request_and_response_ollama(self,messages:List[Dict]) -> str:
        response= requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model":self.model,
                "messages":messages,
                # "stream": False,    # to supress default behavior i.e Ollama’s /api/chat endpoint often returns NDJSON (newline-delimited JSON) like:
                #                     #{"message": {"content": "Hel"}}
                #                     #{"message": {"content": "lo"}}
                #                     #{"done": true}
                "options":{
                    "temperature":self.temperature
                }
            },
            stream=True  # enable streaming
        )

        if response.status_code !=200:
            raise Exception(f"ollama Error: {response.text}")
        
        # Print raw test
        print(response.text)
        
        # ---------if streaming is false----------------
        # return response.json()["message"]["content"].strip() 

        # ---------if streaming is true----------------
        import json
        full_text = ""
        
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode("utf-8"))

                if "message" in chunk:
                    full_text += chunk["message"]["content"]

                if chunk.get("done"):
                    break

        return full_text.strip()
        

    