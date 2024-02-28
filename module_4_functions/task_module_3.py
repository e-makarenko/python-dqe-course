import re


def split_by_special_characters(text):
    return re.split(r'([.!?]\s*)', text)


def convert_to_lowercase(text):
    return text.lower()


# function to capitalize sentences based on their index in splitted sentences (even index = sentence)
def capitalize_sentences(sentences):
    return [sentence.strip().capitalize() if i % 2 == 0 else sentence for i, sentence in enumerate(sentences)]


def replace_iz_with_is(text):
    return text.replace(' iz ', ' is ')


def count_whitespaces(text):
    return len(re.findall(r'\s', text))


def process_text(text):
    lowercase_text = convert_to_lowercase(text)
    sentences = split_by_special_characters(lowercase_text)
    print(sentences)
    formatted_sentences = capitalize_sentences(sentences)
    formatted_text = ''.join(formatted_sentences)
    corrected_text = replace_iz_with_is(formatted_text)

    return corrected_text


original_text = '''homEwork:

  tHis iz your homework, copy these text to variable.



  You need to normalize it from letter cases point of view. also, create one more sentence with last words of each existing sentence and add it to the end of this paragraph.



  it iz misspelling here. fix“iz” with correct “is”, but only when it iz a mistake.



  last iz to calculate number of whitespace characters in this tex. carefull, not only spaces, but all whitespaces. I got 87.'''


processed_text = process_text(original_text)
print(processed_text)

whitespace_count = count_whitespaces(original_text)
print(f'The original text contains {whitespace_count} whitespace characters.')
