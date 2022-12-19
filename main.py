from tkinter import *
from tkinter import ttk
import win32com.client

wmi = win32com.client.GetObject("winmgmts:")
for usb in wmi.InstancesOf("Win32_PnPEntity"):
    print(usb.Name + ' >> ' + usb.PNPClass)


class App(Tk):
    def __init__(self):
        super().__init__()

        self.setUI()

        self.title('USB-IP connecting')
        self.resizable(False, False)
        self.attributes('-toolwindow', True)

    def setUI(self):
        frame_top = Frame()
        frame_middle = Frame()
        frame_bootom = Frame()
        self.lblHost = ttk.Label(frame_top, text='Host:')
        self.cmbHost = ttk.Combobox(frame_top)
        self.lstDevices = Listbox(frame_middle, width=30, height=5)
        self.btnConnect = ttk.Button(frame_bootom, text='Connect')
        self.btnDisconnect = ttk.Button(frame_bootom, text='Disconnect')
        frame_top.pack()
        frame_middle.pack(expand=True, fill=BOTH)
        frame_bootom.pack()
        self.lblHost.pack(side=LEFT, )
        self.cmbHost.pack(side=LEFT, fill=X)
        self.lstDevices.pack(side=LEFT, expand=True, fill=BOTH)
        self.btnConnect.pack(side=LEFT)
        self.btnDisconnect.pack(side=LEFT)


# import subprocess, json
#
# out = subprocess.getoutput("PowerShell -Command \"& {Get-PnpDevice | Select-Object Status,Class,FriendlyName,InstanceId | ConvertTo-Json}\"")
# j = json.loads(out)
# for dev in j:
#     print(dev['Status'], dev['Class'], dev['FriendlyName'], dev['InstanceId'] )


App().mainloop()
