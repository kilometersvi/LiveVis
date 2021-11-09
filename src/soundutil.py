import pyaudio
import os

class SoundUtil:

    def __init__(self):
        self.p = pyaudio.PyAudio()


    def GetInputDevices(self):
        #view mics on system
        devices = []
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                devices.append({'ID':i,'Name':p.get_device_info_by_host_api_device_index(0, i).get('name')})

        return devices

    def EnableJackD2(self):
        os.system('jack_control start')

    def DisableJackD2(self):
        os.system('jack_control stop')
