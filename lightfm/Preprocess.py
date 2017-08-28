"""
I am writing this additional python file to preprocess the data, for each unique user and item, we will generate a
gps_data and interactions, usernum, itemnum should be trasfered into this
"""

import pandas as pd
import numpy as np
import codecs
import math
import time
#from sklearn.crossw_validation import train_test_split
from math import radians, cos, sin, asin, sqrt
from scipy import sparse
import random

class Preprocess(object):

    def __init__(self ,n_users= 1082, n_venues=38332):
        assert n_venues > 0
        assert n_users > 0
        self.n_users = n_users
        self.n_venues = n_venues
        print("object preprocess created")

    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        :param lon1:
        :param lat1:
        :param lon2:
        :param lat2:
        :return:
        """
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371
        return c * r

    def get_dis(self, gps_data, poi_num, venue):
        """
        calculate every poi's distane to venue
        :param gps_data: venue_gps,dataframe
        :param poi_num: n_venues
        :param venue: the number of poi to be encoded
        :return: an distance array
        """
        dis_tmp = np.zeros(poi_num)
        poi = gps_data.loc[venue]
        i = 0
        # print(i)
        while i < poi_num:
            lat1 = poi['latitude']
            lon1 = poi['longitude']
            lat2 = gps_data['latitude'][i]
            lon2 = gps_data['longitude'][i]
            dis_tmp[i] = self.haversine(lon1, lat1, lon2, lat2)
            i = i + 1
        return (dis_tmp)

    def get_neighbor(self, interactions, gps_data,radius):
        """
        I will use this function to get a neighbor matrix for items in geographical sense
        :param interactions:
        :param gps_data:
        :return:
        """
        item_num = interactions.shape[1]
        neighbors = []
        for item in range(item_num):
            #print("calculate neighbor for item %d" % item)
            distances = self.get_dis(gps_data, item_num, item)
            neighbors.append(np.where(distances < radius))
        # to represent neighbors use: neighbors[userid][0], this is an array
        return neighbors

    def preprocess(self,interactions, gps_data, radius):

        start = time.clock()
        neighbors = self.get_neighbor(interactions, gps_data, radius)
        elapse = (time.clock() - start)
        print("get neighbor time used:", elapse)

        interactions = interactions.tocoo()
        usr_ids = interactions.row
        item_ids = interactions.col
        Y = interactions.data
        no_examples = Y.shape[0]
        negative_examples = []
        interactions = interactions.todense()
        for i in range(no_examples):
            usr_id = usr_ids[i]
            positive_item_id = item_ids[i]
            temp_neg = []
            #print(i)
            if not Y[i] > 0:
                continue
            for neighbor in neighbors[positive_item_id][0]:
                if interactions.item((usr_id, neighbor)) < 1:
                    temp_neg.append(neighbor)
            negative_examples.append(temp_neg)

        return (negative_examples)

        return (negtive_examples)


