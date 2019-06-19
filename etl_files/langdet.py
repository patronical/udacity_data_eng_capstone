from langdetect import detect

# define language find function
def langfind(text):
    """
    Detects language of text.
    Imports text.
    Returns language tag.
    """
    try:
        lang = detect(text[1])
    except:
        lang = 'unknown'
    return lang
