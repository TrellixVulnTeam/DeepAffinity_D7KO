from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import scipy.sparse as sps
import numpy as np
import math
import random
from sklearn.model_selection import GridSearchCV
import pickle
import statsmodels.api as sm
from sklearn.feature_selection import VarianceThreshold
from sklearn import preprocessing


random.seed(1234)
def normalize_labels(label):
   x = []
   micro=1000000
   for i in label:
      if i ==0:
         print(i)
      m = -math.log10(i)+math.log10(micro)
      x.append(m)

   return x




################# reading labels

data_path = "/scratch/user/mostafa_karimi/CPI/final_data/new_data/IC50/SPS/"
data_measure="ic50"
label_path_train=data_path+"train_"+data_measure
label_train = []
f = open(label_path_train, "r")
length_train=0
for line in f:
    if (line[0]=="<")or(line[0]==">"):
            print("Inequality!!!\n")
    else:
            label_train.append(float(line))
            length_train = length_train+1

f.close()
#label_train = normalize_labels(label_train)


label_path_test=data_path+"test_"+data_measure
label_test = []
f = open(label_path_test, "r")
length_test=0
for line in f:
    if (line[0]=="<")or(line[0]==">"):
            print("Inequality!!!\n")
    else:
            label_test.append(float(line))
            length_test = length_test+1

f.close()
#label_test = normalize_labels(label_test)

label_path_ER=data_path+"ER_"+data_measure
label_ER = []
f = open(label_path_ER, "r")
length_ER=0
for line in f:
    if (line[0]=="<")or(line[0]==">"):
            print("Inequality!!!\n")
    else:
            label_ER.append(float(line))
            length_ER = length_ER+1

f.close()
#label_ER = normalize_labels(label_ER)


label_path_GPCR=data_path+"GPCR_"+data_measure
label_GPCR = []
f = open(label_path_GPCR, "r")
length_GPCR=0
for line in f:
    if (line[0]=="<")or(line[0]==">"):
            print("Inequality!!!\n")
    else:
            label_GPCR.append(float(line))
            length_GPCR = length_GPCR+1

f.close()
#label_GPCR = normalize_labels(label_GPCR)


label_path_kinase=data_path+"kinase_"+data_measure
label_kinase = []
f = open(label_path_kinase, "r")
length_kinase=0
for line in f:
    if (line[0]=="<")or(line[0]==">"):
            print("Inequality!!!\n")
    else:
            label_kinase.append(float(line))
            length_kinase = length_kinase+1

f.close()
#label_kinase = normalize_labels(label_kinase)

label_path_channel=data_path+"channel_"+data_measure
label_channel = []
f = open(label_path_channel, "r")
length_channel=0
for line in f:
    if (line[0]=="<")or(line[0]==">"):
            print("Inequality!!!\n")
    else:
            label_channel.append(float(line))
            length_channel = length_channel+1

f.close()
#label_channel = normalize_labels(label_channel)


##################  reading compound features
data_path = "/scratch/user/mostafa_karimi/CPI/final_data/new_data/IC50/RNN/"
num_feature=768
feature_type="joint.txt"

feature_train = np.zeros((length_train,num_feature))
textfile = open(data_path+"train_"+feature_type)
count=0
while length_train > count:
    x = textfile.readline()
    x = x.strip()
    result = np.array([list(map(float, x.split()))])
    feature_train[count,]=result
    count = count+1

selector = VarianceThreshold()
feature_train = selector.fit_transform(feature_train)
scaler = preprocessing.StandardScaler().fit(feature_train)
feature_train = scaler.transform(feature_train)

feature_ER = np.zeros((length_ER,num_feature))
textfile = open(data_path+"ER_"+feature_type)
count=0
while length_ER > count:
    x = textfile.readline()
    x = x.strip()
    result = np.array([list(map(float, x.split()))])
    feature_ER[count,]=result
    count = count+1

feature_ER = selector.transform(feature_ER)
feature_ER = scaler.transform(feature_ER)

feature_GPCR = np.zeros((length_GPCR,num_feature))
textfile = open(data_path+"GPCR_"+feature_type)
count=0
while length_GPCR > count:
    x = textfile.readline()
    x = x.strip()
    result = np.array([list(map(float, x.split()))])
    feature_GPCR[count,]=result
    count = count+1

feature_GPCR = selector.transform(feature_GPCR)
feature_GPCR = scaler.transform(feature_GPCR)


feature_kinase = np.zeros((length_kinase,num_feature))
textfile = open(data_path+"kinase_"+feature_type)
count=0
while length_kinase > count:
    x = textfile.readline()
    x = x.strip()
    result = np.array([list(map(float, x.split()))])
    feature_kinase[count,]=result
    count = count+1

feature_kinase = selector.transform(feature_kinase)
feature_kinase = scaler.transform(feature_kinase)

feature_channel = np.zeros((length_channel,num_feature))
textfile = open(data_path+"channel_"+feature_type)
count=0
while length_channel > count:
    x = textfile.readline()
    x = x.strip()
    result = np.array([list(map(float, x.split()))])
    feature_channel[count,]=result
    count = count+1

feature_channel = selector.transform(feature_channel)
feature_channel = scaler.transform(feature_channel)

feature_test = np.zeros((length_test,num_feature))
textfile = open(data_path+"test_"+feature_type)
count=0
while length_test > count:
    x = textfile.readline()
    x = x.strip()
    result = np.array([list(map(float, x.split()))])
    feature_test[count,]=result
    count = count+1

feature_test = selector.transform(feature_test)
feature_test = scaler.transform(feature_test)
######### Lasoo model
regr = RandomForestRegressor(n_jobs=20) # 28 cores

