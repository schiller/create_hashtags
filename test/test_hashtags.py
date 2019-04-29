import pytest
from unittest.mock import MagicMock

from .context import app
from app import HashtagMaker


@pytest.fixture
def hm():
    return HashtagMaker()


def test_get_frequence_dist(hm):
    words = ['How', 'many', 'times', 'does', 'the', 'word', 'word', 'appear']
    fdist = hm._get_frequence_dist(words)
    assert fdist['times'] == 1
    assert fdist['word'] == 2


def test_get_words(hm):
    sentence = 'How many times does the word "word" appear?'
    expected_words = ['How', 'many', 'times', 'does', 'the', 'word', 'word', 'appear']
    words = hm._get_words(sentence)
    assert words == expected_words


def test_get_sentences(hm):
    text = 'How many times does the word "word" appear? I think it\'s two'
    expected_sentences = [
        'How many times does the word "word" appear?',
        'I think it\'s two'
    ]
    sentences = hm._get_sentences(text)
    assert sentences == expected_sentences


def test_update_hashtags(hm):
    assert hm._hashtags == {}

    hm._update_hashtags('spam', 0, 0)
    hm._update_hashtags('spam', 1, 1)
    hm._update_hashtags('spam', 1, 1)
    hm._update_hashtags('eggs', 2, 1)
    expected_hashtags = {
        'spam': {
            'documents': [0, 1],
            'sentences': [0, 1]},
        'eggs': {
            'documents': [1],
            'sentences': [2]}
    }
    assert hm._hashtags == expected_hashtags


def test_update_frequencies(hm):
    words = ['spam', 'spam', 'eggs']

    hm._update_frequencies(words)

    assert hm._fdist['spam'] == 2
    assert hm._fdist['eggs'] == 1


def test_load_sentence(hm):
    document_idx = 1
    sentence = 'spam spam eggs'
    words = ['spam', 'spam', 'eggs']

    hm._get_words = MagicMock(return_value=words)
    hm._update_frequencies = MagicMock()
    hm._update_hashtags = MagicMock()

    hm._load_sentence(sentence=sentence, document_idx=document_idx)

    hm._get_words.assert_called_once_with(sentence)
    hm._update_frequencies.assert_called_once_with(words)
    assert hm._update_hashtags.call_count == len(words)


def test_load_document(hm):
    text = 'How many times does the word "word" appear? I think it\'s two'
    sentences = [
        'How many times does the word "word" appear?',
        'I think it\'s two'
    ]

    hm._get_sentences = MagicMock(return_value=sentences)
    hm._load_sentence = MagicMock()

    hm.load_document(document='doc1.txt', text=text)

    hm._get_sentences.assert_called_once_with(text)
    assert hm._load_sentence.call_count == len(sentences)


def test_get_most_common(hm):
    hm._sentences = [
        'spam, spam, spam',
        'spam, eggs and ham',
        'eggs and ham',
        'ham']
    hm._documents = ['doc0', 'doc1', 'doc2']
    hm._hashtags = {
        'spam': {
            'documents': [0, 1],
            'sentences': [0, 1]},
        'eggs': {
            'documents': [1],
            'sentences': [1, 2]},
        'ham': {
            'documents': [1, 2],
            'sentences': [1, 2, 3]}
    }
    most_common = [('spam', 4), ('ham', 3)]
    hm._fdist.most_common = MagicMock(return_value=most_common)

    expected_hashtags = [
        {
            'word': 'spam',
            'documents': ['doc0', 'doc1'],
            'sentences': [
                'spam, spam, spam',
                'spam, eggs and ham']
        },
        {
            'word': 'ham',
            'documents': ['doc1', 'doc2'],
            'sentences': [
                'spam, eggs and ham',
                'eggs and ham',
                'ham']
        }
    ]

    hashtags = hm.get_most_common(2)
    assert hashtags == expected_hashtags
