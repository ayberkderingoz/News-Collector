import matplotlib.pyplot as plt
from collections import Counter
from MongoDBConnection import MongoDBConnection
from MongoDBConnection import CollectionManager


class WordFrequencyAnalyzer:

    """
    A class to represent word frequency analyzer.
    
    ...

    Attributes
    ----------
    db_connection : MongoDBConnection
        mongodb connection
    collection : CollectionManager
        collection manager
    news : list
        list of news data
    
        
    Methods
    -------
    get_word_frequency()
        Gets word frequency of the news.
    plot_word_frequency(word_frequency, title)
        Plots word frequency of the news.
    get_word_frequency_without_connective()
        Gets word frequency of the news with connectives shown other color to improve data quality.

    
    """
    def __init__(self, db_connection, collection_name,news):
        self.db_connection = db_connection
        self.collection = self.db_connection.db[collection_name]
        self.news = news

    def get_word_frequency(self):
        word_frequency = Counter()
        for news in self.news:
            word_frequency.update(news.text.split())
        return word_frequency
    
    def plot_word_frequency(self, word_frequency, title):
        
        most_common_words = word_frequency.most_common(10)
        plt.bar(*zip(*most_common_words))
        plt.title('10 Most Common Words')
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(f'{title}.png')


    def get_word_frequency_without_connective(self):
        connectives = ['ve', 'ile', 'de', 'da', 'ki', 'bu', 'şu','o', 'ya', 'ne', 'ki', 'değil', 'ama', 'fakat', 'ancak', 'lakin', 'yani', 'ise', 'çünkü', 'zira', 'çünkü']
        word_frequency = Counter()
        for news in self.news:
            word_frequency.update(news.text.split())
        for connective in connectives:
            del word_frequency[connective]
        return word_frequency
    
class WordFrequency:
    def __init__(self, word, frequency):
        self.word = word
        self.frequency = frequency


