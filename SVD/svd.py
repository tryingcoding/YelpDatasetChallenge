import math
import random
from recsys.datamodel.data import Data
import recsys.algorithm
from recsys.algorithm.factorize import SVD
from recsys.evaluation.prediction import RMSE, MAE
recsys.algorithm.VERBOSE = True

filename = '/home/13ritvik_gmail_com/ratings.dat'
data = Data()
format = {'col':0, 'row':1, 'value':2, 'ids': 'string'}
data.load(filename, sep='::', format=format)

#train, test = data.split_train_test(percent=80)
data_l = list(data)
random.shuffle(data_l)
print len(data_l)
div = int(len(data_l)/10)
rmse_lst = []
mae_lst = []

for i in range(0,10):
    svd = SVD()
    #train, test = data.split_train_test(percent=90)
    test = Data()
    train = Data()
    test.set(data_l[(i*div):((i+1)*div)])
    train.set(data_l[:(i*div)] + data_l[((i+1)*div):])
    svd.set_data(train)
    k = 100
    svd.compute(k=k, min_values=5, pre_normalize=None, mean_center=True, post_normalize=True)

    #Evaluation using prediction-based metrics
    rmse = RMSE()
    mae = MAE()
    for rating, item_id, user_id in test.get():
        try:
            pred_rating = svd.predict(item_id, user_id, MIN_VALUE=0.0, MAX_VALUE=5.0)
            #print pred_rating
            rmse.add(rating, pred_rating)
            mae.add(rating, pred_rating)
            #print 'RMSE=%s' % rmse.compute()
            #print 'MAE=%s' % mae.compute()
        except KeyError:
            continue

    rmse_lst.append(rmse.compute())
    mae_lst.append(mae.compute())

rmse_lst = [i ** 2 for i in rmse_lst]
mae_lst = [i ** 2 for i in mae_lst]

rmse_final = math.sqrt(sum(rmse_lst)/10)
mae_final = math.sqrt(sum(mae_lst)/10)
print rmse_final
print mae_final
