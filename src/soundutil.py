import pyaudio
import os

class SoundUtil:

    @staticmethod
    def GetInputDevices():
        #view mics on system
        devices = {}

        p = pyaudio.PyAudio()

        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                devices[p.get_device_info_by_host_api_device_index(0, i).get('name')] = i

        return devices

    @staticmethod
    def EnableJackD2():
        os.system('jack_control start')

    @staticmethod
    def DisableJackD2():
        os.system('jack_control stop')
