from tkinter import *
from Windows import Device_Info_Window
from Device import Device

class SuspiciousDevices:
    # Constructor
    def __init__(self):
        # Opening List File
        self.file = None
        self.devices = []  # Used to store devices locally
        self.open_file()
        # Creating Window
        root = Tk()
        root.title("Suspicious Devices")
        root.geometry("300x350")
        root.resizable(0, 0)  # Disables Maximum button
        root.grid_columnconfigure(0, weight=1)
        # Creating Widgets
        frame = Frame(root)
        frame.grid(row=0, column=0, sticky="NSEW")
        frame.grid_columnconfigure(0, weight=1)  # Make column fill width
        title_lbl = Label(frame, text="Suspicious Devices").grid(row=0, padx=(10, 5), sticky="WE")
        # Frame Devices are entered into
        device_frame = Frame(frame, bg="#f0f0f5", height=260, width=260,
                             highlightbackground="black", highlightthickness=1)
        device_frame.grid(row=1, pady=10, padx=10, sticky="nsew")
        device_frame.grid_columnconfigure(0, weight=1)
        # device_frame.grid_rowconfigure(0, weight=1)
        device_frame.grid_propagate(0)
        row = 0
        for device in self.devices:
            # Creating Device Object
            device_obj = Device(device[1], device[0], device[2], device[3])
            device_obj.set_type("suspicious")
            # Creating Widgets for Device's frame
            inner_frame = Frame(device_frame, bg="#ffb3b3", highlightbackground="black", highlightthickness=1)
            inner_frame.grid(row=row, sticky="WE")
            inner_frame.grid_columnconfigure(0, weight=9)
            inner_frame.grid_columnconfigure(1, weight=1)
            mac_label = Label(inner_frame, text=device_obj.get_mac(), bg="#ffb3b3").grid(row=0, column=0, sticky="W")
            manufacturer_label = Label(inner_frame, text=device_obj.get_manufacturer(), bg="#ffb3b3")
            manufacturer_label.grid(row=1, column=0, sticky="W")
            info_button = Button(inner_frame, text="Info", command=lambda device=device: self.info_button(device_obj))
            info_button.grid(row=0, rowspan=2, column=1, sticky="NSEW")
            row += 1
        return_btn = Button(frame, text="Return", bg="#669999", command=root.destroy).grid(row=2, padx=10, sticky="SWE")

    def open_file(self):
        # Opening File in Read Only
        try:
            self.file = open("Files\\suspect.txt", "r")  # Open in read only
            self.file.seek(0)  # Move marker to top
            for line in self.file:  # Loop through lines
                adj_line = line[:-2]  # Remove the \n from the end
                device = adj_line.split(',')  # Turn into an array
                self.devices.append(device)  # Add to local list of trusted devices
            self.file.close()
            print(self.devices)
        except FileNotFoundError:
            print("Unable to open")

    def info_button(self, device):
        device_info_window = Device_Info_Window.DeviceInfo(device)