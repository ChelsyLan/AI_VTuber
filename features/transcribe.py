from openai import OpenAI

def transcribe_audio(
    client: OpenAI,
    filepath="input.wav",
) -> str:
    
    try:
        with open(filepath, "rb") as audio_file:
            # Transcribe the audio to detected language
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text",
                # TODO: specify language to minimize latency/performance
                # language=,
            )
        print ("Question: " + transcript)
        
        return transcript
    
    except Exception as e:
        print("Error transcribing audio: {0}".format(e))
        return ""
