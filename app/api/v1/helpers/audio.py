import google.cloud.texttospeech as tts
import random
from app.api.v1.global_config.global_config import audio_config
from loguru import logger

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
        audio_config[whatsapp]['audio'] = False
    
    return False