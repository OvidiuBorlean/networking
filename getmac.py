import json

import scapy.all as scapy

def mac_find(mac_address):
    with open ("macaddress.io-db.json","r", encoding = "utf8") as macs:
        for i in macs:
           #print(i)
           data = json.loads(i)
           #print(data["oui"])
           #print(mac_address)
           if data["oui"] == mac_address:
               print(data["companyName"])
               return data["companyName"]
           
           #print (json.dumps(data, indent = 4))
           #print(data["companyName"])
           #if "Ubiq" in data["companyName"]:
           #    print(data["oui"] )




def scan(ip):
   arp_request = scapy.ARP(pdst=ip)
   broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
   arp_request_broadcast = broadcast/arp_request
   mac_db = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)[0]
   #print(mac_db.summary())
   for element in mac_db:
       hostmac = str(element[1].hwsrc)
       if hostmac == "96:01:40:f6:2a:b7":
          print("NOROCOSULE")
       newhostmac = hostmac[0:8]
       uppermac = newhostmac.upper()
       #print("->" + uppermac)
       
       mac_return = mac_find(uppermac)
       print(element[1].psrc + "\t\t" + element[1].hwsrc + "\t\t")
       print('----------------------------------------------------')

               
               
scan("192.168.10.0/24")
