from openai import OpenAI

from config import max_token
from features.openai_t2t import get_openai_client

# Set your OpenAI API key here
client = get_openai_client()
# sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

def translate_openai(text, target_lang):
    if target_lang.lower() in ["ja", "japanese"]:
        message = (
            f"Translate this text: {text} to Japanese. Use commonly accepted Japanese terms for any words that have direct equivalents in Japanese. For words that do not have direct equivalents (such as names or specific terms in other languages), transliterate them into katakana with the closest Japanese pronunciation. If the text is already Japanese, do not change it."
        )
    elif target_lang.lower() in ["KATAKANA", "katakana"]:
        message = (
            f"convert this text: {text} to katakana Japanese with closest pronunciation so it will hear the same."
        )
    else:
        message = f"Translate this text: {text} to {target_lang}. If the some of the text is already {target_lang}, do not change it."
    
    messages = [
        {"role": "system", "content": "You are a translator, do not add any explanations or comments."},
        {"role": "user", "content": message},
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages, 
            max_tokens=max_token,
        )
        
    except Exception as e:
        print(f"Error during translation: {e}")
        return
    
    translated_text = response.choices[0].message.content.strip()
    
    return translated_text

if __name__ == "__main__":
    text = "test word"
    
    translated_text = translate_openai(text, "JA")
    print(f"Translated Text: {translated_text}")
