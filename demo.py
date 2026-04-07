import os
from pathlib import Path
from PIL import Image
from app_secrets import OPENAI_API_KEY
from sql_execution import execute_sf_query

#create env variable
os.environ("OPENAI_API_KEY") =OPENAI_API_KEY
root_path = [p for p in Path(__file__).parents if p.parts[-1]=="ai_app_demo"][0]
print(root_path)