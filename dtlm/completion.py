#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install openai==0.27.0.')
import openai
def get_completion(messages, Model="gpt-4"):
    """
    Retrieves a completion from a specified language model based on the provided messages.

    This function communicates with OpenAI's ChatCompletion API, sending a sequence of messages to a specified model (default is GPT-4) and receiving the model's response. It also extracts the number of tokens used in the prompt and response for tracking and analysis purposes.

    Parameters:
    - messages (list of dicts): A list of messages in the format required by OpenAI's API, where each message is a dictionary with 'role' and 'content'.
    - Model (str, optional): The name of the model to be used for generating completions. Default is 'gpt-4'.

    Returns:
    - tuple: A tuple containing:
        - Response_Content (str): The content of the model's response.
        - Prompt_Nb_Tokens (int): The number of tokens used in the prompt.
        - Response_Nb_Tokens (int): The number of tokens used in the response.

    Note:
    - This function requires access to OpenAI's API and the appropriate API keys to function properly.
    """
    response=openai.ChatCompletion.create(
          model=Model,
          messages=messages,
          temperature=0)
    # Extract relevant information from the response
    Response_Content = response.choices[0].message["content"]  # The content of the model's response
    Prompt_Nb_Tokens = response["usage"]["prompt_tokens"]  # The number of tokens used in the prompt
    Response_Nb_Tokens = response["usage"]["completion_tokens"]  # The number of tokens used in the completion

    # Return the extracted information as a tuple
    return Response_Content, Prompt_Nb_Tokens, Response_Nb_Tokens

