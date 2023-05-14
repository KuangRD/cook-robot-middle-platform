import subprocess
import re

def get_interface_info(interface_name):
    # 运行ipconfig命令获取网络接口信息
    output = subprocess.check_output(["ipconfig", "/all"])
    print(output)

    # 提取指定接口的信息
    pattern = r"(?s)({}\s.*?)\n\n".format(interface_name)
    match = re.search(pattern, output.decode())

    if match:
        interface_info = match.group(1)
        return interface_info.strip()
    else:
        return None

# 指定要获取信息的接口名称
interface_name = "Ethernet"  # 替换为您要查询的接口名称

# 获取指定接口的信息
interface_info = get_interface_info(interface_name)

if interface_info:
    print("Interface Info for {}: \n{}".format(interface_name, interface_info))
else:
    print("No interface information found for {}".format(interface_name))