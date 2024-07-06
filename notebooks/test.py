from faster_whisper import WhisperModel

model_size = "medium"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float32")


segments, info = model.transcribe(
    "/home/rjn/Documents/GitHub/TalkToDatabase/data/test_samles/Best Podcast Intro Examples 2021.mp3",
    beam_size=5,
)

print(
    "Detected language '%s' with probability %f"
    % (info.language, info.language_probability)
)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