num_estimator = [50,100,200,500]
max_feature = ["auto","sqrt","log2"]
min_samples_leaf = [10,50,100]

tuned_parameters = [{'n_estimators': num_estimator,'max_features':max_feature,'min_samples_leaf':min_samples_leaf}]
n_folds = 10
clf = GridSearchCV(regr, tuned_parameters, cv=n_folds)
clf.fit(feature_train,label_train)

print("train error:")
y_pred_train = clf.predict(feature_train)
print(mean_squared_error(label_train,y_pred_train))

results = sm.OLS(y_pred_train,sm.add_constant(label_train)).fit()
print(results.summary())

print("test error:")
y_pred_test = clf.predict(feature_test)
print(mean_squared_error(label_test,y_pred_test))

results = sm.OLS(y_pred_test,sm.add_constant(label_test)).fit()
print(results.summary())

print("ER error:")
y_pred_ER = clf.predict(feature_ER)
print(mean_squared_error(label_ER,y_pred_ER))

results = sm.OLS(y_pred_ER,sm.add_constant(label_ER)).fit()
print(results.summary())


print("kinase error:")
y_pred_kinase = clf.predict(feature_kinase)
print(mean_squared_error(label_kinase,y_pred_kinase))

results = sm.OLS(y_pred_kinase,sm.add_constant(label_kinase)).fit()
print(results.summary())


print("GPCR error:")
y_pred_GPCR = clf.predict(feature_GPCR)
print(mean_squared_error(label_GPCR,y_pred_GPCR))

results = sm.OLS(y_pred_GPCR,sm.add_constant(label_GPCR)).fit()
print(results.summary())

print("channel error:")
y_pred_channel = clf.predict(feature_channel)
print(mean_squared_error(label_channel,y_pred_channel))

results = sm.OLS(y_pred_channel,sm.add_constant(label_channel)).fit()
print(results.summary())


#########  Saving model
rf_pkl_filename = 'rf_20182101.pkl'
rf_model_pkl = open(rf_pkl_filename, 'wb')
pickle.dump(clf,rf_model_pkl)
rf_model_pkl.close()

########## Saving prediction test
rf_pkl_test_filename = 'rf_20182101_test_pred.pkl'
rf_test_pkl = open(rf_pkl_test_filename, 'wb')
pickle.dump(y_pred_test,rf_test_pkl)
rf_test_pkl.close()

######### Saving Real label test
rf_pkl_test_filename = 'rf_20182101_test_real_lable.pkl'
rf_test_pkl = open(rf_pkl_test_filename, 'wb')
pickle.dump(label_test,rf_test_pkl)
rf_test_pkl.close()

########## Saving prediction train
rf_pkl_train_filename = 'rf_20182101_train_pred.pkl'
rf_train_pkl = open(rf_pkl_train_filename, 'wb')
pickle.dump(y_pred_train,rf_train_pkl)
rf_train_pkl.close()

######### Saving Real label train
rf_pkl_train_filename = 'rf_20182101_train_real_lable.pkl'
rf_train_pkl = open(rf_pkl_train_filename, 'wb')
pickle.dump(label_train,rf_train_pkl)
rf_train_pkl.close()


########## Saving prediction ER
rf_pkl_ER_filename = 'rf_20182101_ER_pred.pkl'
rf_ER_pkl = open(rf_pkl_ER_filename, 'wb')
pickle.dump(y_pred_ER,rf_ER_pkl)
rf_ER_pkl.close()

######### Saving Real label ER
rf_pkl_ER_filename = 'rf_20182101_ER_real_lable.pkl'
rf_ER_pkl = open(rf_pkl_ER_filename, 'wb')
pickle.dump(label_ER,rf_ER_pkl)
rf_ER_pkl.close()

########## Saving prediction kinase
rf_pkl_kinase_filename = 'rf_20182101_kinase_pred.pkl'
rf_kinase_pkl = open(rf_pkl_kinase_filename, 'wb')
pickle.dump(y_pred_kinase,rf_kinase_pkl)
rf_kinase_pkl.close()

######### Saving Real label kinase
rf_pkl_kinase_filename = 'rf_20182101_kinase_real_lable.pkl'
rf_kinase_pkl = open(rf_pkl_kinase_filename, 'wb')
pickle.dump(label_kinase,rf_kinase_pkl)
rf_kinase_pkl.close()

########## Saving prediction GPCR
rf_pkl_GPCR_filename = 'rf_20182101_GPCR_pred.pkl'
rf_GPCR_pkl = open(rf_pkl_GPCR_filename, 'wb')
pickle.dump(y_pred_GPCR,rf_GPCR_pkl)
rf_GPCR_pkl.close()

######### Saving Real label GPCR
rf_pkl_GPCR_filename = 'rf_20182101_GPCR_real_lable.pkl'
rf_GPCR_pkl = open(rf_pkl_GPCR_filename, 'wb')
pickle.dump(label_GPCR,rf_GPCR_pkl)
rf_GPCR_pkl.close()

########## Saving prediction channel
rf_pkl_channel_filename = 'rf_20182101_channel_pred.pkl'
rf_channel_pkl = open(rf_pkl_channel_filename, 'wb')
pickle.dump(y_pred_channel,rf_channel_pkl)
rf_channel_pkl.close()

######### Saving Real label channel
rf_pkl_channel_filename = 'rf_20182101_channel_real_lable.pkl'
rf_channel_pkl = open(rf_pkl_channel_filename, 'wb')
pickle.dump(label_channel,rf_channel_pkl)
rf_channel_pkl.close()


