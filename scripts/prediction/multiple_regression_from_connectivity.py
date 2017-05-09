"""
The aim of the script is age prediction of CamCan features extracted with
diferent connectivity matrices and different atlases


"""


import os
import pandas as pd
from collections import OrderedDict
import numpy as np
from camcan.datasets import load_camcan_connectivity_rest, \
    load_camcan_behavioural

from sklearn.metrics import mean_squared_error, mean_absolute_error, \
    explained_variance_score, r2_score
from sklearn import linear_model, svm, tree, ensemble, neighbors
from sklearn.svm import SVR
from sklearn.multioutput import MultiOutputRegressor
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer


def camcan_prediction_uni_out(x, y, regr_uni_list, results_path,
                              name_csv_prediction):
    ''' Unioutput prediction

    :param x: Training vector, array-like, shape (n_samples, n_features)
    :param y: Target vector, array-like, shape (n_samples)
    :param regr_uni_list: list of uni output regressors
    :param results_path: path to the result folder
    :param name_csv_prediction: name of the file to save
    :return: metrics as pandas.DataFrame,
    '''

    name_regr_list = []
    mse_list = []
    mae_list = []
    evs_list = []
    r2s_list = []
    y_test_array = []
    y_predict_array = []

    for regr in regr_uni_list:
        name_regr = str(regr)[0:str(regr).find('(')]
        if name_regr == 'SVR':
            name_regr = name_regr + '_' + regr.kernel
        name_regr_list.append(name_regr)
        print(name_regr)
        name_regr_list.append(name_regr)
        print(name_regr)

        mse_list_cv = []
        mae_list_cv = []
        evs_list_cv = []
        r2s_list_cv = []

        # Train the model using the training sets
        for index, (train_index, test_index) in enumerate(cv.split(x)):
            print(index)
            x_train, x_test = x[train_index], x[test_index]
            y_train, y_test = y[train_index], y[test_index]

            regr.fit(x_train, y_train)

            mse = mean_squared_error(y_test, regr.predict(x_test))
            mse_list_cv.append(mse)
            mae = mean_absolute_error(y_test, regr.predict(x_test))
            mae_list_cv.append(mae)
            evs = explained_variance_score(y_test, regr.predict(x_test))
            evs_list_cv.append(evs)
            r2s = r2_score(y_test, regr.predict(x_test))
            r2s_list_cv.append(r2s)
            y_test_array.append(y_test)
            y_predict_array.append(regr.predict(x_test))

        mse_list.append(np.mean(mse_list_cv))
        mae_list.append(np.mean(mae_list_cv))
        evs_list.append(np.mean(evs_list_cv))
        r2s_list.append(np.mean(r2s_list_cv))

    df_prediction_uni = pd.DataFrame(
        OrderedDict((('Model', pd.Series(name_regr_list)),
                     ('MSE', pd.Series(mse_list)),
                     ('MAE', pd.Series(mae_list)),
                     ('EVS', pd.Series(evs_list)),
                     ('R2S', pd.Series(r2s_list)))))

    df_prediction_uni.to_csv(os.path.join(results_path, name_csv_prediction))
    print('The result csv file %s' % os.path.join(results_path,
                                                  name_csv_prediction))
    return df_prediction_uni, y_test_array, y_predict_array

