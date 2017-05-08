import abc

from polyglot.text import Text
from polyglot.mapping import Embedding


class APIHead(object):
    def __init__(self, *args, **kwargs):
        self.ex_details = kwargs.get('ex_details')
        self.data_iterator = None

    @abc.abstractmethod
    def execute(self):
        """
        :returns list of items to be fed in ElasticSearch or a generator for the same.
        """
        raise NotImplementedError('Please implement this method in class "%s"' % self.__class__.__name__)

    def get_ex_details(self):
        return self.ex_details

    def get_data(self):
        if self.data_iterator is not None:
            return self.data_iterator
        else:
            raise NotImplementedError("data_iterator not assigned an iterable object.")


class NLP(object):
    def __init__(self, sen, *args, **kwargs):
        self.sen = sen
        self.text = Text(self.sen)
        pass

    def validate(self):
        self.sen = Text
        return True


def get_NER():
    embeddings = Embedding.load("/home/rushil/polyglot_data/embeddings2/en/embeddings_pkl.tar.bz2")
    li = ['jobs', 'employee', 'freelance', 'employment', 'fulltime', 'work', 'parttime', 'placement', 'gig',
          'incumbency', 'occupation', 'opportunity', 'work', 'development']
    neighbors = []

    for word in li:
        try:
            neighbors += embeddings.nearest_neighbors(word, top_k=10)
        except:
            pass

    for n in set(neighbors + li):
        print n
        # for n in li:
        #     print n


# tokens = [token for token in tokens if token not in stopwords]

def get_NER2():
    sen = "Backend Developer Needed. Location: Greater Seattle Area Company: Soda.com Description: We 2019 are looking for a Web Developer with an emphasis on Wordpress to join our development team as we increase our capacity in 2017. PHP, MySQL, HTML, CSS, JS, Git, Precompilers, Gulp."
    text = Text(sen)
    print(text.pos_tags)


def get_NER3():
    sen = "Backend Developer Needed. Location: Greater Seattle Area Company: Soda.com Description: We 2019 are looking for a Web Developer with an emphasis on Wordpress to join our development team as we increase our capacity in 2017. PHP, MySQL, HTML, CSS, JS, Git, Precompilers, Gulp."
    # rake_object = RAKE.Rake('/stoplists/SmartStoplist.txt', 5, 3, 4)


# def get_NER()
# def filter_sen()
get_NER()
