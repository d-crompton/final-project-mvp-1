from tkinter import *


class DeviceInfo:
    def __init__(self, device):
        root = Tk()
        root.title("Device Information")
        root.geometry("300x240")
        root.resizable(0, 0)  # Disables Maximum button
        root.grid_columnconfigure(0, weight=1)
        # Creating Widgets
        frame = Frame(root)
        frame.grid(row=0, column=0, sticky="NSEW")
        title_lbl = Label(frame, text="Device Information").grid(row=0, padx=(10, 5), sticky="WE")
        frame.grid_columnconfigure(0, weight=1)  # Make column fill width
        mac_text = "MAC Address: " + device.get_mac()
        mac_lbl = Label(frame, text=mac_text).grid(row=1, padx=(10, 5), sticky="W")
        ip_text = "IP Address: " + device.get_ip()
        ip_lbl = Label(frame, text=ip_text).grid(row=2, padx=(10, 5), sticky="W")
        manu_text = "Manufacturer: " + device.get_manufacturer()
        manu_lbl = Label(frame, text=manu_text).grid(row=3, padx=(10, 5), sticky="W")
        os_text = "Operating System: " + device.get_os()
        os_lbl = Label(frame, text=os_text, wraplength=270, justify=LEFT).grid(row=4, padx=(10, 5), sticky="W")
        # Add button depending if device is trusted or not
        if device.get_type() == "trusted":
            remove_button = Button(frame, text="Remove from Trusted", bg="#669999",
                                   command=lambda device = device: self.remove_from_trusted(device))
            remove_button.grid(row=5, padx=10, pady=(20, 10), sticky="WE")
        elif device.get_type() == "suspicious":
            remove_button = Button(frame, text="Remove from Suspicious", bg="#669999",
                                   command=lambda device = device: self.remove_from_suspicious(device))
            remove_button.grid(row=5, padx=10, pady=(20, 10), sticky="WE")
        # Return Button
        return_btn = Button(frame, text="Return", bg="#669999", command=root.destroy).grid(row=6, padx=10, sticky="WE")
        root.mainloop()

    # Function to rewrite stored text file, removing current device
    def remove_from_trusted(self, device):
        # Opening file to read and store locally
        try:
            file = open("Files\\trusted.txt", "r")
            original_file = file.readlines()
            file.close()
        except FileNotFoundError:
            print("File unable to open to read")
        # Re-open file in Write mode to override
        try:
            file = open("Files\\trusted.txt", "w+")
        except FileNotFoundError:
            print("File unable to open to write")
        for line in original_file:
            if line.split(',')[0] != device.get_mac():
                print("Writing: " + line)
                file.write(line)
        # Close file at the end
        file.close()
        print("Trusted File Closed")

    def remove_from_suspicious(self, device):
        # Opening file to read and store locally
        try:
            file = open("Files\\suspect.txt", "r")
            original_file = file.readlines()
            file.close()
        except FileNotFoundError:
            print("File unable to open to read")
        # Re-open file in Write mode to override
        try:
            file = open("Files\\suspect.txt", "w+")
        except FileNotFoundError:
            print("File unable to open to write")
        for line in original_file:
            if line.split(',')[0] != device.get_mac():
                print("Writing: " + line)
                file.write(line)
        # Close file at the end
        file.close()
        print("Suspect File Closed")
