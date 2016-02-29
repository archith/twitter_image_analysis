import tables


class UrlEntry(tables.IsDescription):
    short_url = tables.StringCol(500)
    long_url = tables.StringCol(500)
    url_domain = tables.StringCol(500)
    tweet_string = tables.StringCol(140)
    tweet_id = tables.Int64Col()
    screen_name = tables.StringCol(500)
    media_downloaded = tables.BoolCol()
    media_file_paths = tables.StringCol(500)


class UrlTable:
    def __init__(self, file_name='tmp.h5', mode='w', title='tmp title'):
        self.h5file = tables.open_file(file_name, mode=mode, title=title)
        self.group = self.h5file.create_group("/", 'url_group', 'URL information')
        self.table = self.h5file.create_table(self.group, 'readout', UrlEntry, "Readout example")


INSTAGRAM_DOM = 'www.instagram.com'
YOUTUBE_DOM = 'www.youtube.com'
IMGUR_DOM = 'www.imgur.com'
TINYPIC_DOM = 'www.tinypic.com'
