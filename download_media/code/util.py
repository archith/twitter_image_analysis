import os, shutil


class Config:
    def __init__(self, overwrite_media=False, download_images=True, download_videos=True):
        self.verbose_debug = False
        self.overwrite_media = overwrite_media
        self.download_images = download_images
        self.download_videos = download_videos

        self.download_instagram = self.download_images
        self.download_imgur = self.download_images
        self.download_tinypic = self.download_images

        self.download_yt = self.download_videos

    def set_instagram_flag(self, download_instagram=True):
        self.download_instagram = download_instagram

    def set_imgur_flag(self, download_imgur=True):
        self.download_imgur = download_imgur

    def set_download_tinypic(self, download_tinypic=True):
        self.download_tinypic = download_tinypic

    def set_download_yt(self, download_yt=True):
        self.download_yt = download_yt

    def set_verbose_debug(self, verbose_debug=False):
        self.verbose_debug = verbose_debug


# simple utility functions

def get_media_file_paths(json_file_path):
    json_file_path = os.path.abspath(json_file_path)

    out_folder_name = os.path.basename(json_file_path).replace('.', '_')
    out_folder_path = os.path.dirname(json_file_path)

    hdf5_file_name = out_folder_name + '.h5'
    new_hdf5_file_name = os.path.basename(hdf5_file_name).split('.')[0] + '_media.h5'

    hdf5_file_path = os.path.join(out_folder_path, out_folder_name, hdf5_file_name)
    out_img_folder = os.path.join(out_folder_path, out_folder_name, 'images')
    out_video_folder = os.path.join(out_folder_path, out_folder_name, 'videos')

    dbg_xl_file_path = os.path.join(out_folder_path, out_folder_name + '_dbg.xlsx')

    return hdf5_file_path, out_img_folder, out_video_folder, dbg_xl_file_path


def create_media_folders(img_folder_path, video_folder_path, config=Config()):
    if not os.path.exists(img_folder_path):
        os.makedirs(img_folder_path)
    else:
        if (config.overwrite_media):
            shutil.rmtree(img_folder_path)
            os.makedirs(img_folder_path)

    if not os.path.exists(video_folder_path):
        os.makedirs(video_folder_path)
    else:
        if (config.overwrite_media):
            shutil.rmtree(video_folder_path)
            os.makedirs(video_folder_path)


if __name__ == "__main__":
    json_file = '/home/archith/work/twitter_image_analytics/primaries_1/tweets_sample.json'
    x, y, z, a = get_media_file_paths(json_file)
    b = 2
