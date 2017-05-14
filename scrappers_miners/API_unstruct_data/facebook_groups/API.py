from urlparse import urlparse
import time

import facebook
import requests

from scrappers_miners.utils.utils import APIHead, NLP
from scrappers_miners.API_unstruct_data.facebook_groups.es_structure import Facebook

FACEBOOK_APP_ID = '424282464597672'
FACEBOOK_APP_SECRET = '1bae9480566ded0bee7d0c895798a18a'


class FacebookAPI(APIHead):
    @staticmethod
    def get_token():
        try:
            oauth_args = dict(client_id=FACEBOOK_APP_ID,
                              client_secret=FACEBOOK_APP_SECRET,
                              grant_type='client_credentials')
            r = requests.get("https://graph.facebook.com/oauth/access_token", params=oauth_args)
            return r.json()['access_token']
        except:
            raise Exception(r.json().get('error', {}).get('message', ""))

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

        if self.ex_details:
            ex_data = self.ex_details
        else:
            raise Exception("No Argument - 'ex_details' provided")

        self.graph = facebook.GraphAPI(access_token=self.get_token(), version='2.8')
        self.data_iterator = self.get_keywords_for_groups(ex_data['data'])

    @staticmethod
    def get_group_fields():
        return ','.join(Facebook.group_detail_list)

    @staticmethod
    def get_post_fields():
        return ','.join(Facebook.post_extra_data)

    @staticmethod
    def get_group_id(group_link_dict):
        group_link = group_link_dict['link']
        path = urlparse(group_link).path.split('/')
        try:
            i = path.index('groups')
            return path[i + 1], group_link_dict.get('update_time', None)
        except Exception as e:
            raise Exception("Error in fetching group_link. [%s]" % e.message)

    def get_group_details(self, group_id, fields):
        return self.graph.get_object(id=group_id, fields=fields)

    def get_keywords_for_groups(self, groups):
        for group_dict in groups:
            if group_dict['active']:
                group, last_update_time = self.get_group_id(group_dict)

                group_details = self.get_group_details(group, self.get_group_fields())

                posts = self.graph.get_all_connections(id=group, connection_name='feed',
                                                       fields=self.get_post_fields(), since=last_update_time)

                for post in posts:
                    post_message = post.get('message', None)

                    if post_message:
                        nlp = NLP(post_message)
                        filter_flag, tokens = nlp.filter_relevant()

                        if filter_flag:
                            entities = nlp.get_entities()
                            keywords = nlp.get_keywords()

                            f = Facebook(source="Facebook",
                                         link=post.get('permalink_url', None),
                                         msg=post_message,
                                         create_time=post.get('updated_time'),
                                         keywords=keywords,
                                         group_name=group_details.get('group_name'),
                                         location=entities.get('LOC', []),
                                         organisation=entities.get('ORG', [])
                                         )
                            # print keywords
                            yield f

                # Update Time for group
                group_dict['update_time'] = int(time.time())
