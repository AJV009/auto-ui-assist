import os
import base64

from dotenv import load_dotenv
import anthropic
import openai

# Load environment variables
load_dotenv(override=True)

# Initialize API clients
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

def is_base64(s):
    try:
        base64.b64decode(s)
        return True
    except Exception:
        return False

def model_loader(provider, model, system_prompt, message_array, userid, sessionid, max_tokens=4096, temperature=0.0, image_base64=None):
    """
    Load and execute the specified AI model based on the provider.

    Args:
        provider (str): The AI provider ("anthropic" or "openai").
        model (str): The specific model to use.
        system_prompt (str): The system prompt for the AI.
        message_array (list): The conversation history.
        userid (str): The user's identifier.
        sessionid (str): The current session identifier.
        max_tokens (int, optional): Maximum number of tokens in the response. Defaults to 4096.
        temperature (float, optional): The randomness of the model's output. Defaults to 0.0.
        image_base64 (str, optional): Base64 encoded image data, if applicable.

    Returns:
        str: The AI model's response content.

    Raises:
        ValueError: If an invalid provider is specified.
    """
    # Get the full model name from environment variables
    model_name = os.getenv(f"{provider.upper()}_{model.upper()}")

    if provider == "anthropic":
        # Handle Anthropic models (e.g., Claude)
        if image_base64 and is_base64(image_base64):
            # Format the message for image input
            message_text = message_array[-1]["content"]
            message_array[-1]["content"] = [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_base64,
                    }
                },
                {
                    "type": "text", 
                    "text": message_text
                }
            ]
        # Call the Anthropic API
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
        # Handle OpenAI models (e.g., GPT-3.5, GPT-4)
        # Add system prompt to the beginning of the message array
        message_array = [{"role": "system", "content": system_prompt}] + message_array
        if image_base64 and is_base64(image_base64):
            # Format the message for image input
            message_text = message_array[-1]["content"]
            message_array[-1]["content"] = [
                {
                    "type": "image_url", 
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}",
                    }
                },
                {
                    "type": "text", 
                    "text": message_text
                }
            ]
        # Call the OpenAI API
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

# This utility file handles the loading and execution of AI models from different providers.
# It supports both text-based and image-based inputs, adapting the API calls accordingly.
# The function uses environment variables to fetch API keys and model names, ensuring security and flexibility.
