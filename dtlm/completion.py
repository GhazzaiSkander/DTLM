import openai
from mistralai.models.chat_completion import ChatMessage
from mistralai.client import MistralClient

def get_completion(messages, model="gpt-4", client=None):
    """
    Retrieves a completion from a specified language model based on the provided messages.

    This function communicates with OpenAI's ChatCompletion API, sending a sequence of messages to a specified model (default is GPT-4) and receiving the model's response. It also extracts the number of tokens used in the prompt and response for tracking and analysis purposes.

    Parameters:
    - messages (list of dicts): A list of messages in the format required by OpenAI's API, where each message is a dictionary with 'role' and 'content'.
    - model (str, optional): The name of the model to be used for generating completions. Default is 'gpt-4'.
    - client (MistralClient, optional): An instance of MistralClient to use when model is set to 'mistral'. If not provided, the function will not work with 'mistral' model.

    Returns:
    - tuple: A tuple containing:
        - Response_Content (str): The content of the model's response.
        - Prompt_Nb_Tokens (int): The number of tokens used in the prompt.
        - Response_Nb_Tokens (int): The number of tokens used in the response.

    Note:
    - This function requires access to OpenAI's API and the appropriate API keys to function properly.
    """
    if model == "gpt-4":
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0)
        # Extract relevant information from the response
        Response_Content = response.choices[0].message["content"]
        Prompt_Nb_Tokens = response["usage"]["prompt_tokens"]
        Response_Nb_Tokens = response["usage"]["completion_tokens"]

        return Response_Content, Prompt_Nb_Tokens, Response_Nb_Tokens

    elif model == "mistral":
        if not client:
            raise ValueError("MistralClient instance must be provided for 'mistral' model.")
        chat_response = client.chat(model=model, messages=messages)
        choice = chat_response.choices[0]  # Access the first choice
        usage = chat_response.usage  # Access the token count
        message_content = choice.message["content"]  # Extract the content of the message.
        
        return message_content, usage.prompt_tokens, usage.completion_tokens
