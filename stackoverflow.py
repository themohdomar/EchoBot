'''
    Python script to search StakeOverflow for any programming queries
    through the API - api.stackexchange.com

    - Created by : Mohammed Omar Mukthar
    - Version : 0.0.1 --- Initial Build

'''
# Packages to be imported :
# import json
import requests
# Global object declaration :
api_link = {'main': {'link': 'https://api.stackexchange.com',
                     'version': '2.3'},
            'path': {'search': ''},
            'parameters': {
                'order': 'desc',
                'sort': 'activity',
                'intitle': '',
                'site': 'stackoverflow'
            }
            }
def component_builder(components, build='link'):
    ''' Function to build different components
    of the URL based on the build type. Default
    build type is 'link', but can support URL
    parts like 'path','parameters'.

    RETURN (str) of all components based on the
    build.

    RETURN (None) if any error occurs

    :arg -- components : (dict) Input
                    iterable to be appended
                    based on the build.
         -- build : ['link','path','parameters']

    '''
    try:
        separator = {'link': '/',
                     'path': '/',
                     'parameters': '&'}
        result = ''
        if build == 'link':
            result = separator[build].join(components.values())
        elif build == 'path':
        # Else if block to be worked upon
            result = ''.join(components.keys())
        elif build == 'parameters':
            param = []
            for key, value in components.items():
                param.append(key + '=' + value)
            result += separator[build].join(param)
        else:
            pass
        return result
    except ValueError:
        print("URL component build failed -- Invalid Arguments passed")
        return None


def stackoverflow_consume(query):
    ''' Function to connect to the StakeOverflow API
        and run GET requests based on the input query
        and RETURN the various links obtained based
        on the Title provided with each link.

        RETURN "No data found" if GET request fails

        :arg -- query : (str) Input query string
                        based on which the GET
                        request is generated.
    '''

    api_link['parameters']['intitle'] = query
    # Append the dynamic parameters in the API Link
    link = component_builder(api_link['main'],'link')
    path = component_builder(api_link['path'],'path')
    parameters = component_builder(api_link['parameters'],'parameters')

    url = link+'/'+path+'?'+parameters
    print("URL :",url)
    response = requests.get(url)
    # response = requests.get("https://api.stackexchange.com/2.3/search?
    # order=desc&sort=activity&intitle=StopIteration&site=stackoverflow")
    print("*****************************************************************************")
    print("************************* Here is what I found ******************************")
    print("*****************************************************************************")
    items = (item for item in response.json()['items'])
    print("Search Query results with links")
    for item in items:
        print(item['title'])
        print(item['link'])
        print("*****************************************************************************")
