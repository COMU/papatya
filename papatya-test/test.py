import os



path_to_papatya="/home/zafer/papatya"

os.environ['DJANGO_SETTINGS_MODULE'] = 'papatya.settings'
sys.path.insert(0, path_to_papatya)

from papatya.songs.models import *


for root, directory, files in os.walk(path_to_papatya):
    pass
