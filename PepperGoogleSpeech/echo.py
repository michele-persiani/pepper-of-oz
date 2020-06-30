# -*- coding: utf-8 -*-
from microphone import PepperMicrophone
from utterance import Utterance
from asr import GoogleASR
import Settings
from threading import Thread
from time import sleep
import qi
import os


class EchoTest():
    def __init__(self):


        self.session = qi.Session()
        try:
            self.session.connect("tcp://"+Settings.ROBOT_IP+":"+str(Settings.PORT))
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"130.239.182.9\" on port 9559.\n"
                   "Please check your script arguments. Run with -h option for help.")

        self.speech = self.session.service("ALAnimatedSpeech")

        #self.microphone = SystemMicrophone(16000, 1)
        self.microphone = PepperMicrophone(self.session)
        self.utterance = Utterance(self.microphone, self.on_utterance)
        self.recognition = GoogleASR()

        self.utterance.start()

        Thread(target=self.voice_activation).start()

        print("\nBooted Echo App")

    def voice_activation(self):
        while True:
            value = float(self.utterance.activation())
            #self.led.set((value if value > self.utterance.VOICE_THRESHOLD else 0, 0, value))
            #print('voice activation:'+str(value))
            sleep(0.2)

    def on_utterance(self, audio):

        hypotheses = self.recognition.transcribe(audio)

        if hypotheses:
            transcript, confidence = hypotheses[0]
            print(transcript+" [{:3.0%}]".format(confidence))
            self.say(transcript)

    def say(self, text):
        self.utterance.stop()
        self.speech.say(text)
        self.utterance.start()


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/michele/Development/PycharmProjects/Pepper_Of_Oz/speech-key.json"
    print(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    app = EchoTest()
