from docling.datamodel.pipeline_options import (
    PictureDescriptionApiOptions,
)





def lms_local_options(model: str, base_url: str, api_key: str = None):

    options = PictureDescriptionApiOptions(
        url=base_url,
        params=dict(
            model=model,
            seed=42,
            max_completion_tokens=200,
            api_key=api_key
        ),
        prompt="Describe the image in three sentences. Be concise and accurate.",
        timeout=90,
    )
    return options



def remote_vlm_options(api_key : str, 
                     base_url : str = "https://api.groq.com/openai/v1/chat/completions", 
                     model : str = "meta-llama/llama-4-maverick-17b-128e-instruct"):
    
    url = base_url

    options = PictureDescriptionApiOptions(
        url=url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        params=dict(
            model=model,
            max_tokens=300,
            temperature=0.0,
        ),
        prompt="Describe the image in three sentences. Be concise and accurate.",
        timeout=60,
    )

    return options



