#!/usr/bin/env python3
# this is a comment for dima
"""this module reads a file in json format, data structure is presentd below
and will save a flie in yaml format with the claulated data, based on format2
the method will overwite output yaml file if exists

input format:
   ppl_ages:
      name: age
      name: age....
   buckets:
       list of age buckets to sort the names in 
output format:
   age_range(python/tuple):
      [ list names ].....
"""
import yaml
import json
import sys
import os

def build_tupples_zip (dict):
    """ build_tupples_zip 
    Args:
        dict: out specual dictionary  
    Returns:
        zip with tupple parttitions of the different buckets
    """
    (min_val,max_val)=min(dict["ppl_ages"].values()),max(dict["ppl_ages"].values())
    (min_key,max_key)=min(dict["buckets"]),max(dict["buckets"])
    min_val=(0 if min_val<min(dict["buckets"]) else min(dict["buckets"]))
    if max_val<=max_key:
        tupples_zip=zip([min_val]+sorted(dict["buckets"]),sorted(dict["buckets"]))
    else:
        tupples_zip=zip([min_val]+sorted(dict["buckets"]),sorted(dict["buckets"]+[max_val]))
    return tupples_zip


def between_tupple(num,the_tupple):
    """ between_tupple gets two input variables
       Args:
         nun: a number 
         the_tupple: tupple of two numbers
       Returns:
         True or False weather the number is between the two numbers int he tupple
    """
    if the_tupple[0] <= num < the_tupple[1]:
       return True
    return False


def init_output_dict(dict,tupples_zip):
    """ this function initiates the dictionary based on a zip
       Args:
         dict: an empty dictionary (not validated)
         tupples_zip: zip of tupple of two numbers
       Returns:
         it sets the dictionary with keys to empty arrays based on the tupples_zip
    """
    for i in tupples_zip:
       dict[i]=[]


def fill_dict(input_dict,output_dict):
    """ this function initiates the dictionary based on a zip
       Args:
         input_dict: dictionary in the initial format
         output_dict: dictionary with touple keys
       Returns:
         if will pupulate the output_dict with all the names from the input_dict
           if their age is between the numbers in the touple (key)
    """
    for name,age in input_dict["ppl_ages"].items():
        for out_key in output_dict.keys():
            if between_tupple(age,out_key):
                output_dict[out_key].append(name)
                break



def main(input_file_name):
    """main will read a file with the initial data in json format and save a file with the output data in yaml format
    Args:
      input_file_name: the file name to read the data from (in Json format)
    """
    output_file_name=os.path.splitext(input_file_name)[0]+".yaml"
    try:
        yaml_file = None
        with open(input_file_name) as json_file:
            in_data = json.load(json_file)
        output_dict={}
        tuppeled_keys=build_tupples_zip(in_data)
        init_output_dict(output_dict,tuppeled_keys)
        fill_dict(in_data,output_dict)
        with open(output_file_name, 'wt') as yaml_file:
            yaml.dump(output_dict, yaml_file, default_flow_style=False)
    except (FileNotFoundError) as e:
        print("cannot find file '"+input_file_name+"'") 
    except (json.decoder.JSONDecodeError):
        print("file '"+input_file_name+"' is not in json format")

if __name__ == '__main__':
    if len(sys.argv)!=2:
       print ("usage:",sys.argv[0], "<file_name>")
    else:
      main(sys.argv[1])
