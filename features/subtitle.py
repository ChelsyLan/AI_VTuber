def generate_subtitle(text, translation, question):
    # output.txt will be used to display the subtitle on OBS
    _save_text_as_lines(text=text, filepath="output.txt")
    _save_text_as_lines(text=translation, filepath="output.txt",
                        header="--- Translation ---\n")

    # chat.txt will be used to display the chat/question on OBS
    _save_text_as_lines(text=question, filepath="chat.txt")


def _save_text_as_lines(text: str, filepath: str,
                        words_per_line=10, header=""):
    try:
        with open(filepath, "w", encoding="utf-8") as outfile:
            if header != "":
                outfile.write(header)
            
            words = text.split()
            lines = [words[i:i + words_per_line]
                    for i in range(0, len(words), words_per_line)]
            
            for line in lines:
                outfile.write(" ".join(line) + "\n")
    
    except Exception as e:
            print(f"Error writing to chat.txt: {e}")
