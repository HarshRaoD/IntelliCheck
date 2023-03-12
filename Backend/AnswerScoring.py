from flair.data import Sentence
from flair.models import SequenceTagger
import spacy

def do_tokenisation(sentence_str: str):
    # load tagger
    tagger = SequenceTagger.load("flair/ner-english-ontonotes")

    # make example sentence
    sentence = Sentence(sentence_str)

    # predict NER tags
    tagger.predict(sentence)

    entities = {}
    for label in sentence.get_labels():
        value = label.shortstring.split('/')[0][1:-1]
        key = label.shortstring.split('/')[1]
        try:
            entities[key].append(value)
        except:
            entities[key] = [value]
    
    return entities

def get_verbs(sentence_str: str) -> list:
    nlp = spacy.load("en_core_web_lg")
    doc = nlp("Man walks into a bar. He ate food.")  # Your text here

    words = []
    for token in doc:
        if token.pos_ == "VERB":
            start = token.idx  # Start position of token
            end = token.idx + len(token)  # End position = start + len(token)
            words.append(token.text)
    
    return words


def __test_do_tokenisation():
    print(do_tokenisation("Sanskar had trouble with poop, while Kshitij had trouble with allergies."))

def __test_get_verbs():
    print(get_verbs("Man walks into a bar. He ate food."))

__test_get_verbs()