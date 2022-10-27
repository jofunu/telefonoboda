import pyaudio
import wave
from datetime import datetime

class Recorder:
    form1 = pyaudio.paInt16  # 16-bit resolution
    chans = 1  # 1 channel
    samp_rate = 44100  # 44.1 khz sampling rate
    chunk = 4096  # 2^12 sample for buffer
    # record_secs = 15  # seconds to record
    dev_index = 1  # device index found by p.get_device_info_by_index(ii)
    audio = None
    stream = None
    sample_width = 0
    frames = None
    isRecording = False

    # def __int__(self):
    #     self.audio = pyaudio.PyAudio()


    def iniciarGrabacion(self):
        self.audio = pyaudio.PyAudio()
        print(self.chans)
        self.stream = self.audio.open(format=self.form1, rate=self.samp_rate, channels=self.chans,
                                      input_device_index=self.dev_index, input=True,
                                      frames_per_buffer=self.chunk)

        self.frames = []
        self.isRecording = True
        # for ii in range(0, int((self.samp_rate / self.chunk) * self.record_secs)):
        #     data = self.stream.read(self.chunk)
        #     self.frames.append(data)
        #
        # self.stream.stop_stream()
        # self.stream.close()
        # self.audio.terminate()

    def update(self):
        data = self.stream.read(self.chunk)
        self.frames.append(data)

    def stopRecording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.isRecording = False

    def writeAudio(self):
        today = datetime.today()
        filename = "/home/pi/boda/grabaciones/"+today.strftime('%d-%m-%Y %H:%M:%S') + ".wav"
        wavefile = wave.open(filename, 'wb')
        wavefile.setnchannels(self.chans)
        wavefile.setsampwidth(self.audio.get_sample_size(self.form1))
        wavefile.setframerate(self.samp_rate)
        wavefile.writeframes(b''.join(self.frames))
        wavefile.close()