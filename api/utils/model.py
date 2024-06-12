import os

from dotenv import load_dotenv
import anthropic
import openai

load_dotenv()
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

def model_loader(provider, model, system_prompt, message_array, userid, sessionid, max_tokens=4096, temperature=0.0, image_base64=None):
    """
    Load and execute the specified model based on the provider.
    """
    model_name = os.getenv(f"{provider.upper()}_{model.upper()}")

    if provider == "anthropic":
        if image_base64:
            message_text = message_array[-1]["content"]
            message_array[-1]["content"] = [
                {
                    "type": "image", 
                    "source": {
                        "media_type": "image/jpeg",
                        "type": "base64",
                        "data": image_base64,
                    }
                },
                {
                    "type": "text", 
                    "text": message_text
                }
            ]
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
        message_array = [{"role": "system", "content": system_prompt}] + message_array
        if image_base64:
            message_text = message_array[-1]["content"]
            message_array[-1]["content"] = [
                {
                    "type": "image_url", 
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}",
                    }
                },
                {
                    "type": "text", 
                    "text": message_text
                }
            ]
        response_message = openai.chat.completions.create(
            model=model_name,
            messages=message_array,
            max_tokens=max_tokens,
            temperature=temperature
        )
        response_content = response_message.choices[0].message.content
    else:
        raise ValueError(f"Invalid provider: {provider}")

    return response_content
