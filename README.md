# RAG-Project
This is a minimal implementation of the RAG model for Question answering .

## Requirements
1) python 3.8 
Note : install python from miniconda
2) create a new environment
3) Activate  the environment


## imptrant note 
> installation
1- install the requirments
''' 
$ pip install -r requirment.txt
'''

## setup the  environment variables


'''
cp  .env.example  .evn
'''
set your environment variables in the '.env'file. for example 'OPEN_APi_KEY" value.

##next step :
ran the FastAPI


# load Settings management using Pydantic
pip install pydantic-settings
or 
in faile requirment.txt add library and after this step write 
pip install -r requirment.txt 

Usage¶
If you create a model that inherits from BaseSettings, the model initialiser will attempt to determine the values of any fields not passed as keyword arguments by reading from the environment. (Default values will still be used if the matching environment variable is not set.)

This makes it easy to:

Create a clearly-defined, type-hinted application configuration class
Automatically read modifications to the configuration from environment variables
Manually override specific settings in the initialiser where desired (e.g. in unit tests)


