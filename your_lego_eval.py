from evaluator.deep_eval import DeepEval


deep_eval = DeepEval()


input_user = (
    "What was the non-GAAP operating efficiency ratio for SVB Financial in 2016?"
)
actual_output = "54.45"
expected_output = (
    "The non‑GAAP operating efficiency ratio for SVB Financial in 2016 was **54.39 %**."
)


result = deep_eval.eval(
    input_user=input_user, actual_output=actual_output, expected_output=expected_output
)
print(result)
