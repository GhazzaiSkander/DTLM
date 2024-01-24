#!/usr/bin/env python
# coding: utf-8

# In[1]:

import logging
import ipywidgets as widgets
from .completion import get_completion
from .verification import Edges_Verification

def simple_transformation(df):
    # Dropdown for column selection
    column_selector = widgets.Dropdown(
        options=df.columns,
        description='Select Column:',
        disabled=False)
    # Widgets for description-based transformation
    description_input = widgets.Text(
        description='Describe Transformation:',
        placeholder='e.g., Convert C to F'
    )
    # Widgets for single input-output example
    input_example = widgets.Text(description='Input:')
    output_example = widgets.Text(description='Output:')

    # Button for adding the example pair
    add_example_button = widgets.Button(description="Add Example Pair")

    # Button for processing all added examples
    #process_examples_button = widgets.Button(description="Process Examples", disabled=True)
    process_examples_button = widgets.Button(description="Process Examples")

    # Output area
    output_area = widgets.Output()

    # Store example pairs
    example_pairs = []



    # Function to display current pairs
    def display_current_pairs():
        """
        Displays the current input-output example pairs.

        This function iterates over the global list `example_pairs` and prints each pair.
        If no pairs have been added yet, it prints an informative message.
        """
        with output_area:
            output_area.clear_output()
            if example_pairs:
                print("Current pairs:")
                for i, (inp, out) in enumerate(example_pairs, start=1):
                    print(f"{i}. Input: {inp} -> Output: {out}")
            else:
                print("No pairs added yet.")

    # Function to add example pair
    def add_example_pair(b):

        """
        Adds a new input-output example pair.

        This function takes the input and output from input fields (`input_example` and `output_example`),
        appends the pair to the global list `example_pairs`, and then clears the input fields.
        """
        inp = input_example.value
        out = output_example.value
        if inp and out:
            example_pairs.append((inp, out))
            input_example.value = ''  # Clear input field
            output_example.value = ''  # Clear output field
            #process_examples_button.disabled = False
        display_current_pairs()

    # Function to process all examples
    def process_examples(b):
        """
        Processes all added example pairs.

        This function collects the transformation description and selected column, displays them along with
        the input-output pairs, and then generates a prompt template for the large language model.
        """
        with output_area:
            output_area.clear_output()
            description = description_input.value
            column=column_selector.value
            inputs=list(df[column].values)
            print(f"Transformation Description: {description}")
            print("Processing the following pairs:")
            for inp, out in example_pairs:
                print(f"Input: {inp} -> Output: {out}")
            # Add your processing logic here
            #print("Prompt ", description,  example_pairs, column )
            try :
              print("Generating messages for model...")
              messages=simple_pormpt_template(example_pairs,description,inputs)
              print(messages)
              print("Getting completion from the model...")
              #Response_Content, Prompt_Nb_Tokens, Response_Nb_Tokens=get_completion(messages)
              Response_Content, Prompt_Nb_Tokens, Response_Nb_Tokens=get_completion(messages)
              try:
                  print("Processing model response...")
                  output = list(Edges_Verification(Response_Content))
              except:
                  print("Automatic extraction failed. Please review the response content below:")
                  print(Response_Content)
                  print("\nPlease manually enter the list in a valid Python list format, e.g., ['item1', 'item2', ...]")
                  output_str = input("Enter the list: ")
                  try:
                      output = ast.literal_eval(output_str)
                      if not isinstance(output, list):
                          raise ValueError("Entered data is not a list.")
                  except Exception as e:
                      print(f"Error in manual input: {e}")
                      output = []
              
              new_column_name = column + "_transformed"
              if new_column_name in df.columns:
                       logging.warning(f"Column '{new_column_name}' already exists. Overwriting the column.")
              df[new_column_name] = output
              print(f"Transformation is done for the column '{column}'. New column '{new_column_name}' added.")

            except Exception as e:
              logging.error("An error occurred during the transformation process: ", exc_info=True)
            #Response_Content, Prompt_Nb_Tokens, Response_Nb_Tokens = get_completion(messages, Model="gpt-4")

    # Initial display of pairs
    display_current_pairs()

    # Linking buttons to functions
    add_example_button.on_click(add_example_pair)
    process_examples_button.on_click(process_examples)

    display(column_selector, description_input, input_example, output_example, add_example_button, process_examples_button, output_area)


# In[ ]:




