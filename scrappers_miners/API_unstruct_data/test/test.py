from sys import stdout

from elastic_search.es_models import DataHead


def main_m(*args, **kwargs):
    stdout.write("Running")
    print "running"


class TestClass(DataHead):
    def __init__(self, *args, **kwargs):
        print "Running 2"
        stdout.write("Running")
        super(TestClass, self).__init__(*args, **kwargs)
