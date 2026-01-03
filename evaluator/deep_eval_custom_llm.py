import json
from pydantic import BaseModel
from openai import OpenAI
from deepeval.models.base_model import DeepEvalBaseLLM


class OpenAIModelCustom(DeepEvalBaseLLM):
    def __init__(self, model_name: str, api_key: str, base_url: str):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.model_name = model_name

    def load_model(self):
        return self.client

    # --------- JSON confinement style (como na doc) ---------
    def generate(self, prompt: str, schema: BaseModel) -> BaseModel:
        """
        DeepEval vai passar um `schema` (Pydantic BaseModel) aqui.
        A ideia é:
        1) chamar o LLM pedindo JSON
        2) fazer json.loads
        3) retornar schema(**json_dict)
        """
        client = self.load_model()

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            # se o backend suportar, você pode tentar forçar JSON:
            # response_format={"type": "json_object"},
            temperature=0,
        )

        text = response.choices[0].message.content

        # DeepEval espera que isso seja JSON válido
        data = json.loads(text)

        # Cria e retorna a instância do schema fornecido pelo DeepEval
        return schema(**data)

    async def a_generate(self, prompt: str, schema: BaseModel) -> BaseModel:
        """
        Versão assíncrona – aqui reaproveitamos o generate síncrono.
        (fica "fake async", mas é exatamente o que a doc sugere
        quando não há client assíncrono disponível.)
        """
        return self.generate(prompt, schema)

    def get_model_name(self):
        return f"OpenAI-{self.model_name}"