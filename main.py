from concurrent.futures import ThreadPoolExecutor
from mcstatus import JavaServer
import enum
import re
from colorama import Fore, Back, Style
from termcolor import colored, cprint
import json
from pyfiglet import figlet_format
import pyfiglet
import codecs

# Printing functions
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

# Minecraft server status related functions
class JavaStatusPlayer:
    def __init__(self, name, id):
        self.name = name
        self.id = id

def fixymotd(motd_obj):
    parsed_data = motd_obj.parsed

    result = []
    for item in parsed_data:
        if isinstance(item, str):
            result.append(item.replace('\n', ' '))
        elif isinstance(item, tuple) and len(item) == 2 and isinstance(item[1], str):
            result.append(item[1].replace('\n', ' '))

    return ''.join(result).strip().replace("@", "_")

def fixyversion(ver):
    pattern = r"name='(.*?)'"
    match = re.search(pattern, ver)
    if match:
        version = match.group(1)
        return version
    else:
        return "idk."

def fixyplayers(input_string):
    match = re.match(r"JavaStatusPlayers\(online=(\d+), max=(\d+), sample=(\[.*\])\)", input_string)

    if match:
        online = match.group(1)
        max_players = match.group(2)
        sample = match.group(3)
        
        try:
            sample_list = eval(sample)
            if isinstance(sample_list, list) and all(isinstance(player, JavaStatusPlayer) for player in sample_list):
                online = len(sample_list)
        except:
            pass

        return f"{online}/{max_players}"
    else:
        match = re.match(r"JavaStatusPlayers\(online=(\d+), max=(\d+), sample=None\)", input_string)
        if match:
            online = match.group(1)
            max_players = match.group(2)
            return f"{online}/{max_players}"
        else:
            return "Invalid input format"

def getinfo(ip):
    try:
        server = JavaServer.lookup(ip)
        status = server.status()

        server_info = {
            'ip': ip,
            'version': fixyversion(str(status.version)),
            'latency': f"{round(status.latency)}ms",
            'onlineplayers': fixyplayers(str(status.players)),
            'motd': fixymotd(status.motd),
        }

        json_object = json.dumps(server_info, indent=4)
        return json_object

    except:
        return f"No server running on {ip}..."

def start():
    prYellow(figlet_format("Server Scanner", font="big"))

def process_server(ip, counter):
    try:
        print("")
        prCyan(f"({counter}) Pinging {ip}...")
        server_info = getinfo(ip.strip())
        if "No server running on" in server_info:
            prRed(server_info.replace("...", ""))
        else:
            prGreen("Server responded")
            data = json.loads(server_info)
            return data
    except Exception as e:
        print(f"An error occurred for {ip}: {e}")
        return None

file_path = "ips.txt"
server_data = []

try:
    with open(file_path, 'r') as file:
        ips = [line.strip() for line in file]

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_server, ips, range(1, len(ips) + 1)))

    server_data = [data for data in results if data is not None]

except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

with open('results.json', 'a') as f:
    json.dump(server_data, f, indent=4)
