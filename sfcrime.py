#1. IMPORT MODULES
import numpy as np
import pandas as pd
import os, time
from sys import argv

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from datetime import datetime

#2. FUNCTIONS
def importData(fileName, separator, indexVariable):
    """
    Function that makes it easier to import data and set index.
    """
    data = pd.read_csv(fileName, sep = separator, error_bad_lines = False, na_values = "NULL")
    if indexVariable != "NA":
        data.set_index(indexVariable, drop=True, append=False, inplace=True, verify_integrity=False)

    return data
    
def testSample(Xtrain, Xtest, Ytrain, size):
    """
    Help function to quickly make samples if necessary.
    """
    train = pd.concat([Ytrain, Xtrain], axis=1)
    sTrain = train.sample(int(size*len(train)), replace=False)
    sYtrain = sTrain.iloc[:,0]
    sXtrain = sTrain.iloc[:,1:len(sTrain.T)]
    sXtest = Xtest.sample(int(size*len(Xtest)), replace=False)
    
    return sXtrain, sYtrain, sXtest
    
#3. IMPORT DATA
yourDirectory = "/Users/cornelisvletter/desktop/progs/kaggle/sfcrime"
os.chdir(yourDirectory)
trainData = importData("train.csv", ",", "NA")
trainData["Dates"] = pd.to_datetime(trainData["Dates"])

testData = importData("test.csv", ",", "Id")
testData["Dates"] = pd.to_datetime(testData["Dates"])

#3.1 EXPLORE
trainTarget = trainData["Category"]

categoryFreq = pd.DataFrame(trainTarget.value_counts())
categoryFreq["pct"] = categoryFreq.iloc[:,0]/len(trainData)

#4. PREP VARIABLES

#4.1 PREP TRAIN DATA


trainFeatures = trainData.drop(["Dates", "Category", "Descript", "Resolution", 
	"Address", "PdDistrict", "DayOfWeek"], 
	axis = 1, inplace = False)

trainData["HourOfDay"] = [x.hour for x in trainData["Dates"]]
trainData["Week"] = [x.week for x in trainData["Dates"]]
trainData["Year"] = [x.year for x in trainData["Dates"]]

areaDummies = pd.get_dummies(trainData["PdDistrict"])
hourDummies = pd.get_dummies(trainData["HourOfDay"])
daysDummies = pd.get_dummies(trainData["DayOfWeek"])
yearDummies = pd.get_dummies(trainData["Year"])

trainFeatures = pd.concat([trainFeatures, areaDummies, hourDummies, daysDummies, yearDummies], axis=1)

#4.2 PREP TEST DATA
testFeatures = testData.drop(["Dates", "Address", "PdDistrict", "DayOfWeek"],
    axis=1, inplace=False)
    
testData["HourOfDay"] = [x.hour for x in testData["Dates"]]
testData["Week"] = [x.week for x in testData["Dates"]]  
testData["Year"] = [x.year for x in testData["Dates"]]

areaDummies = pd.get_dummies(testData["PdDistrict"])
hourDummies = pd.get_dummies(testData["HourOfDay"])
daysDummies = pd.get_dummies(testData["DayOfWeek"])
yearDummies = pd.get_dummies(testData["Year"])

testFeatures = pd.concat([testFeatures, areaDummies, hourDummies, daysDummies, yearDummies], axis=1)

#5. RUN MODEL  

"""
Not calibrated yet. Arbitrary chosen values or default.
""" 

ranFor =  RandomForestClassifier(n_estimators=50, criterion='gini', max_depth=None, min_samples_split=2, 
                                min_samples_leaf=50, min_weight_fraction_leaf=0.0, max_features='auto', 
                                max_leaf_nodes=None, bootstrap=True, oob_score=False, n_jobs=2, 
                                random_state=None, verbose=0, warm_start=False, class_weight='auto')

print "Time before fitting is: %s" % datetime.now().strftime('%H:%M:%S')
ranFor.fit(trainFeatures, trainTarget)

print "Time before in sample predicting is: %s" % datetime.now().strftime('%H:%M:%S')
predictIS = ranFor.predict(trainFeatures)
predictIS = pd.DataFrame(predictIS)

print "The in sample accuracy is: %s" % round(accuracy_score(trainTarget, predictIS),3)

print "Time before out of sample predicting is: %s" % datetime.now().strftime('%H:%M:%S')
predictOS = ranFor.predict(testFeatures)
predictOS = pd.DataFrame(predictOS)

predictOS = pd.get_dummies(predictOS.iloc[:,0])
predictIS = pd.get_dummies(predictIS.iloc[:,0])

predictOS = predictOS.astype(int)
predictIS = predictIS.astype(int)

predictOS.index.name = "Id"
predictIS.index.name = "Id"

#6. CHECK SUBMISSION

"""
Compare out of sample prediction to sample submission.
Checks whether the prediction contains the same amount of columns 
(excluding the ID, which is the index) and in the right order.
"""

sampleSubmission = importData("sampleSubmission.csv", ",", "Id")

arrayOrder = np.sum(predictOS.columns.values == sampleSubmission.columns.values)

print "The order of the columns is the same as in the sample submission: %s" % (arrayOrder == len(sampleSubmission.T))

#7. SAVE TO CSV FILE
"""
Saves both the in sample and out of sample predictions, having the ID variable as index.
"""

script, version = argv

nameOS = "outofsamplePrediction_v%s.csv" % version
nameIS = "insamplePrediction_v%s.csv" % version

predictIS.to_csv(nameIS, sep=',', index=True)
predictOS.to_csv(nameOS, sep=',', index=True)




os.curdir




