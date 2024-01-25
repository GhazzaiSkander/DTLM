#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tiktoken
max_tokens=4000
model_name="gpt-4"
encoding = tiktoken.encoding_for_model(model_name)
def encoding_for_model(model_name):
    # Replace this with the actual implementation from tiktoken
    return tiktoken.encoding_for_model(model_name)

def number_of_tokens(string, encoding):
    return len(encoding.encode(string))

def allowed_list(list_string,max_tokens):
    return number_of_tokens(list_string,encoding) < max_tokens//2


def split_list_diatomic(values, encoding, half_max_tokens):
    if len(values) == 0:
        return []
    if number_of_tokens(str(list(values)), encoding) <= half_max_tokens:
        return [values]

    # Splitting the list into two halves
    mid_index = len(values) // 2
    first_half = values[:mid_index]
    second_half = values[mid_index:]

    # Recursively apply the function to each half
    first_half_result = split_list_diatomic(first_half, encoding, half_max_tokens)
    second_half_result = split_list_diatomic(second_half, encoding, half_max_tokens)

    # Combine the results
    return first_half_result + second_half_result

def split_list_by_token_limit(values, max_tokens=4000, model_name="gpt-4"):
    encoding = encoding_for_model(model_name)
    half_max_tokens = max_tokens // 2

    # Apply the diatomic division
    result = split_list_diatomic(values, encoding, half_max_tokens)

    print(f"The inputs are going to be processed in {len(result)} batches")
    return result

