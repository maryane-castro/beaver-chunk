import openai


class LLM:
    def __init__(self, base_url="https://api.groq.com/openai/v1", api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.client = openai.OpenAI(base_url=base_url, api_key=api_key)

    def get_client(self):
        return self.client

    def generate_response(self, user_input, docs_retriever, model="openai/gpt-oss-20b"):

        response = self.client.responses.create(
            instructions="Baseado nas informações fornecidas, seu objetivo é responder o usuário de forma correta",
            input=f"""
            Informações:
            {docs_retriever}

            Pergunta do usuário:
            {user_input}
            """,
            model=model,
        )

        return response.output_text
