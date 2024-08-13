from typing import List, Any, Literal

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin, MetaEstimatorMixin, clone
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score

class LocalizedRegression(MetaEstimatorMixin, RegressorMixin, BaseEstimator):
    def __init__(
        self,
        estimator: None,
        n_neighbors: int = 10,
        fit_ratio: float = 0.1,
        n_estimators: int = 2
    ) -> None:
        self.estimator = Ridge() if estimator is None else estimator
        self.n_neighbors = n_neighbors
        self.fit_ratio = fit_ratio
        self.n_estimators = n_estimators

    def fit(self, X, y):
        self.n_samples_fit_, self.n_features_in_ = X.shape
        self.fit_count_ = max(self.n_neighbors, int(self.n_samples_fit_ * self.fit_ratio))

        self.fitted_samples_: List[np.ndarray] = []
        self.nn_: List[NearestNeighbors] = []
        self.estimators_: List[List[Any]] = []

        for _ in range(self.n_estimators):
            fitted_samples = np.random.choice(self.n_samples_fit_, self.fit_count_, replace = False)
            nn = NearestNeighbors(n_neighbors = self.n_neighbors)
            nn.fit(X[fitted_samples])
            neighbors = nn.kneighbors(X[fitted_samples], return_distance = False)
            estimators = []

            for n in neighbors:
                estimator = clone(self.estimator)
                estimator.fit(X[fitted_samples[n]], y[fitted_samples[n]])
                estimators.append(estimator)

            self.fitted_samples_.append(fitted_samples)
            self.nn_.append(nn)
            self.estimators_.append(estimators)

        return self

    def predict(self, X, n_neighbors: int | None = None, reduction: Literal["mean", "std"] | None = "mean" ):
        n_neighbors = self.n_neighbors if n_neighbors is None else n_neighbors
        preds_all = np.zeros((X.shape[0], self.fit_count_, self.n_estimators))
        preds_map = np.zeros(preds_all.shape, dtype = bool)

        for n_iter in range(self.n_estimators):
            neighbors = self.nn_[n_iter].kneighbors(X, n_neighbors = n_neighbors, return_distance = False)

            estimator_predict_map = [[] for _ in range(self.fit_count_)]

            for x_i, n in enumerate(neighbors):
                for i in n:
                    estimator_predict_map[i].append(x_i)

            for i, est in enumerate(self.estimators_[n_iter]):
                if len(estimator_predict_map[i]) > 0:
                    preds_all[estimator_predict_map[i], i, n_iter] = est.predict(X[estimator_predict_map[i]])
                    preds_map[estimator_predict_map[i], i, n_iter] = True
        
        preds_all = preds_all[preds_map].reshape(X.shape[0], n_neighbors, self.n_estimators)

        if reduction == "mean":
            return preds_all.mean(axis = (1, 2))
        if reduction == "std":
            return preds_all.std(axis = (1, 2))
        
        return preds_all

    def score(self, X, y):
        return r2_score(y, self.predict(X))