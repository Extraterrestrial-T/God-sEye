import ollama
from ai.prompt_templates import SINGLE_IMAGE, MULTI_IMAGE

class GemmaRunner:
    def __init__(self, model_name='gemma:3n'):
        self.model = model_name
        self.history = []

    def describe_images(self, paths: list[str]) -> str:
        # build multipart message
        content = [{"type":"text","text": MULTI_IMAGE}]
        for p in paths:
            with open(p,'rb') as f: content.append({"type":"image","image":f.read()})
        self.history.append({"role":"user","content": content})
        resp = ollama.chat(model=self.model, messages=self.history)
        ans = resp.get('message',{}).get('content','')
        self.history.append({"role":"assistant","content": ans})
        return ans