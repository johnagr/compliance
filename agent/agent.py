import subprocess
import requests
import json


#### AGENT FUNCTIONS ####
class Inventory():

    def processor_info():
        dict_result = {}
        command = subprocess.run(["lscpu"], text=True, stdout=subprocess.PIPE)

        for d in command.stdout.splitlines():
            (key,value) = d.split(":",1)
            dict_result[key] = value.lstrip()

        return { "Processor": dict_result["Model name"] }

    def processes_info():
        
        command = subprocess.run(['ps', '-e'], text=True,stdout=subprocess.PIPE).stdout.splitlines()
        # Code snippet for parsing the ps output. https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501
        headers = [h for h in ' '.join(command[0].strip().split()).split() if h ]
        raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), command[1:])
        dict_result = [dict(zip(headers, r)) for r in raw_data]
        
        return {"Processes": "".join(set([d["PID"]+ " " + d["CMD"] + " " for d in dict_result]))}
        
    def active_users():
        command = subprocess.run(["users"], text=True, stdout=subprocess.PIPE).stdout.replace("\n", "").split(" ")
        unique_users = set(command)
        return {"Users": ", ".join(unique_users)}
        
    def os_info():
        dict_result = {}
        command = subprocess.run(["cat", "/etc/os-release"], text=True, stdout=subprocess.PIPE)
        
        for d in command.stdout.splitlines():
            (key,value) = d.split("=")
            dict_result[key] = value.replace('"', '')

        return {"OS": dict_result["NAME"], "OS_Version":dict_result["VERSION"]} 

    def ip_info():
        command = subprocess.run(["hostname","-I"], text=True, stdout=subprocess.PIPE).stdout.split(" ")
        return {"IP": command}

    def send_data():
        URL = "http://127.0.0.1:5000/inventory"
        data = {**Inventory.ip_info(), **Inventory.os_info(), **Inventory.active_users(),
                **Inventory.processor_info(), **Inventory.processes_info()}
        try:
            post = requests.post(URL,json=data)
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

        return post
    
#### MAIN ####

Inventory.send_data()
