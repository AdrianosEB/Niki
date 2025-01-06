# Used OpenAI's API for GPT-4 model for code

import pvporcupine
import struct
import wave
from pvrecorder import PvRecorder
from dotenv import load_dotenv
import pvcobra
import os
import sys
from threading import Thread
from enum import Enum
import time
from pydub import AudioSegment
import uuid
import requests
from gtts import gTTS
import pyaudio
# from audioFX.Fx import Fx
# from librosa import load
# import soundfile
import serial

load_dotenv()

# Import API from OPEN AI
picovoice_api_key = os.getenv("PICOVOICE_ACCESS_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Conect to devices
arduino_eyes_port = os.getenv("ARDUINO_EYES_PORT")
arduino_mouth_port = os.getenv("ARDUINO_MOUTH_PORT")
arduino_boddy_port = os.getenv("ARDUINO_BODDY_PORT")

arduino_righthand_port = os.getenv("ARDUINO_RIGHTHAND_PORT")
arduino_lefthand_port = os.getenv("ARDUINO_LEFTHAND_PORT")

selected_mic_device_index = int(os.getenv("SELECTED_MIC_DEVICE_INDEX"))

recording_dir = "./recordings/"
tts_dir = "./tts/"
keyword_paths = ["./wake_word/hey-nikki_en_windows_v3_0_0/hey-nikki_en_windows_v3_0_0.ppn"]

eyes_arduino = serial.Serial(port=arduino_eyes_port, baudrate=9600, timeout=.1)
mouth_arduino = serial.Serial(port=arduino_mouth_port, baudrate=9600, timeout=.1)
boddy_arduino = serial.Serial(port=arduino_boddy_port, baudrate=9600, timeout=.1)

righthand_arduino = serial.Serial(port=arduino_righthand_port, baudrate=9600, timeout=.1)
arduino_lefthand = serial.Serial(port=arduino_lefthand_port, baudrate=9600, timeout=.1)

class RobotState(Enum):
    INIT = 0
    IDLE = 1
    LISTENING = 2
    PROCESSING = 3
    TALKING = 4
    COMPLETE = 5

robot_state = RobotState.INIT
request_uuid = uuid.uuid4()
dialog = []


# Control all of Niki
#def write_righthand(x):
#     righthand_arduino.write(bytes(str(x), 'utf-8'))
def write_lefthand(x):
    arduino_lefthand.write(bytes(str(x), 'utf-8'))
def write_boddy(x):
    boddy_arduino.write(bytes(str(x), 'utf-8'))
   # print(" boddy =  " , x)
def write_head(x):
    mouth_arduino.write(bytes(str(x), 'utf-8'))
   # print(" head =  " , x)
def write_eyes(x):
    #print(x)
    #print(" eyes =  ", x)
    eyes_arduino.write(bytes(str(x), 'utf-8'))
    # time.sleep(0.05)
def write_righthand(x):
    righthand_arduino.write(bytes(str(x), 'utf-8'))


# Control Niki's mouth with a natural effect
def write_mouth(x):
    #print(" mouth x = ", bytes(str(x), 'utf-8'))
    if x < 99 :
        xx = "A"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
    elif x >= 100 and x < 199 :
        xx = "B"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
    elif x >= 200 and x < 299 :
        xx = "C"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
    elif x >= 200 and x < 299 :
        xx = "D"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
    elif x >= 300 and x < 399 :
        xx = "E"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
    elif x >= 400 and x < 499 :
        xx = "F"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
    elif x >= 500 and x < 599 :
        xx = "G"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
    elif x >= 600 and x < 999 :
        xx = "H"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
    elif x >= 1000 and x < 1399 :
        xx = "I"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
    elif x >= 1400 and x < 1599:
        xx = "J"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
    elif x >= 1600 and x < 1999:
        xx = "K"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
    elif x >= 2000 and x < 2299:
        xx = "L"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
    elif x >= 2300 and x < 2599:
        xx = "M"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
    else :
        xx = "N"
        mouth_arduino.write(bytes(str(xx), 'utf-8'))
        # mouth_arduino.write(x.to_bytes(4, 'little'))
    #mouth_arduino.write(bytes(str(x), 'utf-8'))
    #print(xx )
    #time.sleep(0.05)



class VoiceDetector(Thread):


    # set up audio recording and voice detection
    def __init__(self):
        super(VoiceDetector, self).__init__()
        self.wav_audio = []
        self.hq_recorder = None
        #self._minVoicePercent = 20 # voice calibration
        self._minVoicePercent = 50 # voice calibration
        self._lowerThanMin = False
        self._voiceTimer = 0
        self._recordingTimer = 0
        # self._recordingMaxNs = 20_000_000_000  # 20 seconds
        self._recordingMaxNs = 8_000_000_000
        self._recordingMaxNsTimer = 0
        self._maxLowPeriodNs = 2_000_000_000  # 5 seconds
        self._maxLowPeriodTimer = 0
        self._isRecording = False ##
        self._isProcessing = False
        print("VoiceDetector init.")

    def run(self):
        global robot_state
        global request_uuid

        # self.print_mic_devices()

        # Capture voice
        recorder = PvRecorder(frame_length=512, device_index=selected_mic_device_index)
        porcupine = pvporcupine.create(access_key=picovoice_api_key, keyword_paths=keyword_paths)
        cobra = pvcobra.create(access_key=picovoice_api_key)

        recorder.start()


        # keywords = list()
        # for x in keyword_paths:
        #     keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
        #     if len(keyword_phrase_part) > 6:
        #         keywords.append(' '.join(keyword_phrase_part[0:-6]))
        #     else:
        #         keywords.append(keyword_phrase_part[0])



        print('Listening ... (Press Ctrl+C to exit)\n')

        # Threshold for silence( alter depending on background )
        silent_threshold = -40  
        silence_duration = 2 
        silence_timer = None

        # Loop to capture voice until recording stops and processing of audio starts
        try:
            while not self._isProcessing:
                pcm = recorder.read()
                now = time.monotonic_ns()

                # calculate voice probability
                voice_probability = cobra.process(pcm)
                percentage = voice_probability * 100
                bar_length = int((percentage / 10) * 3)
                empty_length = 30 - bar_length
                sys.stdout.write("\r[%3d]|%s%s|" % (
                    percentage, '█' * bar_length, ' ' * empty_length))
                sys.stdout.flush()

                # See if recording exceeds max time or silence
                prev_lower_than_min = self._lowerThanMin
                now_lower_than_min = percentage < self._minVoicePercent
                stopreason_1 = (now - self._recordingTimer) > self._recordingMaxNs
                stopreason_2 = self._lowerThanMin and (now - self._maxLowPeriodTimer) > self._maxLowPeriodNs
                if self._isRecording and (stopreason_1 or stopreason_2):
                # if self._isRecording and ( stopreason_2):
                #    if (stopreason_1):
                #        print("Stop recording due to reason 1\n")
                #        print(f"diff: {str(now - self._recordingTimer)}ns > {str(self._recordingMaxNs)}\n")
                    if (stopreason_2):
                        print("Stop recording due to reason 2\n")
                        print(f"diff: {str(now - self._maxLowPeriodTimer)}ns > {str(self._maxLowPeriodNs)}\n")
                    # stop the recording
                    self._isProcessing = True
                    self.stop_voice_recording(str(request_uuid))
                    robot_state = RobotState.PROCESSING
                    self._isRecording = False

                else:
                    # check conditions to start the recording
                    if (percentage > self._minVoicePercent + 2) and not self._isRecording:
                        # start the recording
                        self._isRecording = True
                        self._recordingTimer = now
                        self._maxLowPeriodTimer = now
                        self.start_voice_recording()
                        robot_state = RobotState.LISTENING
                    else:
                        if self._isRecording:
                            # continue recording
                            hq_pcm = self.hq_recorder.read()
                            self.wav_audio.extend(hq_pcm)
                        # process timers
                        if now_lower_than_min is not prev_lower_than_min:
                            # reset low activity timer
                            print('Reset low activity timer')
                            self._maxLowPeriodTimer = now
                        self._lowerThanMin = now_lower_than_min
        except KeyboardInterrupt:
        # Recording has stopped
           recorder.stop()
        finally:
        # Recording has stopped
            self._isRecording = False
            robot_state = RobotState.PROCESSING
            recorder.stop()
            porcupine.delete()
            recorder.delete()

    # Func to start recording audio
    def start_voice_recording(self):
        print("\nSTART voice recording.")
        #cls.wav_file = wave.open(recording_dir, "w")
        # noinspection PyTypeChecker
        #cls.wav_file.setparams((1, 2, 44100, 1024, "NONE", "NONE"))
        # cls.hq_recorder = PvRecorder(frame_length=1024, device_index=selected_mic_device_index)
        # cls.hq_recorder.delete()
        self.hq_recorder = PvRecorder(frame_length=1024, device_index=selected_mic_device_index)
        self.hq_recorder.start()
        return


    # Func to end recording audio
    def stop_voice_recording(self, id):
        print("\nSTOP voice recording.")
        self.hq_recorder.stop()
        with wave.open(recording_dir+id+".wav", "w") as f:
            f.setparams((1, 2, 16000, 1024, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(self.wav_audio), *self.wav_audio))
        recording_segment = AudioSegment.from_wav(recording_dir+id+".wav")
        recording_segment += 12
        recording_segment.export(recording_dir+id+".mp3", format="mp3")
        self.hq_recorder.delete()
        del self.hq_recorder
        return


    # See if correct mic
    @classmethod
    def print_mic_devices(cls):
        devices = PvRecorder.get_available_devices()
        for i in range(len(devices)):
            print("index: %d, device name: %s" % (i, devices[i]), end=" ")
            if i == selected_mic_device_index:
                print("<-- SELECTED")
            else:
                print("\n", end="")
        return

# Send to arduino, control Niki
def main():
    global robot_state
    global request_uuid
    global dialog
    write_eyes(1)
    write_head(1)
    write_mouth(0)
    write_boddy(1)
    write_righthand(1)
    write_lefthand(1)


###############################################################################################################
    # useConversationStarter = True  #
    useConversationStarter = False  ### SHE STARTS SPEAKING FIRST

    conversationStarterLang = 'el'
    # conversationStarterLang = 'en'
    #conversationStarterLang = 'el'
    ########### DEFAULT
    with open('conversationStarter.txt', 'r', encoding='utf-8') as file:
        conversationStarter = file.read().strip()

    voice_detector = None

    # Greek el
    # English en
    # Chinese zh
    # Italian it
    # Spanish es
    # Russian ru
    # Hindi hi
    # German sq
    # Arabic ar
    # French fr

    current_language = 'el'
    # current_language = 'en'

    dialog = []

    # Control personallity of Niki
    #with open('dialoguesFriendly.txt', 'r', encoding='utf-8') as file:
    with open('dialoguesDemokritos.txt', 'r', encoding='utf-8') as file:
        entry = {'role': '', 'content': ''}
        for line in file:
            if line.strip() == '---':  # End of an entry
                dialog.append(entry)
                entry = {'role': '', 'content': ''}
            elif line.startswith('role:'):
                entry['role'] = line.strip().split('role:')[1].strip()
            else:
                entry['content'] += line


    # To start conversation
    if useConversationStarter:
        print('Starting conversation ...\n')
        request_uuid = uuid.uuid4()
        robot_state = RobotState.TALKING
        tts = gTTS(conversationStarter, lang=conversationStarterLang)
        tts_filename_mp3 = tts_dir + str(request_uuid) + ".mp3"
        tts.save(tts_filename_mp3)
        tts_filename_wav = tts_dir + str(request_uuid) + ".wav"
        tts_wav = AudioSegment.from_mp3(tts_filename_mp3)
        tts_wav += 12
        tts_wav.export(tts_filename_wav, format="wav")
        write_mouth(200)
        CHUNK = 1024
        wf = wave.open(tts_filename_wav, 'rb')


        total_frames = wf.getnframes()
        stop_frame = total_frames * 0.6  # 80% of the total frames

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        # Niki speaks
        played_frames = 0
        CHUNK = 1024

        # read data
        audio_data = wf.readframes(CHUNK)

        # Playback loop
        while len(audio_data) > 0:
            stream.write(audio_data)
            played_frames += CHUNK  # Update played frames

            # Check if played frames have not yet reached 80% of total
            if played_frames <= stop_frame:
                # Process audio data to control mouth movement
                try:
                    ampSample3 = abs(audio_data[2])
                    write_mouth(ampSample3 * 10)
                except IndexError:
                    pass
            # Else, do not move the mouth but continue playback

            audio_data = wf.readframes(CHUNK)


        # Stop audio
        stream.stop_stream()
        stream.close()
        p.terminate()
        robot_state = RobotState.COMPLETE

        # Control Niki
        write_eyes(0)
        write_head(1)
        write_mouth(0)
        write_boddy(1)
        write_righthand(1)
        write_lefthand(1)
        robot_state = RobotState.INIT


# The next API inclusion has been taken from the OpenAI API 
    while True:
        try:
            if robot_state == RobotState.INIT:
                request_uuid = uuid.uuid4()
                voice_detector = VoiceDetector()
                robot_state = RobotState.IDLE
                voice_detector.run()
            elif robot_state == RobotState.LISTENING:
                print("Listening state.")
            elif robot_state == RobotState.PROCESSING:
                del voice_detector
                print("Processing...")
                # Use openai API
                api_url = "https://api.openai.com/v1/audio/transcriptions"
                # Bearer token
                headers = {
                    'Authorization': 'Bearer '+openai_api_key,
                }
                # Form data
                data = {
                    'model': 'whisper-1',
                    'language': 'el',  # Use the current language here
                }

                # File to be uploaded
                filename = recording_dir+str(request_uuid)+".mp3"
                files = {'file': (filename, open(filename, 'rb'))}
                # Make the request
                response = requests.post(api_url, data=data, files=files, headers=headers)
                # Check the response
                if response.status_code != 200:
                    print("Error! Status Code:", response.status_code, "Response:", response.text)
                    robot_state = RobotState.INIT
                    continue
                json_response = response.json()
                print("Success! Response:", json_response)
                question_text = json_response.get('text')
                dialog.append({'role': 'user',
                               'content': question_text})
                # Step 2 -- Completion API ===
                # API endpoint URL
                api_url = "https://api.openai.com/v1/chat/completions"
                # Bearer token
                headers = {
                    'Authorization': 'Bearer ' + openai_api_key,
                    'Content-Type': 'application/json'
                }
                # Form data
                data = {
                    'model': 'gpt-3.5-turbo', #'gpt-4',
                    'messages': dialog,
                }
                # Make the request
                response = requests.post(api_url, json=data, headers=headers)
                # Check the response 
                if response.status_code != 200:
                    print("Error! Status Code:", response.status_code, "Response:", response.text)
                    robot_state = RobotState.INIT
                    continue
                json_response = response.json()
                print("Success! Response:", json_response)
                answer_object = json_response['choices'][0]['message']
                answer_text = answer_object['content']
                print(answer_text)

                # Control Niki
                write_eyes(4)
                write_head(1)
                write_boddy(2)
                write_righthand(1)
                write_lefthand(1)
                #answer_json = json.loads(answer_object)
                dialog.append(answer_object)
                robot_state = RobotState.TALKING
                # tts = gTTS(answer_text, lang='el')
                tts = gTTS(answer_text, lang=current_language)  # Use the current language here
                tts_filename_mp3 = tts_dir+str(request_uuid)+".mp3"
                tts.save(tts_filename_mp3)
                # convert to wav
                tts_filename_wav = tts_dir + str(request_uuid) + ".wav"
                tts_wav = AudioSegment.from_mp3(tts_filename_mp3)
                tts_wav += 12
                tts_wav.export(tts_filename_wav, format="wav")
                # apply audio effects
                # tts_filename_wav_processed = tts_dir + str(request_uuid) + "-processed.wav"
                # x, sr = load(tts_filename_wav)
                # fx = Fx(sr)
                # fx_chain = {"pitch": -6,
                #             "flanger": 0.9
                #             }
                # optional_parameters = {"flanger_frequency": 0.5,
                #                        "flanger_depth": 9.75,
                #                        "flanger_delay": 0.9375
                #                        }
                # y = fx.process_audio(x, fx_chain, optional_parameters)
                # soundfile.write(tts_filename_wav_processed, y, sr)
                # tts_filename_wav = tts_filename_wav_processed
                # playback
                write_mouth(200)
                CHUNK = 1024
                wf = wave.open(tts_filename_wav, 'rb')
                # instantiate PyAudio (1)
                p = pyaudio.PyAudio()
                # open stream (2)
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                output=True)
                # read data
                audio_data = wf.readframes(CHUNK)

                played_frames = 0
                CHUNK = 1024
                total_frames = wf.getnframes()
                stop_frame = total_frames * 0.2  # 40% of the total frames
                #print('stop_frame = ', stop_frame)

                # Sync mouth to audio for intensity 
                while len(audio_data) > 0:
                    stream.write(audio_data)
                    played_frames += CHUNK  # Update played frames

                    # Check if played frames have not yet reached 80% of total
                    #print (played_frames)
                    if played_frames <= stop_frame:
                        # Process audio_data to control mouth movement
                        try:
                            ampSample3 = abs(audio_data[2])
                            write_mouth(ampSample3 * 10)
                        except IndexError:
                            pass
                    # Else, do not move the mouth but continue playback

                    # Read next chunk
                    audio_data = wf.readframes(CHUNK)

                # play stream (3)

                #while len(audio_data) > 0:
                #    stream.write(audio_data)
                #    audio_data = wf.readframes(CHUNK)
                #    # Do all of your DSP processing here i.e. function call or whatever
                #    try:
                #        ampSample3 = abs(audio_data[2])
                #        write_mouth(ampSample3*10)
                #    except IndexError:
                #        break
                # stop stream (4)
                stream.stop_stream()
                stream.close()
                # close PyAudio (5)
                p.terminate()
                robot_state = RobotState.COMPLETE
            elif robot_state == RobotState.COMPLETE:
                # Send to Niki
                write_eyes(0)
                write_head(1)
                write_mouth(0)
                write_boddy(1)
                write_righthand(1)
                write_lefthand(1)
                robot_state = RobotState.INIT
            else:
                continue
        except KeyboardInterrupt:
            del voice_detector
            break

if __name__ == '__main__':
    main()
