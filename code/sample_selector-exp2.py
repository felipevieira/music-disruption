import os
import re
import subprocess


def write_all_files(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.mp3' in file or '.wma' in file:
                album = r.split("/")[5]
                match = re.search('\d{4}', album)
                year = match.group(0) if match else None
                
                if year:       
                    files.append((os.path.join(r, file), int(year)))
    files = sorted(files, key=lambda x: x[1])

    with open('../files/exp-2/all_files.txt', 'w') as my_file:
        for item in files:
            my_file.write("%s\n" % (item[0]))

def create_segmented_files(path, n_segments):
    with open(path, 'r') as list_of_files:
        the_files = list_of_files.readlines()
        for i in range((len(the_files) / n_segments)+1):
            with open('../files/exp-2/segmented/files-%i.txt' % (i+1), 'w') as segmented_file:
                for single_file in the_files[n_segments*i:n_segments*i+n_segments]:
                    segmented_file.write(('%s\n' % single_file.strip()))

def atoi(text):
        return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def extract_features_for_segments(segmented_features_path):
    for r, d, f in os.walk('../files/exp-2/segmented'):
        f.sort(key=natural_keys)
        for i in range(len(f)):
            if i==101:
                file = f[i]
                subprocess.call(['python', '/home/felipev/workspace/transfer_learning_music/easy_feature_extraction.py', '/home/felipev/workspace/music-disruption/files/exp-2/segmented/files-%i.txt' % (i+1) , '/home/felipev/workspace/music-disruption/files/exp-2/segmented_features/features-%i.npy' % (i+1), '10'], cwd="/home/felipev/workspace/transfer_learning_music")


def combine_feature_files(feature_path):
    # with open(feature_path, 'r') as feature_file:
    features_files = os.listdir(feature_path)
    features_files.sort(key=natural_keys)
    
    with open('../files/exp-2/all_features.txt', 'w') as outfile:
        for fname in features_files:
            with open(os.path.join(feature_path, fname)) as infile:
                for line in infile.readlines():
                    outfile.write('%s\n' % line.strip())

if __name__ == "__main__":
    # my_files = write_all_files('/home/felipev/datasets/forro em vinil')    
    # create_segmented_files('../files/exp-2/all_files.txt', 100)

    # extract_features_for_segments('../files/exp-2/segmented_features/')

    combine_feature_files('/home/felipev/workspace/music-disruption/files/exp-2/segmented_features')
