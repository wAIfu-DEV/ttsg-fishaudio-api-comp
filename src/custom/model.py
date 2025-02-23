from fish_audio_sdk import Session, TTSRequest
import logging
import os

def floor_to_nearest_multiple_of_two(n):
    return n // 2 * 2

class FishAudioTTSModel():
    def __init__(self, voice_id):
        self.voice_id = voice_id
        self.session = Session(apikey=os.environ['FISH_API_KEY'])


    def __call__(self, content: str):
        logging.debug(f"Generating Fishaudio TTS response stream for message: {content}")

        leftover = b""

        for chunk in self.session.tts(TTSRequest(
            reference_id=self.voice_id,
            text=content,
            format="pcm",
            normalize=False,
            latency="balanced",
            sample_rate=44100,
        )):
            chunk = leftover + chunk

            chunk_len = len(chunk)
            mul2_len = floor_to_nearest_multiple_of_two(chunk_len)

            leftover = chunk[mul2_len:]
            clipped_chunk = chunk[:mul2_len]
            logging.debug("Sent chunk of size: " + str(len(clipped_chunk)))
            yield clipped_chunk
        
        logging.debug("Finished generating response.")