This folder contains code and sample json files to convert json dumps from Apollo (http://apollo3.cs.illinois.edu/) to media datasets.

The main script is ./code/read_apollo_dump.py
Dependencies on non-builtin modules is documented in dependencies.txt. Modules can installed using

```shell
$ pip install -r dependencies.txt
```

Currently only instagram, youtube and embedded twitter image interfaces are implemented. Also, with arbitrary web-pages, we download the largest image found on the web-page. Code for this is adapted with thanks from Tanvir Al Amin of UIUC.

Planning to add support for Vine, Imgur, TinyPIC as the need arises.

To download embedded twitter images from apollo dumps, run download_twitter_embedded_media.py.

Requirements:
* Twitter credentials can be retrieved from  https://apps.twitter.com/. The link http://blog.igalvez.net/generating-twitter-api-credentials/ has guidlines on how one can get the credentials.

* Create a private copy of generate_twitter_key_pickle_public.py, populate with twitter API keys and secrets and run to generate myTwitterKeys.p pickle file. This is done to avoid publishing twitter API credentials on Github.

*  Your myTwitterKeys.p should now be ready to use in download_twitter_embedded_media.py

* Two .json files get created with this script:
** XYZ_w_emb_media_file.json : contains apollo style json metadata with the field 'media_links' populated
** XYZ_complete_twitter_data.json : contains complete meta-data as provided by the twitter API



