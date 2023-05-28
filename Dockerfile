FROM continuumio/miniconda3

# 将工作目录设置为/app
WORKDIR /app

# 复制当前目录下的环境文件到容器的/app目录下
COPY requirements.txt .

# 创建 Conda 环境
RUN conda create --name middle-platfrom python=3.8

# 激活 Conda 环境
SHELL ["conda", "run", "-n", "middle-platfrom", "/bin/bash", "-c"]

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt
