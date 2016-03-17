import pickle

key_dict = {'consumer_key': 'Y8k2xCtglBTyTnIpigNfb2A6p',
            'consumer_secret': 'mavRaSlnccRNJFYQtSZvp8y1mqj77r4cb8CA2XwteGcLbqOBvi',
            'access_key': '2585122411-CbNjeV5aydqfBzgZcWazuG0TctE6dmfrRY6ISeg',
            'access_secret': 'qaVRSc5wjOV2HGtV3yghcbH9V0iQDTAIsiXTVqdFqsBPq'}

pickle.dump(key_dict, open('myTwitterKeys.p', "wb"))
