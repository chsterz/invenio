import sklearn.decomposition as deco
from sklearn.cluster import DBSCAN

from invenio.bibauthorid import bibauthorid_fast_extract

import numpy as np
import time


class BibauthorID_Fast_Clustering():
    ''' performs a compression of the given data and clusters the results quickly'''


    def __init__(self):
        #get data from the db, prepare clustering, encode and compress, finally cluster
        self.preprocessed_data = bibauthorid_fast_extract.postprocess_and_collate_authors()
        self.get_name_vector_lengths()
        self.generate_null_vector()	
        compressed_dimensions = 5
        self.compress_data( compressed_dimensions, self.encode_data(self.preprocessed_data) )
        self.labels = self.cluster()
        self.print_clusters()
    
    #an alphabet optimized for encoding names with maximum variance, 13 is missing data
    shuffle_alphabet = [16, 23, 22, 8, 14, 2, 6, 20, 15, 26, 7, 18, 21, 10, 11, 24, 0, 12, 17, 19, 9, 5, 25, 1, 4, 3]

    #the value encoding missing_data
    missing_data = 13

    #lenghts of the name vectors(retrieved from data)
    name_vector_lengths = [0, 0, 0, 0]

    #vector containing no data, to be copied and filled
    null_vector = []

    #data reduced to the first prevalent eigenvectors
    compressed_data = []


    def get_name_vector_lenghts(self):
	''' gets the lengths of the longest first, middle, middle, and last name '''
        for name, dummy, dummy in self.preprocessed_data:
            parts = name.split(" ")
            
            #we only consider first, last and two middle names, the rest gets deleted
            part_number = len(parts)
            if( partnumber > 4 ): del parts[2:-2]
            
            #last name is given most often
            last_name_length = len(parts[3])
            if( last_name_length > self.name_vector_lengths[3]): self.name_vector_lengths[3] = last_name_length

            #if there is no first name, continue
            if( partNumber <= 1 ): continue
            first_name_length = len(parts[0])
            if( last_name_length > self.name_vector_lengths[0]): self.name_vector_lengths[0] = first_name_length

            #if there is no mid1 name, continue
            if( partNumber <= 2 ): continue
            mid1_name_length = len(parts[1])
            if( last_name_length > self.name_vector_lengths[1]): self.name_vector_lengths[3] = mid1_name_length

            #if there is no mid2 name, continue
            if( partNumber <= 3 ): continue
            mid2_name_length = len(parts[2])
            if( last_name_length > self.name_vector_lengths[2]): self.name_vector_lengths[2] = mid2_name_length 


    def generate_null_vector(self):
        ''' fills the nullvector with missing data '''
        for i in range(sum(self.null_vector)):
            self.nullvector.append(self.missing_data)


    def encode_character(self):
        ''' applies the enoding maximising the variance in the given name encoding '''
        return self.shuffleAlphabet[ ord(char) - 65 - 32]


    def name_vector(self, name)
        ''' transforms the name string into a consistent vector '''
        name =  name.strip()
        parts = name.split(" ")
        part_number = len(parts)
        vector = self.null_vector[:]
	
	#again, we only consider first, last and two middle names, the rest gets deleted
            part_number = len(parts)
            if( partnumber > 4 ): del parts[2:-2]

	#encode last name, starts at the point where all the previous nameparts stop
        #we set weights descending with 0.5 steps from 10 for the name
        start_offset = self.name_vector_lengths[0] + self.name_vector_lengths[1] + self.name_vector_lengths[2] - 1
        for i in range(len(parts[-1])):
            weight = max( 1, 10 - (0.5*i) )
            vector[start_offset + i] = self.encode_character(parts[-1][i])
        
        #if there is no first name, continue
        #putting more weight on the first letter as initial
        if( part_number <=1 ): return vector
        start_offset = 0
        for i in range(len(parts[0])):
            weight = 5 if i==0 else 2
            vector[start_offset + i] = self.encode_character(parts[0][i])

        #if there is no mid1 name, continue
        #more weight on the first letter
        if( part_number <= 2 ): return vector
        start_offset = self.name_vector_lengths[0] - 1
        for i in range(len(parts[1])):
            weight = 3 if i==0 else 0.5
            vector[start_offset + i ] = self.encode_character(parts[1][i])

        #if there is no mid2 name, continue
        #more weight on the first letter
        if( part_number <= 3): return vector
        start_offset = self.name_vector_lengths[0] + self.name_vector_lengths[1]
        for i in range(len(parts[2])):
            weight = 2 if i==0 else 0.5
            vector[start_offset + i ] = self.encode_character(parts[2][i])

        return vector


    def encode_data(self)
        ''' encode the names, returning a purely numerical matrix '''
        #create a matrix the size (#vectors x vectorlength)
        encoded_data = np.array( len(self.preprocessed_data), sum(self.name_vector_lengths) )
        for index, dataset in enumerate(self.preprocessed_data):
            encoded_data[index] = self.name_vector( dataset[0] )


    def compress_data(self, target_vector_length, matrix):
        ''' analyzes the data and transform it down to a specified number of dimensions '''
        pca = deco.PCA(target_vector_length)
        pca = pca.fit(matrix)
        return pca.transform(matrix)


    def cluster(self)
        ''' use DBSCAN for clustering '''
        dbscan = DBSCAN(eps=0.7, algorithm="kd_tree").fit(self.reduced_data)
        return dbscan.labels_


    def print_clusters(self)
        ''' print the first 50 clusters for visual checking '''
        for cluster in range(50):
            print "cluster", cluster, ":"
            print "=============="
            for i in range(len(self.labels)):
                if (labels[i] == label):
                    print self.preprocessed_data[label]
            print("\n")
            
