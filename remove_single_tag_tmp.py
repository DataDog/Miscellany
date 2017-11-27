from datadog import initialize, api
import json

def removeSingleTag(myHost, myAPIKey, myAPPKey, tagToRemove):
    hostName = myHost

    options = {'api_key': myAPIKey,
               'app_key': myAPPKey}

    initialize(**options)


    myTagList = []                                                  # interim list to hold tags from host

    hosts = api.Infrastructure.search(q='hosts:' + hostName)        # Get tags by host id.

    myTags = api.Tag.get(hosts['results']['hosts'][0])

    for tag in myTags['tags']:                                      # Save tags to interim list
        myTagList.append(tag)

    myTagList.remove(tagToRemove)   

    api.Tag.delete(hostName)                                        # This deletes all tags from your host

    api.Tag.create(hosts['results']['hosts'][0], tags=myTagList)    # This adds back all of your other tags

if __name__=="__main__":

    removeSingleTag('HOSTNAME', 'API_KEY', 'APP_KEY','TAG')