def camcan_prediction_multi_out(x, y, regr_multi_list, regr_uni_list,
                                results_path, name_csv_prediction, y_keys):
    ''' Unioutput predictio

    :param x: Trainig vector, array-like, shape (n_samples, n_features)
    :param y: Target vector, array-like, shape (n_samples)
    :param regr_multi_list: list of multi output regressors
    :param regr_uni_list: list of uni output regressors
    :param results_path: path to the result folder
    :param name_csv_prediction: name of the file to save
    :param y_keys: name of the vectors to predict, i.e "age"
    :return: metrics as pandas.DataFrame,
    '''

    name_regr_list = []
    mse_list = []
    mae_list = []
    evs_list = []
    r2s_list = []

    mse_mt_list = []
    mae_mt_list = []
    evs_mt_list = []
    r2s_mt_list = []
    y_test_array = []
    y_predict_array = []

    for regr in regr_multi_list + regr_uni_list:
        name_regr = str(regr)[0:str(regr).find('(')]
        if name_regr == 'SVR':
            name_regr = name_regr + '_' + regr.kernel
        name_regr_list.append(name_regr)
        print(name_regr)
        if regr in regr_uni_list:
            regr = MultiOutputRegressor(regr)
        mse_list_cv = []
        mae_list_cv = []
        evs_list_cv = []
        r2s_list_cv = []
        mse_mt_list_cv = []
        mae_mt_list_cv = []
        evs_mt_list_cv = []
        r2s_mt_list_cv = []

        # Train the model using the training sets
        for index, (train_index, test_index) in enumerate(cv.split(x)):
            print(index)
            x_train, x_test = x[train_index], x[test_index]
            y_train, y_test = y[train_index], y[test_index]

            regr.fit(x_train, y_train)

            mse = mean_squared_error(y_test, regr.predict(x_test))
            mse_mt = mean_squared_error(y_test, regr.predict(x_test),
                                        multioutput='raw_values')
            # print("Mean squared error: %.2f" % mse)
            mse_list_cv.append(mse)
            mse_mt_list_cv.append(mse_mt)

            mae = mean_absolute_error(y_test, regr.predict(x_test))
            mae_mt = mean_absolute_error(y_test, regr.predict(x_test),
                                         multioutput='raw_values')
            # print("Mean absolute error: %.2f" % mae)
            mae_list_cv.append(mae)
            mae_mt_list_cv.append(mae_mt)

            evs = explained_variance_score(y_test, regr.predict(x_test))
            evs_mt = explained_variance_score(y_test, regr.predict(x_test),
                                              multioutput='raw_values')
            # print(" Explained variance score: %.2f" % evs)
            evs_list_cv.append(evs)
            evs_mt_list_cv.append(evs_mt)

            r2s = r2_score(y_test, regr.predict(x_test))
            r2s_mt = r2_score(y_test, regr.predict(x_test),
                              multioutput='raw_values')
            # print('R² score: %.2f' % r2s)
            r2s_list_cv.append(r2s)
            r2s_mt_list_cv.append(r2s_mt)

            y_test_array.append(y_test)
            y_predict_array.append(regr.predict(x_test))

        mse_list.append(np.mean(mse_list_cv))
        mae_list.append(np.mean(mae_list_cv))
        evs_list.append(np.mean(evs_list_cv))
        r2s_list.append(np.mean(r2s_list_cv))
        mse_mt_list.append(np.mean(mse_mt_list_cv, axis=0))
        mae_mt_list.append(np.mean(mae_mt_list_cv, axis=0))
        evs_mt_list.append(np.mean(evs_mt_list_cv, axis=0))
        r2s_mt_list.append(np.mean(r2s_mt_list_cv, axis=0))

    y_mse_keys = ['MSE_' + key for key in y_keys]
    y_mae_keys = ['MAE_' + key for key in y_keys]
    y_evs_keys = ['EVS_' + key for key in y_keys]
    y_r2s_keys = ['R2S_' + key for key in y_keys]

    mse_mt_df = pd.DataFrame(np.array(mse_mt_list), columns=[y_mse_keys])
    mae_mt_df = pd.DataFrame(np.array(mae_mt_list), columns=[y_mae_keys])
    evs_mt_df = pd.DataFrame(np.array(evs_mt_list), columns=[y_evs_keys])
    r2s_mt_df = pd.DataFrame(np.array(r2s_mt_list), columns=[y_r2s_keys])

    df_prediction_uni = pd.DataFrame(
        OrderedDict((('Model', pd.Series(name_regr_list)),
                     ('MSE', pd.Series(mse_list)),
                     ('MAE', pd.Series(mae_list)),
                     ('EVS', pd.Series(evs_list)),
                     ('R2S', pd.Series(r2s_list)))))
    df_prediction = pd.concat([df_prediction_uni, mse_mt_df, mae_mt_df,
                               evs_mt_df, r2s_mt_df], axis=1)

    df_prediction.to_csv(os.path.join(results_path, name_csv_prediction))
    print('The result csv file %s' % os.path.join(results_path,
                                                  name_csv_prediction))
    return df_prediction, y_test_array, y_predict_array


def plot_regression(y_target, y_predict, fig_name, fig_path):
    plt.scatter(y_target, y_predict)
    fig, ax = plt.subplots()
    ax.scatter(y_target, y_predict)
    ax.plot([y_target.min(), y_target.max()], [y_target.min(), y_target.max()],
            'r-', lw=4)
    ax.set_xlabel('Target')
    ax.set_ylabel('Predicted')
    plt.savefig(os.path.join(fig_path, fig_name))
    plt.close()


###############################################################################
# CamCan data

myhost = os.uname()[1]

if myhost == 'darya':
    print(myhost)
    raw_path = '/home/darya/Documents/Inria/data/camcan'
    csv_path = '/home/darya/Documents/Inria/data/camcan/cc700-scored'
    cache_path = '/home/darya/Documents/Inria/experiments/cache'
    results_path = '/home/darya/Documents/Inria/experiments/CamCan/prediction'
elif myhost == 'drago':
    raw_path = 'drago:/storage/data/camcan'
    csv_path = 'drago:/storage/data/camcan/cc700-scored'
    cache_path = '/storage/tompouce/dchyzhyk/data/cache'
    results_path = '/storage/tompouce/dchyzhyk/data/experiments/camcan'

