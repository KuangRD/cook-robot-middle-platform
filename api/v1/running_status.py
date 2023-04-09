from flask_restful import Resource, reqparse
from udp_client import plc_state


class RunningStatus(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'command',
            type=dict,
            location='json',
        )

    def get(self):
        res = {
            "success": True,
            "data": plc_state
        }

        return res
