import pickle

print ('Create your own copy of this file with the correct values of twitter keys filled in!')
key_dict = {'consumer_key': 'your_consumer_key',
            'consumer_secret': 'your_consumer_secret',
            'access_key': 'your_access_key',
            'access_secret': 'your_access_secret'}

pickle.dump(key_dict, open('myTwitterKeys.p', "wb"))