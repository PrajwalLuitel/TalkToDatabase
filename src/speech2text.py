import gc
import torch
from typing import Literal
from faster_whisper import WhisperModel


class SpeechToText:

    def __init__(
        self, whisper_model_size: Literal["medium", "small"], device: str = None
    ) -> None:

        self.model_type = whisper_model_size

        if device:
            self.device = device
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # load the model
        self.load_model(self.model_type, self.device)

    def load_model(self, model_size, device):

        print(f"Loading the {model_size} model on {device}")

        self.model = WhisperModel(model_size, device=device, compute_type="float32")

    def __call__(self, audio_file_pth: str, beam_size: int = 5):

        segments, info = self.model.transcribe(
            audio_file_pth,
            beam_size=beam_size,
        )

        result = {}

        for segment in segments:
            # get the key
            key = f"{segment.start}-{segment.end}"

            # key will be tine and audio will be file
            result[key] = str(segment.text)

        if torch.cuda.is_available():
            del self.model
            torch.cuda.empty_cache()
            gc.collect()

        return result
