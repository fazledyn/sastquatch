from dotenv import load_dotenv
from pymongo import MongoClient
import json
import sys
import os




if len(sys.argv) < 2:
    print("Usage: <script> [dir/to/sarif]")
    exit(0)


dir_name = sys.argv[1]
sarif_list = os.listdir(dir_name)

def extract_metadata(file_name):
    temp = file_name.split("__")
    platform = temp[0]
    owner = temp[1]
    repo = temp[2]
    

for sarif in sarif_list:
    sarif_path = os.path.join(dir_name, sarif)
    sarif_content = None
    
    with open(sarif_path, "r") as s:
        sarif_content = json.load(s)



