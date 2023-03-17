from flask import Flask
from flask_cors import CORS
from flask_restful import Api

# from api.v1.wlan import Wifi, Wlan
# from api.v1.status import Status
from api.v1.dish import Dish, Dishes, StarredDishes, DishesCount, StarredDishesCount
from api.v1.ingredient import Ingredients, Shapes
from api.v1.seasoning import Seasonings
from api.v1.fire import Fires
from api.v1.stir_fry import StirFries
from api.v1.command import Command,PLCCommand
from api.v1.running_status import RunningStatus
import sys

# from status.system_status import SystemStatus
# from model.system_status_data import SystemStatusData

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
# api.add_resource(Status, "/system-status", resource_class_kwargs={"data": systemStatusData})

api.add_resource(Dish, "/dish/", "/dish/<string:dish_id>")
api.add_resource(Dishes, "/dishes/", "/dishes/<string:initials>")
api.add_resource(StarredDishes, "/starred-dishes/", "/starred-dishes/<string:initials>")
api.add_resource(DishesCount, "/dishes-count/", "/dishes-count/<string:initials>")
api.add_resource(StarredDishesCount, "/starred-dishes-count/", "/starred-dishes-count/<string:initials>")

api.add_resource(Ingredients, "/ingredients/")
api.add_resource(Shapes, "/shapes/")
api.add_resource(Seasonings, "/seasonings/")
api.add_resource(Fires, "/fires/")
api.add_resource(StirFries, "/stir-fries/")

api.add_resource(Command, "/command")
api.add_resource(PLCCommand, "/plc-command")

api.add_resource(RunningStatus, "/running-status")

if __name__ == "__main__":
    # systemStatus.run()

    # tcp_client.run()
    # udp_server.run()

    if sys.platform == "linux":
        # _host = "169.254.216.10"
        _host = "127.0.0.1"
    else:
        # _host = "169.254.70.55"
        _host = "169.254.216.164"
    # _host = "127.0.0.1"
    app.run(host=_host, port=8888, debug=True)
