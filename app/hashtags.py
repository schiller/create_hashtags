import nltk
import nltk.data


class HashtagMaker:

    def __init__(self) -> None:
        nltk.download('punkt')
        self._sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        self._fdist = nltk.FreqDist()
        self._documents = []
        self._sentences = []
        self._hashtags = {}

    def get_most_common(self, count: int) -> list:
        '''Get the hashtags dict for the most common words'''
        most_common = self._fdist.most_common(count)
        output_hashtags = []
        for word, freq in most_common:
            documents = [self._documents[idx] for idx in self._hashtags[word]['documents']]
            sentences = [self._sentences[idx] for idx in self._hashtags[word]['sentences']]
            output_hashtags.append({
                'word': word,
                'documents': documents,
                'sentences': sentences
            })
        return output_hashtags

    def load_document(self, document: str, text: str) -> None:
        '''Break text into sentences and load them'''
        self._documents.append(document)
        document_idx = len(self._documents) - 1

        sentences = self._get_sentences(text)

        for sentence in sentences:
            self._load_sentence(sentence, document_idx)

    def _load_sentence(self, sentence: str, document_idx: int) -> None:
        '''Break sentence into words and update frequencies and hashtags'''
        self._sentences.append(sentence)
        sentence_idx = len(self._sentences) - 1

        words = self._get_words(sentence)

        self._update_frequencies(words)

        for word in words:
            self._update_hashtags(word, sentence_idx, document_idx)

    def _update_frequencies(self, words: str) -> None:
        '''Update words frequence distribution'''
        fdist = self._get_frequence_dist(words)
        self._fdist += fdist

    def _update_hashtags(self, word: str, sentence_idx: int, document_idx: int) -> None:
        '''Update hashtags dict with the given word'''
        if word not in self._hashtags:
            self._hashtags[word] = {
                'documents': [],
                'sentences': []
            }
        if document_idx not in self._hashtags[word]['documents']:
            self._hashtags[word]['documents'].append(document_idx)
        if sentence_idx not in self._hashtags[word]['sentences']:
            self._hashtags[word]['sentences'].append(sentence_idx)

    def _get_sentences(self, text: str) -> list:
        '''Get the list of sentences from a text'''
        return self._sent_detector.tokenize(text.strip())

    def _get_words(self, text: str) -> list:
        '''Get alphanumerical words from a string'''
        tokens = nltk.word_tokenize(text.strip())
        words = [s for s in tokens if s.isalnum()]
        return words

    def _get_frequence_dist(self, words: list) -> nltk.FreqDist:
        '''Count frequencies of words from a list'''
        return nltk.FreqDist(words)
