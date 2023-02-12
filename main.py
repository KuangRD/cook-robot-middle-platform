from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from api.v1.wifi import Wifi, Wlan
from api.v1.status import Status
import sys

from status.system_status import SystemStatus

from model.system_status_data import SystemStatusData

app = Flask(__name__)
CORS(app, supports_credentials=True)

systemStatusData = SystemStatusData()

api = Api(app)

api.add_resource(Wifi, "/system-settings/wifi/<int:flag>", "/system-settings/wifi")
api.add_resource(Wlan, "/system-settings/wlan/<int:flag>", "/system-settings/wlan")
api.add_resource(Status, "/system-status", resource_class_kwargs={"data": systemStatusData})

if __name__ == "__main__":
    systemStatus = SystemStatus(systemStatusData)
    systemStatus.run()

    if sys.platform == "linux":
        _host = "169.254.216.10"
        # _host = "127.0.0.1"
    else:
        _host = "127.0.0.1"
    app.run(host=_host, port=8888, debug=False)
