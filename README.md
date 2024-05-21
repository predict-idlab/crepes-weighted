# crepes-weighted

`crepes-weighted` is an extension of [`crepes`](https://github.com/henrikbostrom/crepes), a Python package that implements conformal classifiers, regressors, and predictive systems on top of any standard classifier and regressor. `crepes-weighted` extends `crepes` by adding support for weighted conformal prediction and predictive systems, in the future this could potentially be merged into the main `crepes` package.

## 🛠️ Installation

|                                                      | command                               |
| :--------------------------------------------------- | :------------------------------------ |
| [**pip**](https://pypi.org/project/crepes-weighted)          | `pip install crepes-weighted`                  |

## :rocket: Quick Start
First we create a synthetic dataset using the data-generating process described in *Kang and Schafer (2007)*. This function generates a dataset with 4 features and a target variable. The target variable is generated using the following formula:
```python
import numpy as np

def synthetic_kang_schafer_2007(n=2000, weights=None):
    if weights is None:
        weights = np.ones(n)/n
    x1 = np.random.normal(size=n)
    x2 = np.random.normal(size=n)
    x3 = np.random.normal(size=n)
    x4 = np.random.normal(size=n)

    y = 210 + 27.4*x1 + 13.7*x2 + 13.7*x3 + 13.7*x4 + np.random.normal(size=n)

    return np.stack([x1, x2, x3, x4], axis=1), y
```

Next, we first split it into a training and a test set using train_test_split from sklearn, and then further split the training set into a proper training set and a calibration set.
```python
from sklearn.model_selection import train_test_split

X, y = synthetic_kang_schafer_2007()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
X_train, X_cal, y_train, y_cal = train_test_split(X_train, y_train, test_size=0.5)
```
We now emulate a covariate shift by creating a new dataset with a different distribution, and we calculate the likelihood of each observation under this new distribution.
```python
shift_weights = np.array([-1, 0.5, -0.25, -0.1])
shifted_likelihood_test = np.exp(X_test @ shift_weights)
shifted_weights_test = shifted_likelihood_test / np.sum(shifted_likelihood_test)
shifted_likelihood_cal =  np.exp(X_cal @ shift_weights)

def weighted_sample(weights, frac=0.5):
    return np.random.choice(range(len(weights)), size=int(len(weights) * frac), p=weights)

idx_no_shift = weighted_sample(np.ones(len(shifted_weights_test))/len(shifted_weights_test), frac=0.25)
idx_shift = weighted_sample(shifted_weights_test, frac=0.25)
```
We now "wrap" a random forest regressor, fit it to the proper training set, and fit a weighted conformal classifier through the `calibrate` method, using the calibration set and a set of weights to account for the covariate shift.
```python
from sklearn.ensemble import RandomForestRegressor
from crepes_weighted import WrapRegressor

rf_wcps = WrapRegressor(RandomForestRegressor(n_estimators=100, random_state=17))
rf_wcps.fit(X_train_prop, y_train_prop)

rf_wcps.calibrate(X_cal, y_cal, likelihood_ratios=shifted_likelihood_cal, cps=True)
```
Finally, we can make predictions (intervals, p_values, and distributions) on the test set and calculate the coverage of the conformal predictive system.
```python
int_wcps = rf_wcps.predict_int(X_test[idx_shift], y=y_test[idx_shift], likelihood_ratios=shifted_likelihood_test[idx_shift])
dist_wcps = rf_wcps.predict_cps(X_test[idx_shift], y=y_test[idx_shift], likelihood_ratios=shifted_likelihood_test[idx_shift], return_cpds=True)
p_values_wcps = rf_wcps.predict_cps(X_test[idx_shift], y=y_test[idx_shift], likelihood_ratios=shifted_likelihood_test[idx_shift])
```

## Citing crepes-weighted

If you use `crepes-weighted` for a scientific publication, you are kindly requested to cite the following paper:

```bibtex
@misc{jonkers2024conformal,
      title={Conformal Predictive Systems Under Covariate Shift},
      author={Jef Jonkers and Glenn Van Wallendael and Luc Duchateau and Sofie Van Hoecke},
      year={2024},
      eprint={2404.15018},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```
The preprint version of the paper can be found at [https://arxiv.org/abs/2404.15018](https://arxiv.org/abs/2404.15018).

We also recommend citing the original `crepes` package:

```bibtex
@InProceedings{crepes,
  title = 	 {crepes: a Python Package for Generating Conformal Regressors and Predictive Systems},
  author =       {Bostr\"om, Henrik},
  booktitle = 	 {Proceedings of the Eleventh Symposium on Conformal and Probabilistic Prediction and Applications},
  year = 	 {2022},
  editor = 	 {Johansson, Ulf and Boström, Henrik and An Nguyen, Khuong and Luo, Zhiyuan and Carlsson, Lars},
  volume = 	 {179},
  series = 	 {Proceedings of Machine Learning Research},
  publisher =    {PMLR}
}
```

## License
This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

- - -

<p align="center">
👤 <i>Jef Jonkers</i>
</p>

