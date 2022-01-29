import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import cross_val_score
from numpy import absolute
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from joblib import dump

dataset = pd.read_excel('dataset.xlsx')


dataset_2 = dataset[['price', 'length']].dropna(how='any',axis=0)

y = dataset_2.iloc[:,0].values
X = dataset_2.iloc[:,1:].values

# ohe = OneHotEncoder()
# X = ohe.fit_transform(X).toarray()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)

model_xgboost = XGBRegressor()
model_xgboost.fit(X_train, y_train)

pred_xgboost = model_xgboost.predict(X_test)


model_rf = RandomForestRegressor()
model_rf.fit(X_train, y_train)

pred_rf = model_rf.predict(X_test)


from sklearn.preprocessing import RobustScaler
robust_scaler = RobustScaler()
Xtr_r = robust_scaler.fit_transform(X_train)
Xte_r = robust_scaler.transform(X_test)

model_rf_rb = RandomForestRegressor()
model_rf_rb.fit(Xtr_r, y_train)

pred_rb = model_rf_rb.predict(Xte_r)


'''
accuracies = cross_val_score(estimator = model, X = X_train, y = y_train, cv = 10)
print("Accuracy: {:.2f} %".format(accuracies.mean()*100))
print("Standard Deviation: {:.2f} %".format(accuracies.std()*100))
'''

r2_score = model_rf_rb.score(Xte_r,y_test)
print(r2_score*100,'%')

mean_squared_error(y_test, pred_xgboost)
mean_absolute_percentage_error(y_test, pred_xgboost)


dump(model_xgboost, 'model_xgboost.joblib')
dump(model_rf, 'model_rf.joblib')
dump(model_rf_rb, 'model_rf_rb.joblib')

