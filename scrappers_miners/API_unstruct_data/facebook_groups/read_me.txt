To start scrapping Facebook Groups:
1. Login into Admin Panel at gojobi.de/verwalter

2. Under Data Tab, Click on Sources.

3. Add a new Source, Click on Add Source +

Fields in The form are as follows:

Name: Name of the source
Verbose Name: ALternative name
Ds Type: Data Structure Type (Select API without Stuctured Data for Facebook)
Miner Class: Points to a class in Code which will execute Mining Process (Set facebook_groups.API.FacebookAPI)

ex_details: This is a list of objects which represent a Facebook Group.
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
            Link: Facebook Group Link (Eg. https://www.facebook.com/groups/115194395496242/)
            Update Time: Unix Timestamp when the group was last scrapped. (Set 0 initially)
            active: A flag for overriding the scrapper to skip a group. (Set True to Scrap)

Es Structure: Points to a class in Code which is used as Model to store a document in Elasticsearch (Set facebook_groups.es_structure.Facebook)
refresh_rate: Time after which the groups will be scrapped again. (In minutes)
Counter: A Counter for successful completion of scrapper.
error_counter: A couter for unsuccessful completion of scrapper.
Active: A flag that signifies that scrapper is running in the background. (Set False)

4. Press Save.
