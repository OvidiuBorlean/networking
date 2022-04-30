import pathlib
from netmiko import Netmiko
import yaml
import time
from datetime import datetime


def connect(host, username, password, device_type, secret):
        date_time = now.strftime("%d-%m-%Y_%H:%M")   
        #print(c_report)
        connection = Netmiko(host, username= c_username, password = c_password, device_type=c_device, secret = c_secret)
        print("Starting Up The Precheck Commands \n")
        outfile = open(c_report, 'a')
        for pre_cmds in data["precheck"]:
            print ("Executing Pre-Check Statement : ---> " + pre_cmds + "\n")
            detect_prompt = connection.find_prompt()
            print(detect_prompt)
            if ">" in detect_prompt:
                print("Device in Operational Mode. Switching to Enable Mode")
                detect_prompt = connection.enable()
            precheck_task = connection.send_command(pre_cmds)
            outfile.write(host + date_time)
            outfile.write(precheck_task)
            print(precheck_task)
        print("Finished Precheck Statement : ---> " + pre_cmds + "\n")       
        time.sleep(2)
        print("Finished Precheck Tasks \n")
        time.sleep(5)
        
   ################################# CONFIG ###############################     
        
        print ("Executing Config Statements : ---> \n")
        detect_prompt = connection.find_prompt()
        print(detect_prompt)
        if ">" in detect_prompt:
            print("Device in Operational Mode. Switching to Enable Mode")
            detect_prompt = connection.enable()
            print(detect_prompt)
            prompt = connection.find_prompt()
            print(prompt)
        config_task = connection.send_config_set(config_commands= data["config"], exit_config_mode=True, delay_factor=1, max_loops=150, strip_prompt=False, strip_command=False, config_mode_command=None, cmd_verify=True, enter_config_mode=True)
        outfile.write(config_task)
        print(config_task)
        time.sleep(5)
        
        for post_cmds in data["postcheck"]:
            print ("Executing Post-Check Statement : ---> " + post_cmds + "\n")
            detect_prompt = connection.find_prompt()
            print(detect_prompt)
            if ">" in detect_prompt:
                print("Device in Operational Mode. Switching to Enable Mode")
                detect_prompt = connection.enable()
            postcheck_task = connection.send_command(post_cmds)
            print("--------------------------------------------------------------\n")
            outfile.write(postcheck_task)
            print(postcheck_task)
            print ("Finished Post-Check Statement : ---> " + post_cmds + "\n")
        time.sleep(2)
        outfile.close()
       
        
        print("\n")
        print("Done")



if __name__ == "__main__":
    now = datetime.now()
    print("Infomate Automation Tool v2.0 \n")
   
    #config_file = pathlib.Path("infomate-v2.yaml")
    hosts_file = pathlib.Path("hosts.yaml")
    if not hosts_file.exists ():
        print ("Hosts Database is not present. Please check the configuration.")
    else:
        with open('hosts.yaml') as f_hosts:
            hosts = yaml.load(f_hosts, Loader=yaml.FullLoader)
            #print(type(hosts))
            for host_ip, host_config in hosts.items():
                #print(host_ip)
                #print(host_config)
                c_hostname = host_ip    
                config_file = pathlib.Path(host_config)
                with open(host_config) as f:
                    data = yaml.load(f, Loader=yaml.FullLoader)
                    #print(data)
                    print("\n")
                    '''
                    Code
                    '''
                    if "device" in data:
                        c_device = data["device"]
                    if "c_username" in data:
                        c_username = data["c_username"]
                        #print("Username: " + c_username)
                    if "c_password" in data:
                        c_password = data["c_password"]
                        #print("Password: <hidden>")
                    if "c_secret" in data:
                        c_secret = data["c_secret"]
                        #print("Secret: <hidden>")
                    if "c_report" in data:
                        c_report = data["c_report"]
                        #print("Secret: <hidden>")
                connect (c_hostname, c_username, c_password, c_device, c_secret)
                
