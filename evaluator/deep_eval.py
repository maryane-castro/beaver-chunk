import os

# from deepeval import assert_test, set_local_model
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams


from evaluator.deep_eval_custom_llm import OpenAIModelCustom

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

global_custom_llm = OpenAIModelCustom(
    base_url=os.getenv("GROQ_BASE_URL"),
    api_key=os.getenv("GROQ_API_KEY"),
    model_name=os.getenv("GROQ_MODEL"),
)


class DeepEval:
    def __init__(self, custom_llm=global_custom_llm):
        self.correctness_metric_professionalism = GEval(
            name="Correctness",
            criteria=("Determine whether the actual output is factually correct "),
            evaluation_steps=[
                "Check whether the facts in 'actual output' contradict any facts in 'expected output'.",
                "Verify whether the key facts in 'expected output' are present in 'actual output'.",
                "Do NOT penalize additional content, as long as it is accurate and consistent.",
            ],
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.EXPECTED_OUTPUT,
            ],
            model=custom_llm,
        )

    def eval(self, input_user, actual_output, expected_output):
        test_case = LLMTestCase(
            input=input_user,
            actual_output=actual_output,
            expected_output=expected_output,
        )

        return self.correctness_metric_professionalism.measure(test_case)


# teste = DeepEval()

# teste.eval(
#     input_user="como posso configurar o servidor?",
#     output_response_model=(
#     "Claro! Posso te ajudar com isso. Para configurar o servidor, você precisa "
#     "instalar primeiro os pacotes necessários. Depois é só ajustar os arquivos "
#     "de configuração. Qual parte você não conseguiu fazer?"
# )
# )

# teste.eval(
#     input_user="como posso configurar o servidor?",
#     output_response_model=(
#     "Para configurar adequadamente o servidor, recomendo iniciar pela instalação "
#     "dos pacotes essenciais e dependências. Em seguida, ajuste os arquivos de "
#     "configuração conforme os requisitos do ambiente. Caso precise de suporte em "
#     "alguma etapa específica, posso orientar com mais detalhes."
# )
# )
