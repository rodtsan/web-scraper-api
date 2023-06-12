from os import environ
import os 

OPENAI_API_KEY = environ.get('OPENAI_API_KEY')
OPENAI_API_ORG = environ.get('OPENAI_API_ORG')
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__)).split("//")[-1]