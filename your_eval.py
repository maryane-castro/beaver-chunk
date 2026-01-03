from evaluator.deep_eval import DeepEval


deep_eval = DeepEval()


input_user= "qual ultimo faturamento"
actual_output= "54.45"
expected_output= "o ultimo faturamento presente no relatorio é de 54.45"


deep_eval.eval(
    input_user= input_user,
    actual_output=actual_output,
    expected_output=expected_output
)