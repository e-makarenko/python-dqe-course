import re

text = '''homEwork:

  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate number of whitespace characters in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''

# transform the whole text to lowercase
lowercase_text = text.lower()

# split the text into paragraphs
paragraphs = lowercase_text.split('\n\n')

# initialize empty lists for capitalized paragraphs and last words of the sentences
capitalized_paragraphs = []
last_words = []

# iterate over each paragraph and split each paragraph into sentences to capitalize them
for paragraph in paragraphs:
    sentences = paragraph.split('. ')

    #check if the sentence is not empty, remove whitespaces and capitalize it
    capitalized_sentences = [sentence.strip().capitalize() for sentence in sentences if sentence]

    #get the last word of each sentence without the ending dot
    last_words += [re.sub(r'[^\w\s]', '', sentence.split()[-1]) for sentence in sentences if sentence]

    capitalized_paragraph = '. '.join(capitalized_sentences)

    #add the capitalized paragraph to the list
    capitalized_paragraphs.append(capitalized_paragraph)

# generate the new sentence with the collected last words, and add to the target paragraph
new_sentence = ' '.join(last_words).capitalize() + '.'

index = 0

# iterate through capitalized paragraphs and add the new sentence at the end of needed paragraph
for paragraph in capitalized_paragraphs:
    if 'to the end of this paragraph' in paragraph.lower():
        capitalized_paragraphs[index] += ' ' + new_sentence
    index += 1

# join the transformed paragraphs to have 2 new lines and whitespaces between each of them
capitalized_text = '\n\n  '.join(capitalized_paragraphs)

capitalized_text = capitalized_text.replace(' iz ', ' is ')

print(capitalized_text)

# count whitespaces in the original text using re.findall() method
whitespace_count = len(re.findall(r'\s', text))

print(f'The original text contains {whitespace_count} whitespace characters.')
