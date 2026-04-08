# to use hugging face install transformers, here it is not used but always prefer to install dependencies/library in a virtual environment
from transformers import pipeline

# NLP Tasks

'''
1. Text Classification: Assigning a category to a piece of text.
Sentiment analysis
Topic classification
spam detection
'''

#no need to write code from scratch for text-classification, we can use pre-trained models from Hugging Face
classifier=pipeline('text-classification')

'''
2. Token classification: Assigning a label to individual tokens in a text sequence.
Named entity recognition (NER)
Part-of-speech tagging
'''

token_classifier=pipeline('token-classification')

'''
3. Question Answering: Extracting an anser from a given context based on a question.
'''
question_answerer=pipeline('question-answering')

'''
4. Text Generation: Generating text based on a given prompt.
Language modelling
story generation
'''
text_generator=pipeline('text-generation')

'''
5. Summarixation: Condensing a long piece of text into a shorter summary
'''
summarizer=pipeline('summarization')

'''
Translation: Translating text from one language to another.
'''

translator=pipeline('translation',model='Helsinki-NLP/opus-mt-en-fr')

'''
6. Text2Text Generation: General-purpose text transformation,including summarization and translation
'''

text2text_generator=pipeline('text2text-generation')

'''
7. Fill mask= Predicting masked token in a sequence
'''

fill_mask=pipeline('fill-mask')

'''
8. Feature Extraction: Extracting hidden states or features from text
'''

feature_extractor=pipeline('feature-extraction')

'''
9. Sentence similarity: Measuring the similarity between two sentences
'''

sentence_similarity=pipeline('sentence-similarity')

# using the models
result=classifier("I love Hugging Face!")
print(result)