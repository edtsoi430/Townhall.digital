# Imports the Google Cloud client library
from google.cloud import translate

# Instantiates a client
translate_client = translate.Client()

# The text to translate
text = u'La Universidad de Michigan es una excelente escuela pública.'
# The target language
target = 'en'

# Translates some text into Russian
translation = translate_client.translate(
    text,
    target_language=target)

print(u'Original text: {}'.format(text))
print(u'Translation: {}'.format(translation['translatedText']))