#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.metrics.pairwise import rbf_kernel
import random

def load_features_from_file(path):
        with open(path, 'r') as features_file:
                return [[float(feature) for feature in feature_set.split()] for feature_set in features_file.readlines()]    

def similarity_matrix_by_rbf(feature_set):
        return rbf_kernel(features, gamma=0.1)

def get_artist_indexes(artist_song, list_of_files):
        indexes = []

        artist_name = artist_song.split('/')[5].split('-')[0]
        with open(list_of_files, 'r') as list_of_files:
                all_files = list_of_files.readlines()
                for i in range(len(all_files)):
                        song_artist_name = all_files[i].split('/')[5].split('-')[0]
                        if all_files[i].split("|")[0].strip() == artist_song.strip():
                                continue
                        if song_artist_name == artist_name:
                                indexes.append(i)
        
        return indexes

def face_validity(path_list_of_files, similarity_matrix):
        expected_count = 0
        unexpected_count = 0

        with open(path_list_of_files, 'r') as list_of_files:
                all_files = list_of_files.readlines()
                for i in range(len(all_files)):
                        song_file = all_files[i]
                        same_artist_songs = get_artist_indexes(song_file.split('|')[0].strip(), path_list_of_files)                    
                        

                        if len(same_artist_songs) > 5:
                                different_artist_songs = random.sample([j for j in range(350) if j not in same_artist_songs], len(same_artist_songs))
                                same_artist_similarities = [similarity_matrix[i][k] for k in same_artist_songs]
                                different_artists_similarities = [similarity_matrix[i][l] for l in different_artist_songs]

                                same_artist_average = (sum(same_artist_similarities)/len(same_artist_similarities))
                                different_artists_average = (sum(different_artists_similarities)/len(different_artists_similarities))
                                print("Data for %s" % song_file)
                                print("Average similarity for same artist songs: %f" % same_artist_average)
                                print("Average similarity for different artists songs: %f" % different_artists_average)
                                print("-----------------")
                                
                                if same_artist_average > different_artists_average:
                                        expected_count += 1
                                else:
                                        unexpected_count += 1

        print("Number of times the same artist similarity was higher: %i" % expected_count)
        print("Number of times the different artists similarity was higher: %i" % unexpected_count)
                        
                        

if __name__ == "__main__":
        features = load_features_from_file('../files/all_features.txt')
        sm = similarity_matrix_by_rbf(features)

        face_validity('../files/top50s - ordered.txt', sm)