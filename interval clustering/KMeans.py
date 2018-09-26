# -*- coding: utf-8 -*-

import numpy as np
from random import shuffle
from Hausdorff import dist, update_centroids, update_lambda

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def k_means_interval(lowers, uppers, number_of_cluster, iterations):

    number_of_sample = len(uppers)
    dim = len(uppers[0])
    vector_indices = list(range(number_of_sample))
    shuffle(vector_indices)

    # 初始化聚类中心
    centroids_upper = np.array([uppers[vector_indices[i]] for i in range(number_of_cluster)])
    centroids_lower = np.array([lowers[vector_indices[i]] for i in range(number_of_cluster)])

    # 初始化权重Lambda
    lamb = np.ones([dim])

    # 初始化样本归属
    tmp = dist(lowers, uppers, centroids_lower[0], centroids_upper[0], lamb)
    for k in range(1, number_of_cluster):
        distances = dist(lowers, uppers, centroids_lower[k], centroids_upper[k], lamb)
        tmp = np.vstack((tmp, distances))
    cluster = np.argmin(tmp, axis=0)

    test = 1
    iteration = 1
    while test != 0 or iteration < iterations:

        # 更新聚类中心
        for k in range(number_of_cluster):
            assignment = np.squeeze(np.where(cluster == k))

            [centroids_lower[k], centroids_upper[k]] = update_centroids(lowers, uppers, assignment)

        # 更新权重Lambda
        lamb = update_lambda(lowers, uppers, centroids_lower, centroids_upper, cluster, dim)

        test = 0
        tmp = dist(lowers, uppers, centroids_lower[0], centroids_upper[0], lamb)
        for k in range(1, number_of_cluster):
            distances = dist(lowers, uppers, centroids_lower[k], centroids_upper[k], lamb)
            tmp = np.vstack((tmp, distances))
        original_cluster = cluster
        cluster = np.argmin(tmp, axis=0)
        for i in range(number_of_sample):
            if cluster[i] != original_cluster[i]:
                test = test + 1
        print('iter =', iteration, 'test =', test)
        iteration = iteration + 1

    return cluster

# # 测试样本
# n_sample = 100
# n_clusters = 2
# iteration = 50
#
# center1 = [1, 1]
# center2 = [3, 3]
#
# data_u = []
# data_l = []
# data = [center1] + [center2]
# for i in range(int(n_sample/2)):
#     data.append([center1[0] + np.random.random() * 1 - 0.5, center1[1] + np.random.random() * 1 - 0.5])
#     r = np.random.random() * 0.5
#     data_u.append([data[-1][0] + r, data[-1][1] + r])
#     data_l.append([data[-1][0] - r, data[-1][1] - r])
#     data.append([center2[0] + np.random.random() * 1 - 0.5, center2[1] + np.random.random() * 1 - 0.5])
#     r = np.random.random() * 0.5
#     data_u.append([data[-1][0] + r, data[-1][1] + r])
#     data_l.append([data[-1][0] - r, data[-1][1] - r])
#
# result = k_means_interval(np.array(data_l), np.array(data_u), n_clusters, iteration)
#
# res={"x":[],"y":[],"kmeans_res":[]}
#
# for i in range(len(result)):
#     res["x"].append(data_u[i][0])
#     res["y"].append(data_u[i][1])
#     res["kmeans_res"].append(result[i])
# pd_res = pd.DataFrame(res)
# sns.lmplot("x","y",data=pd_res,fit_reg=False,size=5,hue="kmeans_res")
# plt.show()
