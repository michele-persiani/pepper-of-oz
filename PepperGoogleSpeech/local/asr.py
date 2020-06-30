from google.cloud import speech
import re
import Settings

class ASR(object):
    """Abstract Speech Recognition Class"""

    def transcribe(self, audio):
        """
        Transcribe Speech in Audio

        Parameters
        ----------
        audio: numpy.ndarray

        Returns
        -------
        transcript: list of (str, float)
            List of (<transcript>, <confidence>) pairs
        """
        raise NotImplementedError()


class GoogleASR(ASR):
    def __init__(self, language=Settings.LANGUAGE, sample_rate=16000, max_alternatives = 10, phrases=()):
        """
        Transcribe Speech using Google Speech API

        Parameters
        ----------
        language: str
            Language Code, See: https://cloud.google.com/speech/docs/languages
        sample_rate: int
            Input Audio Sample Rate
        max_alternatives: int
            Maximum Number of Alternatives Google will provide
        phrases: tuple of str
            Phrases or words to add to Google Speech's Vocabulary
        """
        super(GoogleASR, self).__init__()

        self._config = speech.types.RecognitionConfig(
            encoding = speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz = sample_rate,
            language_code = language,
            max_alternatives = max_alternatives,
            speech_contexts=[speech.types.SpeechContext(
                phrases=phrases
            )]
        )

    def transcribe(self, audio):
        """
        Transcribe Speech in Audio

        Parameters
        ----------
        audio: numpy.ndarray

        Returns
        -------
        transcript: List
            List of (<transcript>, <confidence>) pairs
        """
        response = speech.SpeechClient().recognize(self._config,speech.types.RecognitionAudio(content=audio.tobytes()))
        hypotheses = []

        for result in response.results:
            for alternative in result.alternatives:
                hypotheses.append([
                    alternative.transcript.encode('utf-8'),
                    alternative.confidence
                ])
        return hypotheses


class GoogleWordASR(ASR):
    def __init__(self, language=Settings.LANGUAGE, sample_rate=16000, max_alternatives = 10, phrases=()):
        """
        Transcribe Speech using Google Speech API and provide Word Timings

        Parameters
        ----------
        language: str
            Language Code, See: https://cloud.google.com/speech/docs/languages
        sample_rate: int
            Input Audio Sample Rate
        max_alternatives: int
            Maximum Number of Alternatives Google will provide
        phrases: tuple of str
            Phrases or words to add to Google Speech's Vocabulary
        """
        super(GoogleWordASR, self).__init__()

        self._config = speech.types.RecognitionConfig(
            encoding = speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz = sample_rate,
            language_code = language,
            max_alternatives = max_alternatives,
            enable_word_time_offsets=True,
            speech_contexts=[speech.types.SpeechContext(
                phrases=phrases
            )]
        )

    def transcribe(self, audio):
        """
        Transcribe Speech in Audio

        Parameters
        ----------
        audio: numpy.ndarray

        Returns
        -------
        transcript: List
            List of (<transcript>, <confidence>, <word timings>) pairs
        """
        response = speech.SpeechClient().recognize(self._config,speech.types.RecognitionAudio(content=audio.tobytes()))
        hypotheses = []

        for result in response.results:
            for alternative in result.alternatives:
                hypotheses.append([
                    alternative.transcript,
                    alternative.confidence,
                    [[word.word,
                      word.start_time.seconds + word.start_time.nanos * 1E-9,
                      word.end_time.seconds + word.end_time.nanos * 1E-9,
                      ] for word in alternative.words]
                ])
        return hypotheses

