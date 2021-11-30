from dotenv import load_dotenv
from mainview import MainWindow
#from soundutil import SoundUtil

if __name__ == "__main__":
    load_dotenv()
    #SoundUtil.EnableJackD2()

    w = MainWindow()