# connectivity folder
connectivity_folder = 'camcan_connectivity'
atlases = ['basc064', 'basc122', 'basc197', 'msdl']
kind_connectivity = ['tangent', 'correlation', 'partial correlation']

# phenotype
csv_name = 'participant_data.csv'
csv_file = os.path.join(csv_path, csv_name)
# behaviour
csv_behav = os.path.join(raw_path, 'total_score.csv')

dataname = 'CamCan'

###############################################################################
# Cross validation

n_iter = 10  # Number of splits
cv = KFold(n_splits=n_iter, random_state=0, shuffle=True)

###############################################################################
# Create regression object

regr_multi_list = [linear_model.LinearRegression(),
                   linear_model.RidgeCV(),
                   tree.DecisionTreeRegressor(),
                   ensemble.ExtraTreesRegressor(),
                   neighbors.KNeighborsRegressor()]

regr_uni_list = [linear_model.BayesianRidge(),
                 linear_model.ElasticNet(),
                 linear_model.HuberRegressor(),
                 linear_model.Lasso(),
                 linear_model.LassoLars(),
                 linear_model.PassiveAggressiveRegressor(),
                 svm.LinearSVR(),
                 ensemble.RandomForestRegressor(),
                 ensemble.AdaBoostRegressor(),
                 ensemble.BaggingRegressor(),
                 SVR(kernel='rbf'),
                 SVR(kernel='linear')]

###############################################################################
# Prediction: Unilabel
# Prediction age

# select number of subject
# n_subj_list = [100, 200, 400, 626]
n_subj_list = [626]

y_keys = ['age']
y_keys_save_name = '_'.join(y_keys)


for atlas in atlases:
    for kind_con in kind_connectivity:

        conn_files = load_camcan_connectivity_rest(data_dir=os.path.join(
            raw_path, connectivity_folder), patients_info_csv=csv_file,
            atlas=atlas, kind=kind_con, patients_excluded=None)

        x = np.array(conn_files.connectivity)
        y = np.array(conn_files.scores.age)
        for n_subjects in n_subj_list:
            name_csv_prediction = (dataname + '_' + y_keys_save_name +
                                   '_prediction_' + str(n_subjects) + 'subj_' +
                                   atlas + '_atlas_' + kind_con + '.csv')

            df_prediction, y_test_array, y_predict_array = \
                camcan_prediction_uni_out(x[0:n_subjects, :], y[0:n_subjects],
                                          regr_uni_list, results_path,
                                          name_csv_prediction)

            # plotting
            y_test_array_plot = np.concatenate(y_test_array)
            y_predict_array_plot = np.concatenate(y_predict_array)

            name_fig = (dataname + '_' + y_keys_save_name + '_prediction_' +
                        str(n_subjects) + 'subj_' + atlas + '_atlas_' +
                        kind_con + '.png')

            plot_regression(y_test_array_plot, y_predict_array_plot, name_fig,
                            results_path)

###############################################################################
# Multioutput prediction
# Prediction behavioural data

n_subj_list = [626]

y_keys = ['age', 'hand', 'gender_text']
y_keys = ['RTcv_59', 'RTcv_73', 'RTcv_79']
y_keys_save_name = '_'.join(y_keys)

for atlas in atlases:
    for kind_con in kind_connectivity:

        conn_files = load_camcan_connectivity_rest(data_dir=os.path.join(
            raw_path, connectivity_folder), patients_info_csv=csv_file,
            atlas=atlas, kind=kind_con, patients_excluded=None)
        x = np.array(conn_files.connectivity)

        # load behavioural data
        scores = load_camcan_behavioural(csv_behav,
                                         patients_info_csv=csv_file,
                                         patients_excluded=None,
                                         column_selected=None)
        df = scores.data.copy()
        df['subject_id'] = scores.subject_id
        df = df[df['subject_id'].isin(conn_files.subject_id)]

        y = df.loc[:, y_keys]
        y = Imputer().fit_transform(y)

        for n_subjects in n_subj_list:
            name_csv_prediction = (dataname + '_' + y_keys_save_name +
                                   '_prediction_' + str(n_subjects) + 'subj_' +
                                   atlas + '_atlas_' + kind_con + '.csv')

            df_prediction, y_test_array, y_predict_array = \
                camcan_prediction_multi_out(x[0:n_subjects, :], y[0:n_subjects],
                                            regr_multi_list, regr_uni_list,
                                            results_path, name_csv_prediction,
                                            y_keys)

            # plotting
            y_test_array_plot = np.concatenate(y_test_array)
            y_predict_array_plot = np.concatenate(y_predict_array)

            name_fig = (dataname + '_' + y_keys_save_name + '_prediction_' +
                        str(n_subjects) + 'subj_' + atlas + '_atlas_' +
                        kind_con + '.png')

            plot_regression(y_test_array_plot, y_predict_array_plot, name_fig,
                            results_path)
