import wave
import pyaudio
import os


class Playback:
    chunk = 1024
    dirPath = "/home/pi/boda/grabaciones"
    isPlay = False
    #
    # def __init__(self):
    #     self.GPIO = GPIO


    def listFiles(self):
        res = os.listdir(self.dirPath)
        print(res)
        return res

    def play(self, file):
        self.p = pyaudio.PyAudio()
        self.wf = wave.open(self.dirPath + '/' + file, 'rb')
        self.isPlay = True

        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True)

        data = self.wf.readframes(self.chunk)
        while data != b'' and self.isPlay:
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

        if self.isPlay:
            self.close()

    def playSaludo(self,  GPIO, buttonPin):
        self.p = pyaudio.PyAudio()
        self.wf = wave.open('/home/pi/boda/saludo.wav', 'rb')
        self.isPlay = True

        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True)

        data = self.wf.readframes(self.chunk)
        while data != b'' and self.isPlay:
            buttonState = GPIO.input(buttonPin)
            if buttonState:
                break
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

        print("termino saludo")

        if self.isPlay:
            self.close()

    def close(self):
        self.isPlay = False
        self.stream.close()
        self.p.terminate()
