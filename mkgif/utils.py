import os
from django.conf import settings


def mk_gif_ffmpeg(params):
    #path: where in the file system the files we are dealing with reside:
    #every animation has its own folder, so here we are trying to point to where the files are:
    #using "" here just because Im alrady using '' outside
    path = settings.MEDIA_ROOT / f'{params["pk"]}'
    command = f'ffmpeg -framerate 60 -pattern_type glob -y -i "{path}/*.png" -r 15 -vf scale=512:-1 {path}/out.gif'
    print(path, params)
    print(command)
    #we use the os system to run the command
    os.system(command)
