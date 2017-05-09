from urlparse import urlparse
import time

import facebook
import nltk
import requests

from scrappers_miners.utils.utils import APIHead
from scrappers_miners.API_unstruct_data.facebook_groups.es_structure import Facebook

FACEBOOK_APP_ID = '424282464597672'
FACEBOOK_APP_SECRET = '1bae9480566ded0bee7d0c895798a18a'


class FacebookGroupCrawler(object):
    def __init__(self, app_id, app_secret, version='2.8'):

        oauth_args = dict(client_id=FACEBOOK_APP_ID,
                          client_secret=FACEBOOK_APP_SECRET,
                          grant_type='client_credentials')
        r = requests.get("https://graph.facebook.com/oauth/access_token", params=oauth_args)
        try:
            access_token = r.json()['access_token']
            self.graph = facebook.GraphAPI(access_token=access_token, version=version)
        except KeyError as e:
            raise Exception(r.json().get('error', {}).get('message', ""))
        else:
            self.groups = []
            self.grammar = r"""
            NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
            PP: {<IN><NP>}               # Chunk prepositions followed by NP
            VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
            CLAUSE: {<NP><VP>}           # Chunk NP, VP
            """
            self.cp = nltk.RegexpParser(self.grammar)
            self.keywords = {}

    @staticmethod
    def get_group_fields():
        return ','.join(Facebook.group_detail_list)

    @staticmethod
    def get_post_fields():
        return ','.join(Facebook.post_extra_data)

    def get_keywords_for_groups(self, groups):
        for group_dict in groups:
            if group_dict['active']:
                group, last_update_time = self.get_group_id(group_dict)
                self.keywords[group] = {}

                self.keywords[group]['group_details'] = self.get_group_details(group, self.get_group_fields())
                self.keywords[group]['posts'] = {}

                posts = self.graph.get_all_connections(id=group, connection_name='feed',
                                                       fields=self.get_post_fields(), since=last_update_time)

                for post in posts:
                    post_message = post.get('message', None)
                    post_id = post.get('id')
                    post_update_time = post.get('updated_time')

                    self.keywords[group]['posts'][post_id] = {
                        'post_details': post,
                        'keywords': [],
                        'group_name': self.keywords[group]['group_details']['name']
                    }

                    if post_message:
                        sentences = self.process_text(post_message)
                        for sen in sentences:
                            result = self.cp.parse(sen)
                            self.traverse(result, group, post_id)

                # Update Time for group
                group_dict['update_time'] = int(time.time())
        # TODO: Return message, post link, post_time, group_name get all post related data
        return self.keywords

    @staticmethod
    def get_group_id(group_link_dict):
        group_link = group_link_dict['link']
        path = urlparse(group_link).path.split('/')
        try:
            i = path.index('groups')
            return path[i + 1], group_link_dict.get('update_time', None)
        except Exception as e:
            raise Exception("Error in fetching group_link. [%s]" % e.message)

    @staticmethod
    def process_text(text):
        sentences = nltk.sent_tokenize(text)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        return sentences

    def traverse(self, t, group, post_id):
        try:
            t.label()
        except AttributeError:
            return
        else:
            # Now we know that t.node is defined
            if t.label() == 'NP':
                self.keywords[group]['posts'][post_id]['keywords'].append(
                    ' '.join([leave for leave, typ in t.leaves()]))
            for child in t:
                self.traverse(child, group, post_id)

    def get_group_details(self, group_id, fields):
        return self.graph.get_object(id=group_id, fields=fields)


class FacebookAPI(APIHead):
    def execute(self):
        """
        ex_details: {
            data: [
                {
                    'link': '[complete_link]',
                    'update_time: '[UNIX_TIMESTAMP]',
                    'active': '[Boolean]'
                }
            ]
        }
        """

        # TODO: Get Group Details

        if self.ex_details:
            ex_data = self.ex_details
        else:
            raise Exception("No Argument - 'ex_details' provided")

        fb = FacebookGroupCrawler(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)

        post_key_words = fb.get_keywords_for_groups(ex_data['data'])

        post_objs = []

        for group_id, v in post_key_words.items():
            posts = post_key_words[group_id]['posts']
            for post_id, value in posts.items():
                f = Facebook(
                    source="Facebook",
                    link=value['post_details']['permalink_url'],
                    msg=value['post_details'].get('message', None),
                    create_time=value['post_details']['updated_time'],
                    keywords=value['keywords'],
                    group_name=value['group_name'],
                )
                post_objs.append(f)

        self.data_iterator = post_objs
