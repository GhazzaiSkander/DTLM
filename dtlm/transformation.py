#!/usr/bin/env python
# coding: utf-8

# In[1]:


import logging

import time
import ipywidgets as widgets
from datetime import datetime
# Example usage
from .completion import get_completion
from .verification import Edges_Verification
from .prompt import simple_prompt_template
from .prompt import generate_prompt
from .counter import split_list_by_token_limit
from .history import log_experiment
from sklearn.metrics import accuracy_score
from .verification import Edges_Verification_Improved
import ast

def generate_experiment_id(Model="gpt-4"):
    return Model+datetime.now().strftime("exp_%Y%m%d_%H%M%S")
def simple_transformation(df, Model="gpt-4",client=None,dataset_name="Unknown",filename="experiment_results.csv",verbose=False):
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
            if verbose :
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
            sublists=split_list_by_token_limit(inputs)
            print(f"Transformation Description: {description}")
            print("Processing the following pairs:")
            results=[]
            if example_pairs:
                for inp, out in example_pairs:
                    print(f"Input: {inp} -> Output: {out}")
            # Add your processing logic here
            #print("Prompt ", description,  example_pairs, column )
            Total_Nb_Token=0
            iteration=0
            for subpart in sublists :
                start_time = time.time()
                try :
                  if verbose :
                      print("Working with batch number", iteration)
                      iteration+=1
                      print("Generating messages for model...")
                  print("Processing this number of element" , len(subpart))
                  #messages=simple_prompt_template(example_pairs,description,subpart)
                  messages=generate_prompt(example_pairs,description,subpart,Model)
                  if verbose :  
                      print(messages)
                      print("Getting completion from the model...")
                  Response_Content, Prompt_Nb_Tokens, Response_Nb_Tokens=get_completion(messages,Model,client)
                  if verbose: 
                      print(Response_Content)
                  Total_Nb_Token+=Prompt_Nb_Tokens + Response_Nb_Tokens 
                  try:
                      print("Processing model response...")
                      output = list(Edges_Verification(Response_Content))
                  except:
                      print("Automatic extraction failed. Please review the response content below:")
                      print(Response_Content)
                      #print("\nPlease manually enter the list in a valid Python list format, e.g., ['item1', 'item2', ...]")
                      
                      output_str = Edges_Verification_Improved(Response_Content)
                      output=list(output_str)
                      """
                      try:
                          output = ast.literal_eval(output_str)
                          if not isinstance(output, list):
                              raise ValueError("Entered data is not a list.")
                      except Exception as e:
                          print(f"Error in manual input: {e}")
                          output = []"""
                          
                  print("The number of element that has been processed" , len(output))
                  print("--- %s seconds ---" % (time.time() - start_time))
                  if len(output) !=len(subpart) :
                        print("len(output) !=len(subpart) this condition is True")
                        # Splitting the list into two halves
                        mid_index = len(subpart) // 2
                        first_half = subpart[:mid_index]
                        second_half = subpart[mid_index:]
                        #####working with the first part 
                        #messages=simple_prompt_template(example_pairs,description,first_half)
                        messages=generate_prompt(example_pairs,description,first_half,Model)

                        Response_Content, Prompt_Nb_Tokens, Response_Nb_Tokens=get_completion(messages,Model,client)
                        output_1 = list(Edges_Verification(Response_Content))
                        #####Working for the second part
                        #messages=simple_prompt_template(example_pairs,description,second_half)
                        messages=generate_prompt(example_pairs,description,second_half,Model)

                        Response_Content, Prompt_Nb_Tokens, Response_Nb_Tokens=get_completion(messages,Model,client)
                        output_2 = list(Edges_Verification(Response_Content))
                        results.extend(output_1)
                        results.extend(output_2)
                  else:     
                      results.extend(output)
                      print(len(results))
                except Exception as e:
                    logging.error("An error occurred during the transformation process: ", exc_info=True)
            new_column_name = column + "_transformed"
            if new_column_name in df.columns:
                    logging.warning(f"Column '{new_column_name}' already exists. Overwriting the column.")
            try :
                df.loc[:, new_column_name] = results
                print(f"Transformation is done for the column '{column}'. New column '{new_column_name}' added.")

            except Exception as e:
                print("An error occurred during the integration of the results into the dataframe")
                print(results)
                print(len(results))
            if len(results)==len(inputs):
                try :
                    Unchanged_values=accuracy_score(inputs,results)
                except :
                    print("the accuracy couldn't be calculated we are returning a non values ")
                    Unchanged_values="N/A"
                    
                experiment_data = {
                        "experiment_id": generate_experiment_id(Model),
                        "Dataset_Name": dataset_name,
                        "Column_name": column,
                        "inputs": inputs,
                        "description_keywords": description,
                        "example_pairs": example_pairs,
                        "output": results,
                        "accuracy": Unchanged_values,
                        "total_number_of_token": Total_Nb_Token
                    }
                log_experiment(experiment_data)
                print("The transformation is now complete")
                if verbose :
                    print("The is the data add it in the experiment_data ",experiment_data)

            else :
                experiment_data = {
                        "experiment_id": generate_experiment_id(Model),
                        "Dataset_Name": dataset_name,
                        "Column_name": column,
                        "inputs": inputs,
                        "description_keywords": description,
                        "example_pairs": example_pairs,
                        "output": results,
                        "accuracy": "N/A",
                        "total_number_of_token": Total_Nb_Token
                    }
                log_experiment(experiment_data)
                print("The transformation is now complete")

    


    # Initial display of pairs
    display_current_pairs()

    # Linking buttons to functions
    add_example_button.on_click(add_example_pair)
    process_examples_button.on_click(process_examples)

    display(column_selector, description_input, input_example, output_example, add_example_button, process_examples_button, output_area)


