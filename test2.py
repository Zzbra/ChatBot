import pyaudio
import scipy.io.wavfile as wav
import wave
import json
import os
from google.cloud import speech
import io

WAVE_OUTPUT_FILENAME = "test_audio.wav"


def record_audio(WAVE_OUTPUT_FILENAME):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 2

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = [stream.read(CHUNK) for i in range(0, int(RATE / CHUNK * RECORD_SECONDS))]

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def send_google_request():
    stream = os.popen(
        "curl -s -H Content-Type: application/json -H Authorization: Bearer $(gcloud auth application-default print-access-token) https://speech.googleapis.com/v1/speech:recognize -d @sync-request.json")
    output = stream.read()
    print(output)
    with open('out.json', 'w') as outfile:
        json.dump(output, outfile)


def google_predict(WAVE_OUTPUT_FILENAME):
    """Transcribe the given audio file."""
    client = speech.SpeechClient()

    with io.open(WAVE_OUTPUT_FILENAME, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="fr-FR",
    )

    response = client.recognize(config=config, audio=audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))


if __name__ == '__main__':
    # record_audio(WAVE_OUTPUT_FILENAME)
    predicted_text = google_predict(WAVE_OUTPUT_FILENAME)
    print(predicted_text)
