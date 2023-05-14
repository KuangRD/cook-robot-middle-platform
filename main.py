import threading

from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from apscheduler.schedulers.background import BackgroundScheduler

# from api.v1.wlan import Wifi, Wlan
# from api.v1.status import Status
from api.v1.dish import Dish, Dishes, StarredDishes, DishesCount, StarredDishesCount
from api.v1.ingredient import Ingredients, Shapes
from api.v1.seasoning import Seasonings
from api.v1.command import Command, PLCCommand
from api.v1.running_status import RunningStatus
from api.v1.phone_pairing import PhonePairing
import sys

# from status.system_status import SystemStatus
# from model.system_status_data import SystemStatusData
from packer import StateRequestPacker
from udp_client import command_client, state_client

from sqlite_db import Config, db

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
CORS(app, supports_credentials=True)
api = Api(app)

# systemStatusData = SystemStatusData()
# systemStatus = SystemStatus(systemStatusData)
#
# api.add_resource(Wifi, "/system-settings/wifi/<int:flag>", "/system-settings/wifi")
# api.add_resource(Wlan, "/system-settings/wlan/<int:flag>", "/system-settings/wlan")
api.add_resource(PhonePairing, "/system-settings/phone-pairing/<int:flag>")

# api.add_resource(Status, "/system-status", resource_class_kwargs={"data": systemStatusData})

api.add_resource(Dish, "/dish/", "/dish/<string:dish_id>")
api.add_resource(Dishes, "/dishes/", "/dishes/<string:initials>")
api.add_resource(StarredDishes, "/starred-dishes/", "/starred-dishes/<string:initials>")
api.add_resource(DishesCount, "/dishes-count/", "/dishes-count/<string:initials>")
api.add_resource(StarredDishesCount, "/starred-dishes-count/", "/starred-dishes-count/<string:initials>")

api.add_resource(Ingredients, "/ingredients/")
api.add_resource(Shapes, "/shapes/")
api.add_resource(Seasonings, "/seasonings/")
# api.add_resource(Fires, "/fires/")
# api.add_resource(StirFries, "/stir-fries/")

api.add_resource(Command, "/command")
api.add_resource(PLCCommand, "/plc-command")

api.add_resource(RunningStatus, "/running-status")


if __name__ == "__main__":

    state_request_packer = StateRequestPacker()
    state_request_packer.pack()
    t1 = threading.Thread(target=command_client.run)
    t2 = threading.Thread(target=state_client.run)
    t1.start()
    t2.start()

    apscheduler = BackgroundScheduler()  # 创建调度器
    apscheduler.add_job(state_client.send, args=(state_request_packer.msg,), trigger="interval", seconds=0.5, )
    apscheduler.start()

    # systemStatus.run()

    # tcp_client.run()
    # udp_server.run()

    if sys.platform == "linux":
        # _host = "169.254.216.10"
        # _host = "127.0.0.1"
        _host = "0.0.0.0"
    else:
        # _host = "169.254.70.55"
        # _host = "127.0.0.1"
        _host = "0.0.0.0"
    app.run(host=_host, port=8888, debug=False)
