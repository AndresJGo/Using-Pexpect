from pexpect import pxssh
import getpass
import sys


devices = {"lax-edg-r1" : {"ip": "192.168.122.68"}, "lax-edg-r2" : {"ip" : "192.168.122.49"}}

commands = ["show version", "show ip interface brief", "show running-config"]

username = input("Ingresa tu nombre de usuario: ")
password = getpass.getpass("Contraseña: ")

for device in devices.keys():
    outputFileName = device + "_output.txt"

    devicePrompt = device + r"[>#]"

    child = pxssh.pxssh()
    child.login(devices[device]["ip"], username.strip(), password.strip(), auto_prompt_reset = False)
    child.sendline("terminal length 0")
    child.expect(devicePrompt)
    child.sendline("enable")
    child.expect(devicePrompt)

    with open(outputFileName, "wb") as f:
        for command in commands:
            child.sendline(command)
            child.expect(devicePrompt)
            f.write(child.before)
    
    child.logout()






