#!/usr/bin/env python
# coding: utf-8

# In[1]:

#!/usr/bin/env python
# coding: utf-8

def simple_prompt_template(Input_Output_Pair_Examples, Desired_Format_Keywords, inputs):
    """
    Generates a formatted prompt for a large language model to transform data values based on explicit examples and keywords.

    This function creates a structured prompt incorporating explicit instructions for transforming data values into a specified format,
    emphasizing returning the original value if the transformation is uncertain and ensuring the number of outputs matches the number of inputs.

    Parameters:
    - Input_Output_Pair_Examples (list of tuples): Example input-output pairs.
    - Desired_Format_Keywords (str): Keywords describing the desired output format.
    - inputs (list): Input data values to be transformed.

    Returns:
    - list: A list of dictionaries for structured interaction with a language model.

    Raises:
    - ValueError: If both Input_Output_Pair_Examples and Desired_Format_Keywords are missing.

    Note:
    - Designed for structured prompts in large language models.
    """
    if not Input_Output_Pair_Examples and not Desired_Format_Keywords:
        raise ValueError("Input examples or format keywords must be provided.")

    messages = [{"role": "system", "content": "You are a helpful assistant that transforms values into the specified format. If unsure about any transformation, return the original value. Ensure the number of outputs matches the number of inputs exactly."}]

    prompt_introduction = "Given different values in data format, the objective is to transform individual values to align with the new format. The model should transform each provided value with 100% accuracy. If the model is unsure about any transformation, it should return the original value. The number of transformed values in the output should exactly match the number of input values."

    if Input_Output_Pair_Examples:
        example_input = [pair[0] for pair in Input_Output_Pair_Examples]
        example_output = [pair[1] for pair in Input_Output_Pair_Examples]
        examples_section = f"**Examples**:{len(example_input)} number of examples \nValues: {list(example_input)}\nOutput: {list(example_output)}"
    else:
        examples_section = ""

    if Desired_Format_Keywords:
        keywords_section = f"The value to be transformed into the appropriate format: {Desired_Format_Keywords}\n"
    else:
        keywords_section = ""

    inputs_section = f"**Inputs**: {inputs} Ensure the output count matches the number of inputs {len(inputs)}.\n**Output**: "

    full_prompt = f"{prompt_introduction}\n\n{examples_section}\n\n{keywords_section}\n{inputs_section}"

    messages.append({"role": "user", "content": full_prompt})

    return messages
