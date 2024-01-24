#!/usr/bin/env python
# coding: utf-8

# In[1]:


def simple_pormpt_template(Input_Output_Pair_Examples,Desired_Format_Keywords,inputs):
      """
      Generates a formatted prompt for a large language model to transform data values.

      This function creates a prompt that instructs a language model to transform input data values into a specified format. It uses examples of input-output pairs and desired format keywords to guide the transformation. The function supports different modes based on whether input-output examples and/or keywords are provided.

      Parameters:
      - Input_Output_Pair_Examples (list of tuples): A list of tuples where each tuple represents an example input and its corresponding transformed output.
      - Desired_Format_Keywords (str): Keywords or a phrase that describe the desired output format.
      - inputs (any): The input data values that need to be transformed.

      Returns:
      - list: A list of dictionaries, each representing a part of the prompt with a specific role ('system' or 'user') and content.

      Raises:
      - ValueError: If no input examples or format keywords are provided.

      Note:
      - The function is designed to work with large language models and assumes a specific prompt structure that such models can interpret.
      """
      messages = [{"role": "system", "content": "You are a helpful assistant that transforms values into the specified format."}]
      if Input_Output_Pair_Examples:
          example_input = [pair[0] for pair in Input_Output_Pair_Examples]
          example_output = [pair[1] for pair in Input_Output_Pair_Examples]
          if Desired_Format_Keywords:
              prompt_introduction = f"""Given different values in data format, the objective is to transform individual values to align to the new format.
  The model should be evaluated on its ability to transform all of the values to a specified format with 100% accuracy."""
              prompt_corps = f"""The value to be transformed into the appropriate format:{Desired_Format_Keywords}
  **Values**: {list(example_input)}
  **Output**: {list(example_output)}
  **Values**: {inputs}
  **Output**:"""
              messages.append({"role": "user", "content": prompt_introduction + prompt_corps})
          else:
              prompt_introduction = f"""Given a value in data format, the objective is to transform the value to align to the new format.
  The model should be able to transform any value to the specified format with 100% accuracy.\n"""
              prompt_corps = f"""The value to be transformed into the appropriate format:
  **Values**: {list(example_input)}
  **Output**: {list(example_output)}
  **Value**: {inputs}
  **Output**:"""
              messages.append({"role": "user", "content": prompt_introduction + prompt_corps})
      else:
          if Desired_Format_Keywords:
              prompt_introduction = f"""Given a value in data format, the objective is to transform the value to align to the new format.The model should be able to transform any value to the specified format with 100% accuracy."""
              prompt_corps = f"""\nThe value to be transformed into the appropriate format: {Desired_Format_Keywords}.
  **Value**: {inputs}
  **Output**:"""
              messages.append({"role": "user", "content": prompt_introduction + prompt_corps})
          else:
              print("NO INPUTS has been provided !!")
              prompt_introduction = f"""Given a value in data format, the objective is to transform the value into a new format.
  The model should be able to transform any value to a new format with 100% accuracy."""
              prompt_corps = f"""The value to be transformed:
  **Value**: {inputs}
  **Output**:"""
              messages.append({"role": "user", "content": prompt_introduction + prompt_corps})
      return messages

