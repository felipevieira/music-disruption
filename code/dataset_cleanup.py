import sys
import os
import re
import shutil

from operator import itemgetter

def remove_entries_without_age_info(path):
    with_info = 0
    no_info = 0
    with open('list_albums.txt','w') as list_albums:
        with open('list_songs.txt', 'w') as list_songs:
            my_data = sorted(os.walk(path),key=itemgetter(0))
            for directory in my_data:
                match = re.match(r'.*([1-3][0-9]{3})', os.path.basename(directory[0]))
                if not match:
                    print("veio")
                    #MUDAR ISSO PRO DIRETORIO ATUAL!!!
                    if directory[0] == '/home/felipev/datasets/forro em vinil resampled/':
                        continue
                    else:
                        pass
                        # shutil.rmtree(directory[0])
                else:
                    list_albums.write("%s\n" % os.path.basename(directory[0]))

                    year = re.match(r'.*([1-3][0-9]{3})', directory[0]).group(1)
                    the_directory = os.path.basename(directory[0])
                    # filename = "[%s] - %s" % (year, os.path.basename(directory[0]))

                    for song in directory[2]:
                        if song.endswith(".mp3") or song.endswith(".wma") or song.endswith(".ogg"):
                            list_songs.write("%s | %s | %s\n" % (year, the_directory, song))
                    
                    # new_filename = os.path.join(the_directory, filename)
                    # os.rename(directory[0], new_filename) 


            


if __name__ == "__main__":
    remove_entries_without_age_info(sys.argv[1])