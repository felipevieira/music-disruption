#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
from networkx.drawing.nx_pylab import draw_networkx

from face_validity import *

SONGS_PER_DECADE = 50 

def generate_network(listfiles, similarity_matrix):
    slice_index = 0
    G = nx.DiGraph()

    with open(listfiles, 'r') as list_of_files:
        song_files = list_of_files.readlines()

        for i in range(len(song_files)):
            G.add_node(i)

        for i in range(0, 7):
            if i==0:
                continue
            similarities_for_decade_slice = similarity_matrix[SONGS_PER_DECADE*i : SONGS_PER_DECADE*i+SONGS_PER_DECADE]
            comparison_range = range(0, SONGS_PER_DECADE*i)

            for j in range(len(similarities_for_decade_slice)):
                for k in comparison_range:
                    if similarities_for_decade_slice[j][k] > 0.80:
                        current_song = song_files[SONGS_PER_DECADE*i + j].split("|")[0].strip().split('/')[-1]
                        previous_song = song_files[k].split("|")[0].strip().split('/')[-1]

                        G.add_edge(SONGS_PER_DECADE*i + j, k)
    return G

def get_disruption_index_for_nodes(listfiles, graph):
    disruption_info = {}
    with open(listfiles, 'r') as list_of_files:
        song_files = list_of_files.readlines()
        song_files = [song.split("|")[0].strip() for song in song_files]

        for i in range(len(song_files)):

            decade = (i/SONGS_PER_DECADE) + 1
            
            songs_after = song_files[i+1:]
            song_influences = [edge[1] for edge in graph.edges(song_files[i])]

            ni = 0
            nj = 0
            nk = 0
            
            for song_after in songs_after:
                consolidating_influence = False
                if graph.has_edge(song_after , song_files[i]):
                    for influence in song_influences:
                        if graph.has_edge(song_after, influence):
                            consolidating_influence = True
                            break
                    if consolidating_influence:
                        nj+=1
                    else:
                        ni+=1
                else:
                    for influence in song_influences:
                        if graph.has_edge(song_after, influence):
                            nk+=1
            
            disruption_info[song_files[i]] = [ni, nj, nk, float((ni-nj)) / float((ni+nj+nk))] if (ni+nj+nk) > 0 else [ni, nj, nk, 0]
    
    return disruption_info

if __name__ == "__main__":
    import collections

    features = load_features_from_file('../files/all_features.txt')
    sm = similarity_matrix_by_rbf(features)

    g = generate_network('../files/top50s - ordered.txt', sm)
    di = get_disruption_index_for_nodes('../files/top50s - ordered.txt', g)
    
    sorted_x = sorted(di.items(), key=lambda kv: (kv[1][3], kv[1][0]), reverse=True)
    sorted_dict = collections.OrderedDict(sorted_x)
    
    # for song in sorted_dict.keys():
    #     print "%s - %s" % (song, sorted_dict[song])
    
    # nx.write_gexf(g, "test.gexf")
