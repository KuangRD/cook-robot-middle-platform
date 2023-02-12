from flask_restful import Resource, fields, marshal_with, reqparse
from copy import deepcopy


class Status(Resource):
    def __init__(self, **kwargs):
        self.data = kwargs['data']

    def get(self):
        status = deepcopy(self.data.get_status())
        self.data.clear_qr_scan_data()
        return status
