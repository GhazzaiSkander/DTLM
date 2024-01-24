
import re
import ast
def Edges_Verification(response_content):

    """
    Extracts a list from a string response, ensuring proper format for parsing.

    This function is designed to handle responses from language models that are expected to be in list format. It attempts to parse the string response into a Python list, handling various edge cases to ensure the string is correctly formatted for parsing.

    Parameters:
    - response_content (str or list): The content of the response, either as a string or a list.

    Returns:
    - list: The parsed list from the response content.

    Raises:
    - ValueError: If the input is neither a string nor a list, or if parsing fails.
    """
    # Check if the input is already in the desired format (list)
    if isinstance(response_content, list):
        return response_content

    # Ensure the input is a string
    if not isinstance(response_content, str):
        raise ValueError("Input must be a string or a list")
    response_content = response_content.strip()
    # Find the first occurrence of '[' and trim the string to start from there
    index = response_content.find("[")
    if index !=-1:
      response_content=response_content[index:]
    # Use regular expression to find the list content
    match = re.search(r'\[.*\]', response_content)
    #print("response_content_1",response_content)
    if match:
        if response_content[-2] != "'":
            response_content = response_content[:-1] + "'" + response_content[-1]
        if response_content[1] != "'":
            response_content = response_content[:1] + "'" + response_content[1:]
        return ast.literal_eval(response_content)
    else:
        if not response_content.startswith("["):
            if response_content[0] == "," or response_content[0] == "'":
                response_content = "[" + response_content
            else:
                response_content = "['" + response_content

        if not response_content.endswith("]"):
            if response_content.endswith("'") or response_content.endswith(","):
                response_content = response_content + "]"
            else:
                response_content = response_content + "']"
        # Check if the second-to-last character is neither a quote nor a comma
        if response_content[-2]!="'":
          if response_content[-2]==",":
            verif_1=response_content[:-2]
            verif_1=verif_1.strip()
            if verif_1[-1]=="'":
              pass
            else:
              response_content=response_content[:-2]+"'"+response_content[-2:]
          else :
            response_content = response_content[:-1] + "'" + response_content[-1]
        if response_content[-2] != "'" and (response_content[-2] != "," and response_content[-3]!="'") :
            response_content = response_content[:-1] + "'" + response_content[-1]
        if response_content[-2] == "'":
            verif_part = response_content[:-2]
            verif_part = verif_part.strip()
            if verif_part.endswith(","):
                response_content = verif_part + "]"

    return ast.literal_eval(response_content)


# In[ ]:




