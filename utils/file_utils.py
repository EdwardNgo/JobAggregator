import os
import json

def save_links(path,links):
    with open(path,'w+') as f:
        for link in links:
            f.write(link + '\n')

def save_jobs(path,json_list):
    with open(path,'w+') as f:
        json.dump(json_list,f,ensure_ascii=True,indent = 4)

def createDir(path):
    try: 
        os.makedirs(path)
    except:
        print("folder existed")