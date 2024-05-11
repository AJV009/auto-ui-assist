import os

from dotenv import load_dotenv
import anthropic
import openai

load_dotenv()
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

def model_loader(provider, model, system_prompt, message_array, userid, sessionid, max_tokens=4096, temperature=0.0):
    """
    Load and execute the specified model based on the provider.
    """
    model_name = os.getenv(f"{provider.upper()}_{model.upper()}")

    if provider == "anthropic":
        response_message = anthropic_client.messages.create(
            model=model_name,
            system=system_prompt,
            messages=message_array,
            max_tokens=max_tokens,
            metadata={"user_id": userid+"-"+sessionid},
            temperature=temperature
        )
        response_content = response_message.content[0].text
    elif provider == "openai":
        messages = [{"role": "system", "content": system_prompt}] + message_array
        response_message = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        response_content = response_message.choices[0].message.content
    else:
        raise ValueError(f"Invalid provider: {provider}")

    return response_content
