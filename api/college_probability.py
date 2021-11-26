import pandas as pd
import csv
from scipy import spatial
import numpy as np
import os
from django.conf import settings


def index2d(list2d, value):
    return next((i, j) for i, lst in enumerate(list2d)
                for j, x in enumerate(lst) if x == value)

CollegeTiers = []

# with open('train/CollegeTiers.csv') as csv_file:
with open(os.path.join(settings.PROJECT_ROOT, 'train/CollegeTiers.csv')) as csv_file:
    csv_reader2 = csv.reader(csv_file, delimiter=',')
    for row in csv_reader2:
        CollegeTiers.append(row[1:])

# datPoints = pd.read_csv("train/CleanedDataFinal.csv")
datPoints = pd.read_csv(os.path.join(settings.PROJECT_ROOT, 'train/CleanedDataFinal.csv'))
CollegeScores = pd.read_csv(os.path.join(settings.PROJECT_ROOT, 'train/ClusteredDataWithoutTiers.csv'))

datPoints["Tier"] = ""
for i,j in CollegeTiers:
    datPoints["Tier"] = datPoints["Tier"].mask(datPoints["College Name"] == i, j)

def CollegeProb(CollegeName, Scores):       # Scores - "GPA Verbal Quants Writing"
    Scores = list(map(float,Scores.split(' ')))
    NeededTier = CollegeTiers[index2d(CollegeTiers,CollegeName)[0]][1]
    
    NeededVerbal = CollegeScores[CollegeScores["College Name"] == CollegeName]["Verbal"]
    NeededQuants = CollegeScores[CollegeScores["College Name"] == CollegeName]["Quants"]
    NeededGPA = CollegeScores[CollegeScores["College Name"] == CollegeName]["GPA"]
    NeededWriting = CollegeScores[CollegeScores["College Name"] == CollegeName]["Writing"]


    DistFromTiers = {}

    for y,x in datPoints.groupby("Tier"):
        v= np.triu(spatial.distance.cdist(x[['GPA','Verbal','Quants','Writing']].values, [Scores]),k=0)

        v = np.mean(np.ma.masked_equal(v, 0))
        DistFromTiers[y] = v
    sumDist = 0
    for k in DistFromTiers:
        sumDist+=1/DistFromTiers[k]

    ProbTier = {}
    for k in DistFromTiers:
        ProbTier[k] = (1 / DistFromTiers[k]) / sumDist

    MaxTire = max(ProbTier, key=ProbTier.get)
    return NeededTier,MaxTire,ProbTier,NeededGPA.values[0],NeededVerbal.values[0], NeededQuants.values[0], NeededWriting.values[0]
