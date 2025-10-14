from gtts import gTTS
import os

def tts_synthesize(text, lang="en", output_path="out/speech.mp3"):
    """Convert text to speech"""
    try:
        os.makedirs("out", exist_ok=True)
        
        # Map language codes
        lang_map = {
            "en": "en",
            "hi": "hi",
            "kn": "kn"  # Kannada supported by gTTS
        }
        
        tts_lang = lang_map.get(lang, "en")
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        tts.save(output_path)
        
        return output_path
    except Exception as e:
        print(f"TTS Error: {e}")
        return None
