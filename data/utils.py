import abc


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
