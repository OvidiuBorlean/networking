import pathlib
from netmiko import Netmiko
import yaml
import time

def connect(device, host, c_username, c_password, c_delay_factor, c_get_cmd_1, c_get_cmd_2, c_get_cmd_3 ):
        print ("Connecting on {} device with IP address {} with username {} \n".format(device, host, c_username))
        print("Using delay_factor {} and commands: {}, {}, {} \n".format(c_delay_factor, c_get_cmd_1, c_get_cmd_2, c_get_cmd_3))
        connection = Netmiko(host, username= c_username, password = c_password, device_type=device)
        print("Running command 1:\n")
        get_cmd_1 = connection.send_command(c_get_cmd_1, delay_factor = c_delay_factor)
        config_file = open(host,"a")
        config_file.write(get_cmd_1)
        config_file.close()
        if not c_get_cmd_2 == None:
            print("Running command 2 : " + c_get_cmd_2 + "\n")
            get_cmd_2 = connection.send_command(c_get_cmd_2, delay_factor = c_delay_factor)
            config_file = open(host,"a")
            config_file.write(get_cmd_2)
            config_file.close()
            print("Running command 3:\n")
        if not c_get_cmd_3 == None:
            print("Running command 3 : " + c_get_cmd_3 + "\n")
            get_cmd_3 = connection.send_command(c_get_cmd_3, delay_factor = c_delay_factor)
            config_file = open(host,"a")
            config_file.write(get_cmd_3)
            config_file.close()
            time.sleep(2)
        
if __name__ == "__main__":
   
    print("Infomate Automation Tool v0.10 \n")
    config_file = pathlib.Path("netfacts.config")
    hosts_file = pathlib.Path("hosts.db")
    if not hosts_file.exists():
        print("hosts.db file not found")
    
    if config_file.exists ():
        with open('netfacts.config') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if not "device" in data:
                print("device variable not found")
                quit()
            c_device = data["device"]
                
            if not "hostname" in data:
                print("hostname variable not found")
                quit()
            c_hostname = data["hostname"]
                
            if not "password" in data:
                print("password variable not found")
                quit()            
            c_password = data["password"]
                           
            if not "delay_factor" in data:
                print("delay_factor variable not found")
                quit()
            c_delay_factor = data["delay_factor"]
            
            if not "get_cmd_1" in data:
                print("get_cmd_1 variable not found")
                quit()
            c_get_cmd_1 = data["get_cmd_1"]
                
            if not "get_cmd_2" in data:
                print("get_cmd_2 variable not found")
                c_get_cmd_2 = "Null"
            else: 
                c_get_cmd_2 = data["get_cmd_2"]
                
            if not "get_cmd_3" in data:
                print("get_cmd_3 variable not found")
                c_get_cmd_3 = "Null"
            else:
                c_get_cmd_3 = data["get_cmd_3"]
            
            hostsdb = open("hosts.db","r")
            hostline = hostsdb.read()
            host_item = hostline.split("\n")
            for i in host_item:
                print(i)
                connect(c_device, i, c_username, c_password, c_delay_factor, c_get_cmd_1, c_get_cmd_2, c_get_cmd_3)           

