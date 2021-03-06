# Secure XGBoost

## Introduction

**Secure XGBoost** is a privacy-preserving gradient boosting library based off the popular [XGBoost](https://github.com/dmlc/xgboost) project. In addition to offering the same efficiency, flexibility, and portability that vanilla XGBoost provides, Secure XGBoost enables privacy-preserving model training and inference by leveraging hardware enclaves and data-oblivious algorithms. 

In a nutshell, data owners can use Secure XGBoost to train a model on a remote server _without_ revealing their data contents to the remote server. Furthermore, multiple data owners can use the library to _collaboratively_ train a model on their collective data, without revealing their individual data to each other.

This project is currently under development as part of the broader **mc<sup>2</sup>** effort (i.e., **M**ultiparty **C**ollaboration and **C**oopetition) by the UC Berkeley [RISE Lab](https://rise.cs.berkeley.edu/).

Please feel free to reach out to us if you would like use Secure XGBoost for your applications. We also welcome contributions to our work!

## Documentation

To get started with the library, please refer to the [documentation](https://mc2-xgboost.readthedocs.io/en/latest/).
