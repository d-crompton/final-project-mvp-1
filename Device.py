# Device Class used to store device details


class Device:
    # Constructor for devices that do not have a user given name
    # Empty Device
    def __init__(self, ip, mac, manufacturer, os):
        self.ip = ip
        self.mac = mac
        self.manufacturer = manufacturer
        self.os = os
        self.type = None # Whether device is "trusted" or "suspicious"
        self.name = None

    # Setters
    def set_ip(self, ip):
        self.ip = ip

    def set_mac(self, mac):
        self.mac = mac

    def set_manufacturer(self, manufacturer):
        self.manufacturer = manufacturer

    def set_os(self, os):
        self.os = os

    def set_type(self, type):
        self.type = type

    # Getters
    def get_ip(self):
        return self.ip

    def get_mac(self):
        return self.mac

    def get_manufacturer(self):
        return self.manufacturer

    def get_os(self):
        return self.os

    def get_type(self):
        return self.type