def basic_transformation(df,column,example_pairs,description,input,dataset_name="Unknown",filename="experiment_results.csv",verbose=False):
      messages=simple_prompt_template(example_pairs,description,subpart)

      Response_Content, Prompt_Nb_Tokens, Response_Nb_Tokens=get_completion(messages)
      output = list(Edges_Verification(Response_Content))
      new_column_name = column + "_transformed"+description
      try :
        df.loc[:, new_column_name] = results
        print(f"Transformation is done for the column '{column}'. New column '{new_column_name}' added.")
        experiment_data = {
                      "experiment_id": generate_experiment_id(Model),
                      "Dataset_Name": dataset_name,
                      "Column_name": column,
                      "inputs": inputs,
                      "description_keywords": description,
                      "example_pairs": example_pairs,
                      "output": results,
                      "accuracy": accuracy_score(inputs,results),
                      "total_number_of_token": Total_Nb_Token
                  }
      except :
        print("problem with the results inputs and results")
        experiment_data = {
                      "experiment_id": generate_experiment_id(Model),
                      "Dataset_Name": dataset_name,
                      "Column_name": column,
                      "inputs": inputs,
                      "description_keywords": description,
                      "example_pairs": example_pairs,
                      "output": results,
                      "accuracy": "Corrupted_function",
                      "total_number_of_token": Total_Nb_Token
                  }




