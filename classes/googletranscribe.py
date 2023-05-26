from datetime import timedelta
from typing import Optional, Sequence, cast

from google.cloud import videointelligence_v1 as vi


class GoogleTranscribe:
    def __init__(self):
        self.video_client = vi.VideoIntelligenceServiceClient()
        self.language_code = "es-MX"
        self.results = None

    def transcribe_speech(self, video_uri, segments=None):
        video_client = vi.VideoIntelligenceServiceClient()
        features = [vi.Feature.SPEECH_TRANSCRIPTION]
        config = vi.SpeechTranscriptionConfig(
            language_code=self.language_code,
            enable_automatic_punctuation=True,
        )
        context = vi.VideoContext(
            segments=segments,
            speech_transcription_config=config,
        )
        request = vi.AnnotateVideoRequest(
            input_uri=video_uri,
            features=features,
            video_context=context,
        )

        print(f'Processing video "{video_uri}"...')
        operation = self.video_client.annotate_video(request)

        # Wait for operation to complete
        response = cast(vi.AnnotateVideoResponse, operation.result())
        # A single video is processed
        self.results = response.annotation_results[0]

    def video_speech(self, min_confidence: float = 0.8):

        def keep_transcription(transcription: vi.SpeechTranscription) -> bool:
            return min_confidence <= transcription.alternatives[0].confidence

        transcriptions = self.results.speech_transcriptions
        transcriptions = [t for t in transcriptions if keep_transcription(t)]

        transcription_list = []
        for transcription in transcriptions:
            first_alternative = transcription.alternatives[0]
            confidence = first_alternative.confidence
            transcript = first_alternative.transcript
            transcription_list.append(transcript.strip())
        return " ".join(transcription_list)

    def get_transcription(self, video_uri, segments=None, min_confidence: float = 0.8):
        self.transcribe_speech(video_uri, segments)
        return self.video_speech(min_confidence)
