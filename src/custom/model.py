from fish_audio_sdk import Session, TTSRequest
import logging
import os

class FishAudioTTSModel():
    def __init__(self, voice_id):
        self.voice_id = voice_id
        self.session = Session(apikey=os.environ['FISH_API_KEY'])


    def __call__(self, content: str):
        logging.debug(f"Generating Fishaudio TTS response stream for message: {content}")

        for chunk in self.session.tts(TTSRequest(
            reference_id=self.voice_id,
            text=content,
            format="pcm",
            normalize=False,
            latency="balanced",
            chunk_length=int(4096/2),
            sample_rate=44100
        )):
            yield chunk
        
        logging.debug("Finished generating response.")