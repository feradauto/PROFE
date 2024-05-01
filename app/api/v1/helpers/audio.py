import google.cloud.texttospeech as tts
import random
from app.api.v1.global_config.global_config import audio_config
from loguru import logger
from google.cloud import speech
import requests
import soundfile as sf
from base64 import b64encode
from app.api.v1.twilio.whats import ACCOUNT_SID, AUTH_TOKEN


def get_and_transcribe(speech_file):
    auth_str = ACCOUNT_SID+":"+AUTH_TOKEN
    auth_bytes = auth_str.encode('utf-8')
    auth_b64 = b64encode(auth_bytes).decode('utf-8')
    headers = {'Authorization': 'Basic ' + auth_b64}
    data = requests.get(speech_file, headers=headers)
    with open("temp.ogg", 'wb') as file:
        file.write(data.content)
    audio_data, sample_rate = sf.read("temp.ogg")
    wav_file_path = f'temp.wav'
    sf.write(wav_file_path, audio_data, sample_rate)
    
    res = transcribe_file(wav_file_path)
    return res


def transcribe_file(speech_file):
    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    final_result=[]
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        final_result.append(result.alternatives[0].transcript)
        logger.info(f"Transcript: {result.alternatives[0].transcript}")
    final_result_str = ' '.join(final_result)

    return final_result_str


def text_to_wav(whatsapp:str, voice_name: str, text: str):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    random_number = str(random.randint(0, 999))

    filename = f"{whatsapp}_{voice_name}_{random_number}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        logger.info(f'Generated speech saved to "{filename}"')
        return filename
        

def audio_response(whatsapp, answer):
    if whatsapp in audio_config:
        if audio_config[whatsapp]['audio'] == True:
            filename = text_to_wav(whatsapp, "en-US-Studio-O", answer)
            logger.info(filename)
            return filename
    else:
        audio_config[whatsapp] = {'audio':False}
    
    return False