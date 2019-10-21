from face_validity import *


def generate_network(listfiles, similarity_matrix):
    slice_index = 0
    G = nx.DiGraph()

    with open(listfiles, 'r') as list_of_files:
        song_files = list_of_files.readlines()

        for i in range(len(song_files)):
            G.add_node(i)
            for j in range(i, len(song_files)):
                if similarity_matrix[i][j] > 0.8:
                    G.add_edge(j, i)
    return G

def get_disruption_index_for_nodes(listfiles, graph):
    disruption_info = {}
    with open(listfiles, 'r') as list_of_files:
        song_files = list_of_files.readlines()
        song_files = [song.split("|")[0].strip() for song in song_files]

        for i in range(len(song_files)):        
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

    features = load_features_from_file('../files/exp-2/all_features.txt')
    sm = similarity_matrix_by_rbf(features)

    # g = generate_network('../files/top50s - ordered.txt', sm)
    # di = get_disruption_index_for_nodes('../files/top50s - ordered.txt', g)
    
    # sorted_x = sorted(di.items(), key=lambda kv: (kv[1][3], kv[1][0]), reverse=True)
    # sorted_dict = collections.OrderedDict(sorted_x)
    
    # for song in sorted_dict.keys():
    #     print "%s - %s" % (song, sorted_dict[song])
    
    # nx.write_gexf(g, "test.gexf")
