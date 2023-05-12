#!/bin/bash

# 添加第一个脚本
lxterminal --command="/home/xupc/Desktop/init_controller.sh" &

# 添加第二个脚本
lxterminal --command="/home/xupc/Desktop/init_server.sh" &

# 添加第三个脚本
lxterminal --command="/home/xupc/Desktop/init_ui_new.sh" &
