from flask_restful import Resource, reqparse
from udp_client import udp_command_client
from packer import CommandPacker, InquiryPacker, PLCCommandPacker


class Command(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'command',
            type=dict,
            location='json',
        )

    def post(self):
        res = {"success": False}
        args = self.parser.parse_args()
        command = args.get("command")
        print(command)
        command_packer = CommandPacker()
        # inquiry_packer = InquiryPacker()

        try:
            command_packer.pack(command)
            # inquiry_packer.pack(b"\x01")
        except Exception as e:
            print(e)
            return res
        # inquiry_result = udp_command_client.send(inquiry_packer.msg)
        # if not inquiry_result:
        #     return res

        command_result = udp_command_client.send(command_packer.msg)
        if not command_result:
            return res

        res["success"] = True

        return res


class PLCCommand(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'command',
            type=dict,
            location='json',
        )

    def post(self):
        res = {"success": False}
        args = self.parser.parse_args()
        command = args.get("command")
        print(command)
        plc_command_packer = PLCCommandPacker()
        try:
            plc_command_packer.pack(command)
        except Exception as e:
            print(e)
            return res
        # command_packer = CommandPacker()
        # inquiry_packer = InquiryPacker()
        #
        # try:
        #     command_packer.pack(command)
        #     inquiry_packer.pack(b"\x01")
        # except Exception as e:
        #     print(e)
        #     return res
        # inquiry_result = udp_command_client.send(inquiry_packer.msg)
        # if not inquiry_result:
        #     return res
        #
        command_result = udp_command_client.send(plc_command_packer.msg)
        if not command_result:
            return res

        res["success"] = True

        return res
