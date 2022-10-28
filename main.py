# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/

#
# import pyaudio
#
# p = pyaudio.PyAudio()
#
# for ii in range(p.get_device_count()):
#     dev = p.get_device_info_by_index(ii)
#     print(p.get_device_info_by_index(ii).get('name'))
#     print((ii, dev['name'], dev['maxInputChannels']))


import RPi.GPIO as GPIO
from recorder import Recorder
from playback import Playback
import time
import enum


class Estado(enum.Enum):
    Esperando = 1
    Saludo = 2
    Grabando = 3
    Reproduciendo = 4
    Finalizado = 5


buttonPin = 16
estadoActual = Estado.Esperando

recorder = Recorder()
playback = Playback()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    buttonState = GPIO.input(buttonPin)

    if estadoActual == Estado.Esperando:
        if (buttonState == False):
            estadoActual = Estado.Saludo
            time.sleep(2)
            playback.playSaludo(GPIO, buttonPin)

    elif estadoActual == Estado.Saludo:
        if (not playback.isPlay):
            # grabar audio
            if(buttonState == False):
                print("grabar audio")
                estadoActual = Estado.Grabando
                recorder.iniciarGrabacion()
            else:
                estadoActual = Estado.Esperando

    elif estadoActual == Estado.Grabando:
        if (buttonState == False):
            recorder.update()
        else:
            if recorder.isRecording:
                print("finalizando grabacion")
                recorder.stopRecording()
                recorder.writeAudio()
                estadoActual = Estado.Esperando
            else:
                print("esperando.....")

    elif estadoActual == Estado.Reproduciendo:
        if (not playback.isPlay):
            lst = playback.listFiles()
            playback.play(lst[0])

        if (buttonState == True):
            if (playback.isPlay):
                playback.close()
            estadoActual = Estado.Esperando
