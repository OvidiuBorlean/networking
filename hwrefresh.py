from __future__ import absolute_import, division, print_function
import netmiko
import time
import yaml
import requests
import pathlib

configuration = []
print("Cisco 9300 ZeroTouchConfiguration v0.1\n")
configuration_file = pathlib.Path("config.yaml")
if not configuration_file.exists ():
        print (
                '''
        Fisierul de configuratie nu a fost gasit. Va rog creati un fisier denumit "config.yaml" avand urmatoarea structura: \n
        Serial : COM7   # Portul serial asignat de sistemul de operare
        Prompt : Switch # Prompt-ul de definire a configuratiei factory-default
        Server : 10.10.10.1 # URL sau Adresa IP a serverului de unde se va descarca configuratia
        \n
        ''')
        exit()

with open("config.yaml") as config_file:
        config_items = yaml.load(config_file, Loader=yaml.FullLoader)
        print("Au fost identificate urmatoarele configuratii: \n")
        print(config_items["Serial"] + "\n")
        print(config_items["Prompt"] + "\n")
        print(config_items["Server"] + "\n") 

device = {
"device_type": "cisco_ios_serial",
"username": None,
"password": "",
"secret": None,
"serial_settings": {"port": config_items["Serial"]}
}

conn = netmiko.ConnectHandler(**device, global_delay_factor = 3)
prompt = conn.find_prompt()
if not config_items["Prompt"] in prompt:
        print ("Device not in Factory Default. Now will exit")
        exit()
else:
        
        enable_prompt = conn.find_prompt()
        if not "#" in enable_prompt:
                enable_prompt = conn.find_prompt()
                conn.enable()
                enable_prompt_cfg = conn.find_prompt()
                print(enable_prompt_cfg)
                get_sn = conn.send_command(" show version | inc System Serial Number")
                sn = get_sn.split(":")
                device_sn = sn[1][1:]
                print(device_sn)
                url = config_items["Server"] + "/" + device_sn
                print(url)
                try:
                        print("Trying to find configuration file in the Cloud")
                        r = requests.get(url, allow_redirects = True)
                        open(device_sn,"wb").write(r.content) 
                        with open(device_sn, "r") as f:
                                config = f.read().splitlines()
                                for i in config:
                                        output = conn.send_config_set(config_commands = i, exit_config_mode=False,cmd_verify=True)
                                        print(output)
                except:
                        print("Configuration file was not found on the server. Trying local file >\n")
                        with open(device_sn, "r") as f:
                                config = f.read().splitlines()
                                for i in config:
                                        output = conn.send_config_set(config_commands = i, exit_config_mode=False,cmd_verify=True)
                                        print(output)
        

        
        conn.disconnect()
