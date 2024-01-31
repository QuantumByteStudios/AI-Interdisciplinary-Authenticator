import google.generativeai as palm
import utils
from api import API_KEY


def askBard(p):
    palm.configure(api_key=API_KEY)
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name
    # print(model)
    completion = palm.generate_text(
        model=model,
        prompt=str(p),
        # prompt="benefits of yoga bullet points", # Test prompt
        temperature=0,
        # The maximum length of the response
        # max_output_tokens=100,
    )

    # Remove particular symbols from the response
    source_code_tag = utils.colors.GREEN + utils.colors.BOLD + "<code> " + utils.colors.END
    bullet_point = utils.colors.BLUE + utils.colors.BOLD + "• " + utils.colors.END

    result = completion.result
    if result is not None:
        # result = result.replace("*", str(bullet_point)).replace("```", str(source_code_tag))
        result = result.replace("*", " ")
    else:
        result = ""
    # print(result)
    return result