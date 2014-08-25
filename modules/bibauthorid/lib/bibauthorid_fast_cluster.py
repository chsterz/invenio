import sklearn.decomposition as deco
from sklearn.cluster import DBSCAN

from invenio.bibauthorid import bibauthorid_fast_extract

import numpy as np
import pickle
import time


class BibauthorID_Fast_Clustering():
    ''' performs a compression of the given data and clusters the results quickly'''

    def __init__(self):
        self.preprocessed_data = bibauthorid_fast_extract.postprocess_and_collate_authors()
        self.get_name_vector_lengths()
        self.generate_null_vector()
        self.compress_data()
    
    #an alphabet optimized for encoding names with maximum variance, 13 is missing data
    shuffle_alphabet = [16, 23, 22, 8, 14, 2, 6, 20, 15, 26, 7, 18, 21, 10, 11, 24, 0, 12, 17, 19, 9, 5, 25, 1, 4, 3]

    #the value encoding missing_data
    missing_data = 13

    #lenghts of the name vectors(retrieved from data)
    name_vector_lengths = [0, 0, 0, 0]

    #vector containing no data, to be copied and filled
    null_vector = []

    #data reduced to the first prevalent eigenvectors
    reduced_data = []


    def encode_character(self):
        ''' applies the enoding maximising the variance in the given name encoding '''
        return self.shuffleAlphabet[ ord(char) - 65 - 32]


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


