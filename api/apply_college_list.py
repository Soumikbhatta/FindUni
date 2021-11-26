from sklearn.neighbors import NearestNeighbors
import csv
import pandas as pd
import pickle
import numpy as np
import math
import os
from django.conf import settings
import joblib

model = joblib.load(os.path.join(settings.PROJECT_ROOT,
                    "train/CollegeProbPredictor.joblib"))

datPoints = pd.read_csv(os.path.join(
    settings.PROJECT_ROOT, "train\\ClusteredDataWithTiers.csv"))
datPoints = datPoints.drop(['Cluster'], axis=1)
Scores = [4, 159, 165, 4.5]


def predictListCollege(Scores):
    Scores = list(map(float, Scores.split(' ')))
    Scores = np.asarray(Scores).reshape(1, -1)
    ProbMax = max(max(model.predict_proba(Scores)))
    tier = model.predict(Scores)[0]
    CollegeTierList = {}
    if(tier == '5'):
        nTier = 10
        Neigh1 = NearestNeighbors(
            n_neighbors=nTier, p=2, algorithm='auto', metric='euclidean')
        TierUpperPoints = datPoints[datPoints["Tier"]
                                    == int(tier)].reset_index(drop=True)
        Neigh1.fit(np.asarray(TierUpperPoints.drop(
            ['Unnamed: 0', 'College Name', 'Tier'], axis=1).values))
        Indexes = Neigh1.kneighbors(Scores, return_distance=False)[0]
        CollegeList = [TierUpperPoints.at[i, 'College Name'] for i in Indexes]
        UTier = []
        for Name in CollegeList:
            College = {}
            College["Verbal"] = datPoints[datPoints["College Name"]
                                          == Name]["Verbal"].values[0]
            College["Quants"] = datPoints[datPoints["College Name"]
                                          == Name]["Quants"].values[0]
            College["GPA"] = datPoints[datPoints["College Name"]
                                       == Name]["GPA"].values[0]
            College["Writing"] = datPoints[datPoints["College Name"]
                                           == Name]["Writing"].values[0]
            College["CollegeName"] = Name
            UTier.append(College)
        CollegeTierList[tier] = UTier
    else:
        nTier = int(math.ceil(ProbMax*10))
        nTierLower = int(10-nTier)
        Neigh1 = NearestNeighbors(
            n_neighbors=nTier, p=2, algorithm='auto', metric='euclidean')
        TierUpperPoints = datPoints[datPoints["Tier"]
                                    == int(tier)].reset_index(drop=True)
        Neigh1.fit(np.asarray(TierUpperPoints.drop(
            ['Unnamed: 0', 'College Name', 'Tier'], axis=1).values))
        Indexes = Neigh1.kneighbors(Scores, return_distance=False)[0]
        CollegeList = [TierUpperPoints.at[i, 'College Name'] for i in Indexes]
        UTier = []
        for Name in CollegeList:
            College = {}
            College["Verbal"] = datPoints[datPoints["College Name"]
                                          == Name]["Verbal"].values[0]
            College["Quants"] = datPoints[datPoints["College Name"]
                                          == Name]["Quants"].values[0]
            College["GPA"] = datPoints[datPoints["College Name"]
                                       == Name]["GPA"].values[0]
            College["Writing"] = datPoints[datPoints["College Name"]
                                           == Name]["Writing"].values[0]
            College["CollegeName"] = Name
            UTier.append(College)
        Neigh2 = NearestNeighbors(
            n_neighbors=nTierLower, p=2, algorithm='auto', metric='euclidean')
        TierLowerPoints = datPoints[datPoints["Tier"]
                                    == (int(tier)+1)].reset_index(drop=True)
        Neigh2.fit(np.asarray(TierLowerPoints.drop(
            ['Unnamed: 0', 'College Name', 'Tier'], axis=1).values))
        Indexs2 = Neigh2.kneighbors(Scores, return_distance=False)[0]
        CollegeList2 = [TierLowerPoints.at[i, 'College Name'] for i in Indexs2]
        LTier = []
        for Name in CollegeList2:
            College = {}
            College["Verbal"] = datPoints[datPoints["College Name"]
                                          == Name]["Verbal"].values[0]
            College["Quants"] = datPoints[datPoints["College Name"]
                                          == Name]["Quants"].values[0]
            College["GPA"] = datPoints[datPoints["College Name"]
                                       == Name]["GPA"].values[0]
            College["Writing"] = datPoints[datPoints["College Name"]
                                           == Name]["Writing"].values[0]
            College["CollegeName"] = Name
            LTier.append(College)
        CollegeTierList[tier] = UTier
        if(LTier != []):
            CollegeTierList[str(int(tier)+1)] = LTier

    return CollegeTierList
