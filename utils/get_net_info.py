import subprocess
import re


def get_net_info(interface_name):
    output = subprocess.check_output(["ifconfig"])
    pattern = r"{}:.*?inet (\d+\.\d+\.\d+\.\d+).*?ether (\w+:\w+:\w+:\w+:\w+:\w+)".format(interface_name)
    match = re.search(pattern, output.decode(), re.DOTALL)
    if match:
        ip_address = match.group(1)
        mac_address = match.group(2)
        return ip_address, mac_address
    else:
        return None, None
