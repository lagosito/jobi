from elasticsearch_dsl import DocType, Text, Date


class Data(DocType):
    source = Text()
    link = Text()
    msg = Text()
    info = 0
    create_time = Date()
