import paramiko, json, time, re

commands = []
MAX_BUFFER = 65535

def clearBuffer(connection):

    time.sleep(2)

    outputBytes = b""

    while connection.recv_ready():
        outputBytes += connection.recv(MAX_BUFFER)
        time.sleep(0.5)
    
    if not outputBytes:
        return ""
    
    return outputBytes.decode("utf-8", errors = "ignore")
    
def clean_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


with open("paramikoDevices.json", "r") as file:
    devices = json.load(file)

with open("paramikoCommands.txt") as file2:
    for line in file2:
        commands.append(line)

for device in devices:

    outputFileName = device + "_Paramiko_output.txt"

    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(devices[device]["ip"], username = "cisco", password = "cisco", look_for_keys = False, allow_agent = False)

    new_connection = connection.invoke_shell()

    time.sleep(3)

    output = clearBuffer(new_connection)

    new_connection.send("enable\n")
    new_connection.send("terminal length 0\n")

    time.sleep(1)

    output = clearBuffer(new_connection)

    with open(outputFileName, "w", encoding = "utf-8") as outputFile:
        for command in commands:

            new_connection.send(command)

            time.sleep(1)

            rawOutput = clearBuffer(new_connection)

            cleanOutput = clean_ansi(rawOutput)

            outputFile.write(cleanOutput)
    
    new_connection.close()


