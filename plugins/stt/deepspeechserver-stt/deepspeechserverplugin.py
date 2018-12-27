import logging
import wave
import requests
from naomi import plugin


class DeepspeechSTTPlugin(plugin.STTPlugin):
    def __init__(self, *args, **kwargs):
        plugin.STTPlugin.__init__(self, *args, **kwargs)

        self._logger = logging.getLogger(__name__)
        self._http = requests.Session()

        try:
            url = self.profile['deepspeechserver-stt']['url']
        except KeyError:
            url = 'http://localhost:8888/stt'
        self._url = url

    def transcribe(self, fp):
        wav = wave.open(fp, 'rb')
        frame_rate = wav.getframerate()
        wav.close()
        data = fp.read()

        r = self._http.post(self._url, data=data)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            self._logger.critical('Request failed with http status %d',
                                  r.status_code)
            return []

        if not r.status_code == "200":
            msg = r.content
            self._logger.critical('Transcription failed: %s', msg)
            return []

        results = r.content

        self._logger.info('Transcribed: %r', results)
        return results