def complex_transformation(df, model="gpt-4", client=None, dataset_name="Unknown", filename="experiment_results.csv", verbose=False):
    """
    An enhanced transformation function that allows users to specify detailed context and chain of thought
    for transforming data in a pandas DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data to be transformed.
    - model (str): The model to use for the transformation, default is "gpt-4".
    - client: The API client for interacting with the model.
    - dataset_name (str): Name of the dataset for logging purposes.
    - filename (str): File name for saving experiment results.
    - verbose (bool): If True, prints detailed logs of the transformation process.
    """
    
    # UI components for specifying transformation details
    column_selector = widgets.Dropdown(options=df.columns, description='Select Column:', disabled=False)
    description_input = widgets.Text(description='Describe Transformation:', placeholder='e.g., Convert temperatures from C to F')
    context_input = widgets.Textarea(description='Context:', placeholder='e.g.,The context of the transformation ...')
    additional_knowlodge_input = widgets.Textarea(description='Additional_knowledge:', placeholder='e.g.,Ground truth  for the model ...')

    chain_of_thought_input = widgets.Textarea(description='Chain of Thought:', placeholder='e.g., Chain of thougths...')
    input_example = widgets.Text(description='Input Example:')
    output_example = widgets.Text(description='Output Example:')
    add_example_button = widgets.Button(description="Add Example Pair")
    process_button = widgets.Button(description="Process Transformation")
    output_area = widgets.Output()

    example_pairs = []  # To store input-output example pairs
    
    def add_example_pair(b):
        """
        Adds a new input-output example pair to the list and displays current pairs.
        """
        inp = input_example.value
        out = output_example.value
        if inp and out:  # Check if both input and output are provided
            example_pairs.append((inp, out))
            input_example.value = ''  # Clear fields after adding
            output_example.value = ''
            display_current_pairs()  # Display updated list of pairs

    def display_current_pairs():
        """
        Displays the current list of input-output example pairs in the output area.
        """
        with output_area:
            output_area.clear_output()  # Clear previous outputs
            if example_pairs:
                print("Current input-output pairs:")
                for i, (inp, out) in enumerate(example_pairs, start=1):
                    print(f"{i}. {inp} -> {out}")
            else:
                print("No example pairs added yet.")
                
    def process_transformation(b):
        """
        Processes the transformation based on user inputs, context, and chain of thought.
        """
        # Implementation for processing the transformation
        # This should include generating prompts for the model based on the user inputs,
        # context, chain of thought, and the input-output examples.
        with output_area:
            output_area.clear_output()
            column=column_selector.value
            inputs=list(df[column].values)
            print("Processing transformation...")
            description=description_input.value
            context=context_input.value
            if example_pairs:
                for inp, out in example_pairs:
                    print(f"Input: {inp} -> Output: {out}")
            additional_knowlodge=additional_knowlodge_input.value
            chain_of_thought=chain_of_thought_input.value
            #Ditcomtic split
            sublists=split_list_by_token_limit(inputs)
 
            Total_NB_tokens=0
            for subpart in sublists :
              print("Processing this number of element" , len(subpart))
              start_time=time.time()
              try :
                if verbose :
                  print("Working  with the batch number", iteration)
                  iteration+=1
                  print("Generation messages for model..")
                  prompt=generate_prompt_complet(example_pairs, description, context,chain_of_thought,additional_knowlodge,subpart,model)
                  if verbose :
                    for msg in prompt :
                      print(msg)
                  Response_Content, Prompt_Nb_Tokens, Response_Nb_Tokens=get_completion(prompt,model,client)
                  if verbose :
                    print(Response_Content)
                  Total_Nb_Token+=Prompt_Nb_Tokens + Response_Nb_Tokens 
                  try :
                    print("Processing Model response ...")
                    output = list(Edges_Verification(Response_Content))
                  except :
                    print("Automatic extraction failed. Second attemp")
                    output_str = Edges_Verification_Improved(Response_Content)
                    output=list(output_str)
                    if len(output)!=len(subpart):
                        if verbose:
                          print("Problem with the number of element we are going divide the list in two ")
                        mid_index = len(subpart) // 2
                        first_half = subpart[:mid_index]
                        second_half = subpart[mid_index:]
                        prompt=generate_prompt_complet(example_pairs, description, context,chain_of_thought,additional_knowlodge,first_half,model)
                        Response_Content, Prompt_Nb_Tokens, Response_Nb_Tokens=get_completion(prompt,model,client)
                        try :
                          output_1 = list(Edges_Verification(Response_Content))
                        except:
                          output_1=list(Edges_Verification_Improved(Response_Content))
                        prompt=generate_prompt_complet(example_pairs, description, context,chain_of_thought,additional_knowlodge,second_half,model)
                        try :
                          output_2=list(Edges_Verification(Response_Content))
                        except:
                          output_2=list(Edges_Verification_Improved(Response_Content))
                        results.extend(output_1)
                        results.extend(output_2)
                    else :
                      results.extend(output)
                      print("the length the results",len(results))
              
              except  Exception as e :
                print("Problem with the iteration ", len(subpart))
                logging.error("An error occurred during the transformation process: ", exc_info=True)
              print("The number of element that has been processed" , len(results))
              print("--- %s seconds ---" % (time.time() - start_time))
              new_column_name=column+"_"+description+"_Transformation"
              try :
                df.loc[:,new_column_name]=experiment_results
                print(f"Transformation is done for the column '{column}'. New column '{new_column_name}' added.")
              
              except Exception as e:
                  print("An error occurred during the integration of the results into the dataframe")
                  print(results)
                  print(len(results))
              try :
                Unchanged_values=accuracy_score(inputs,results)
              except:
                print("The accuracy couldn't be calculated we are returning a non values ")
                Unchanged_values="N/A"
              experiment_data = {
                        "experiment_id": generate_experiment_id(Model),
                        "Dataset_Name": dataset_name,
                        "Column_name": column,
                        "inputs": inputs,
                        "description_keywords": description,
                        "example_pairs": example_pairs,
                        "output": results,
                        "accuracy": Unchanged_values,
                        "total_number_of_token": Total_Nb_Token
                    }
              log_experiment(experiment_data)
              print("The transformation is now complete")
              if verbose :
                 print("The is the data add it in the experiment_data ",experiment_data)


            # Here, you would integrate the logic to use the model for data transformation
            # This can involve constructing a detailed prompt with the provided information
            # and sending it to the model for processing.
            
            # Example of what might be included in your processing logic:
            # 1. Construct the prompt using the description, context, chain of thought, and example pairs.
            # 2. Send the prompt to the model for each value in the selected column.
            # 3. Display the transformed values and any relevant logs if verbose is True.
    
    # Link buttons to their action functions
    add_example_button.on_click(add_example_pair)
    process_button.on_click(process_transformation)
    
    # Layout the widgets
    input_widgets = widgets.VBox([column_selector, description_input, context_input,additional_knowlodge_input, chain_of_thought_input, input_example, output_example, add_example_button, process_button])
    display(input_widgets, output_area)
