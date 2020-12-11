from tkinter import *
import tkinter.messagebox
import nmap
import os
from Device import Device
from Windows import Device_Info_Window, Trusted_Window, Suspicious_Window


class Main:
    def __init__(self):
        # Opening Device List Files
        self.trust_file = None  # Declaring class variables
        self.sus_file = None
        # Creating Arrays to store previously saved devices
        self.trusted_devices = []
        self.suspect_devices = []
        self.open_files()
        # Creating Root Window
        root = Tk()
        root.title("Network Device Scanner")
        root.geometry("500x450")
        root.resizable(0, 0)  # Disables Maximum button
        # root_bg = "#4d4d4d"  # Background Colour
        # root.configure(background=root_bg)  # Setting root bg
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        # Adding Elements
        button_bg = "#669999"  # - Was "#669999"
        title_lbl = Label(root, text="Network Device Scanner").grid(row=0, columnspan=2, pady=(0, 5))
        scan_btn = Button(root, text="Scan Network", width=50, padx=5, pady=5, bg=button_bg,
                          command=self.scan_button)
        scan_btn.grid(row=1, columnspan=2)
        self.device_frame = Frame(root, bg="#f0f0f5", height=300, width=450,  # Bg was #f0f0f5
                                  highlightbackground="black", highlightthickness=1)
        self.device_frame.grid(row=2, columnspan=2, pady=10, padx=10, sticky="nsew")  # dev_frame's pos on root window
        # Setting initial weighting
        self.device_frame.grid_columnconfigure(0, weight=1)
        self.device_frame.grid_columnconfigure(0, weight=1)
        self.device_frame.grid_propagate(0)  # Prevent children re-shaping
        # Buttons at bottom
        trusted_btn = Button(root, text="Trusted Devices", width=30, pady=5, bg=button_bg,
                             command=self.trusted_window)
        trusted_btn.grid(row=3)
        suspect_btn = Button(root, text="Suspicious Devices", width=30, pady=5, bg=button_bg,
                             command=self.suspicious_window)
        suspect_btn.grid(row=3, column=1)
        # No code after this
        root.mainloop()

    # Additional Functions
    # Function to open two files for trusted and suspect devices
    def open_files(self):
        # Trust File
        try:
            # Attempt to open in append, if file exists
            self.trust_file = open("Files\\trusted.txt", "a+")
            # If file appears, locally store devices
            self.trust_file.seek(0)  # Puts marker at the start of the file
            for line in self.trust_file:  # Loop through file's lines
                adj_line = line[:-2]  # Remove the \n from the end
                device = adj_line.split(',') # Turn into an array
                self.trusted_devices.append(device) # Add to local list of trusted devices
        except FileNotFoundError:
            # Open in write mode to create file, if not
            self.trust_file = open("Files\\trusted.txt", "w+")
        # Suspect File
        try:
            # Attempt to open in append, if file exists
            self.sus_file = open("Files\\suspect.txt", "a+")
            # If file appears, locally store devices
            self.sus_file.seek(0) # Puts marker at start of file
            for line in self.sus_file:
                adj_line = line[:-2]
                device = adj_line.split(',')
                self.suspect_devices.append(device)
        except FileNotFoundError:
            # Open in write mode to create file, if not
            self.sus_file = open("Files\\suspect.txt", "w+")

    # Function that runs when the scan button is pressed
    def scan_button(self):
        # Check if files had been closed previously
        if self.trust_file.closed:
            self.open_files()
        # Run code to remove devices currently in frame (loop through devices, destroy)
        for child in self.device_frame.winfo_children():
            child.destroy()
        # Run Quick Scan to get available hosts
        nm = nmap.PortScanner()
        quick_scan = nm.scan(hosts='192.168.0.1/24', arguments='-F')
        row = 0
        hosts = nm.all_hosts()
        for host in hosts:
            # OS Scan
            os_scan = nm.scan(hosts=host, arguments='-O -F')
            # Try Getting Mac
            try:
                mac = os_scan['scan'][host]['addresses']['mac']
            except KeyError:  # Error if the dictionary key is not available
                mac = "Mac Address not Available"
            # Try Getting Manufacturer
            try:
                manu = os_scan['scan'][host]['vendor'][mac]
            except KeyError:
                manu = "Manufacturer not Available"
            # Try Getting OS
            try:
                op_sys = os_scan['scan'][host]['osmatch'][0]['name']
            except KeyError:
                op_sys = "OS not Available"
            except IndexError:
                op_sys = "OS not Available"
            # Creating Device Object
            curr_device = Device(host, mac, manu, op_sys)
            print("Current MAC" + curr_device.get_mac())
            # Checking if device is already known
            device_known = False
            # Checking Trusted Devices List
            for device in self.trusted_devices:
                if curr_device.get_mac() == device[0]:
                    print(curr_device.get_mac() + " is trusted")
                    curr_device.set_type("trusted")
                    frame_bg = '#adebad'  # Turn Device's frame background green
                    device_known = True
                    break  # Exit loop, unnecessary to loop any more
            # Checking Suspected Devices List - Only run if device_known is false
            if not device_known:
                for device in self.suspect_devices:
                    if curr_device.get_mac() == device[0]:
                        curr_device.set_type("suspicious")
                        print(curr_device.get_mac() + " is suspicious")
                        # Show message box alerting User
                        tkinter.messagebox.showwarning("Suspicious Device Found",
                                                       "A Device that was flagged previously as suspicious is on " +
                                                       "the network")
                        frame_bg = "#ffb3b3"
                        device_known = True
                        break
            # If device isn't known run code
            if not device_known:
                # Creating Pop-Up asking User if they trust device
                pop_message = "Do you trust this device:\n" +\
                              "MAC Address: " + curr_device.get_mac() + "\n" +\
                              "IP Address: " + curr_device.get_ip() + "\n" +\
                              "Manufacturer: " + curr_device.get_manufacturer() + "\n" +\
                              "OS: " + curr_device.get_os()
                user_input = tkinter.messagebox.askquestion("New Device Found", pop_message)
                if user_input == "yes":
                    curr_device.set_type("trusted")
                    self.trust_file.write(curr_device.get_mac() + "," + host + "," + curr_device.get_manufacturer()
                                          + "," + curr_device.get_os() + "\n")
                    self.trust_file.flush()
                    frame_bg = "#adebad"  # If User answers yes, frame bg is green
                elif user_input == "no":
                    curr_device.set_type("suspicious")
                    self.sus_file.write(curr_device.get_mac() + "," + host + "," + curr_device.get_manufacturer()
                                        + "," + curr_device.get_os() + "\n")
                    self.sus_file.flush()
                    frame_bg = "#ffb3b3"  # If User answers no, frame bg is red
            # Creating Frame for device
            frame = Frame(self.device_frame, bg=frame_bg, highlightbackground="black", highlightthickness=1)
            frame.grid(row=row, sticky="WE")  # "WE" stretches the frames
            # Elements inside this frame
            host_lbl = Label(frame, text=host, bg=frame_bg).grid(row=0, column=0, sticky="W")
            manu_lbl = Label(frame, text=op_sys, bg=frame_bg).grid(row=1, column=0, sticky="W")
            frame.grid_columnconfigure(0, weight=9)
            frame.grid_columnconfigure(1, weight=1)
            info_btn = Button(frame, text="Info",
                              command=lambda curr_device = curr_device: self.info_button(curr_device))
            info_btn.grid(row=0, column=1, rowspan=2, padx=2, pady=5, sticky="NESW")
            row += 1
        # Close Files after loop finishes
        tkinter.messagebox.showinfo("Scan Finished", "Scan Finished") # Message to let User know scan loop has ended
        # Closing Trust file
        self.trust_file.flush()  # Flush and fsync, writes lists without waiting for buffer
        os.fsync(self.trust_file.fileno())
        self.trust_file.close()
        # Closing Sus file
        self.sus_file.flush()
        os.fsync(self.sus_file.fileno())
        self.sus_file.close()

    # Button Functions - Opening Other Windows
    def info_button(self, device):
        device_info_window = Device_Info_Window.DeviceInfo(device)

    def trusted_window(self):
        trusted_window = Trusted_Window.TrustedDevices()

    def suspicious_window(self):
        suspicious_window = Suspicious_Window.SuspiciousDevices()