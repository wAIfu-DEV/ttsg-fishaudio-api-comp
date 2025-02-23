from dotenv import load_dotenv
from .config import config
load_dotenv(dotenv_path=config['env'])

'''
Supported component type entrypoints

- Implement the specific entrypoint associated with your component type
- You can leave the others unimplemented

To support streaming, your implementation should be a generator: https://wiki.python.org/moin/Generators
You may also simply return the final result
'''

from .model import FishAudioTTSModel
import logging
ttsg_model = FishAudioTTSModel(config['voice_id'])

from jaison_grpc.common import STTComponentRequest, T2TComponentRequest, TTSGComponentRequest, TTSCComponentRequest
async def request_unpacker(request_iterator):
    async for request_o in request_iterator:
        match request_o:
            case STTComponentRequest():
                yield request_o.audio, request_o.sample_rate, request_o.sample_width, request_o.channels
            case T2TComponentRequest():
                yield request_o.system_input, request_o.user_input
            case TTSGComponentRequest():
                yield request_o.content
            case TTSCComponentRequest():
                yield request_o.audio, request_o.sample_rate, request_o.sample_width, request_o.channels
            case _:
                raise Exception(f"Unknown request type: {type(request_o)}")

def is_sentence(sentence):
    return sentence.endswith('.')

# For text-to-speech generation
async def start_ttsg(request_iterator):
    global ttsg_model
    sentence = ""
    async for content in request_unpacker(request_iterator): # receiving chunks of info through a stream
        logging.debug(f"Got content chunk: {content}")
        sentence += content
        if is_sentence(sentence):
            logging.debug(f"Processing sentence: {sentence}")
            for audio_chunk in ttsg_model(sentence):
                yield audio_chunk, 44100, 2, 1
            sentence = ""
    if len(sentence) > 0:
        logging.debug(f"Processing sentence: {sentence}")
        for audio_chunk in ttsg_model(sentence):
            yield audio_chunk, 24000, 2, 1

# For speech-to-text models
async def start_stt(request_iterator) -> str:
    for audio, sample_rate, sample_width, channels in request_unpacker(request_iterator): # receiving chunks of info through a stream
        raise NotImplementedError

# For text generation models
async def start_t2t(request_iterator) -> str:
    for system_input, user_input in request_unpacker(request_iterator): # receiving chunks of info through a stream
        raise NotImplementedError

# For voice changers
async def start_ttsc(request_iterator) -> str:
    for audio, sample_rate, sample_width, channels in request_unpacker(request_iterator): # receiving chunks of info through a stream
        raise NotImplementedError