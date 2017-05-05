import abc


class APIHead(object):
    def __init__(self, *args, **kwargs):
        self.ex_details = kwargs.get('ex_details')
        self.data_iterator = None
        self.traceback_info = None

    @abc.abstractmethod
    def execute(self):
        """
        :returns list of items to be fed in ElasticSearch or a generator for the same.
        """
        raise NotImplementedError('Please implement this method in class "%s"' % self.__class__.__name__)

    def get_ex_details(self):
        return self.ex_details

    def get_data(self):
        return self.data_iterator

    def get_traceback(self):
        return self.traceback_info
