from zeroconf import Zeroconf, ServiceInfo

service_type = "_http._tcp.local."
service_name = "MyService"
port = 9999


class MDnsService:
    def __init__(self):
        self.m_dns = Zeroconf()
        self.service_info = ServiceInfo(service_type, service_name + "." + service_type, port=port, properties={})

    def start(self):
        self.m_dns.register_service(self.service_info)

    def pause(self):
        self.m_dns.unregister_service(self.service_info)


mDnsService = MDnsService()
