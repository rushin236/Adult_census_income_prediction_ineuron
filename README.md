# Ineuron Adult Census Income Prediction 


## Table Of Content

- [Ineuron Adult Census Income Prediction](#ineuron-adult-census-income-prediction)
  - [Table Of Content](#table-of-content)
  - [About](#about)
  - [Demo](#demo)
  - [Problem Statement](#problem-statement)
  - [Project Work Flow](#project-work-flow)
  - [Project Documentation](#project-documentation)
  - [Project Installation Guide](#project-installation-guide)
  - [Author](#author)

## About

This project focuses on predicting whether an individual's income exceeds $50K based on census data. By leveraging machine learning techniques, we aim to assist in identifying factors that influence income levels and provide insights into socioeconomic trends.

## Demo

![demo gif](./demo/webapp-demo.gif)

## Problem Statement

The Adult Census Income Prediction problem involves predicting whether an individual's income exceeds $50K per year based on demographic and socioeconomic attributes collected in a census survey. This binary classification task aims to assist in understanding the factors influencing income levels and identifying individuals likely to earn above a certain threshold, which can have implications for resource allocation, policy-making, and targeted interventions.

## Project Work Flow

1. **Data Ingestion**: Data is in the form of CSV and is being downloaded from GitHub.
2. **Data Validation**: Checking if the file is downloaded or not.
3. Data Analysis: In this stage the we do, **data preprocessing**, **data analysis**, **build preprocessor**, **feature selection**.
4. **Model Build**: In this we build the models with various available classification algorithms.
5. **Model Evaluation**: We evaluate all the models based on train and test data results to find the best one.
6. Save Model: Save the best model.
7. Prediction: Making predictions using the saved models.

## Project Documentation

- [Exploratory Data Analysis](https://github.com/rushin236/Ineuron_adult_census_income_prediction/blob/main/research/03_data_analysis.ipynb)
- [High Level Design](https://github.com/rushin236/Ineuron_adult_census_income_prediction/blob/main/docs/High%20Level%20Design%20(HLD).pdf)
- [Low Level Design](https://github.com/rushin236/Ineuron_adult_census_income_prediction/blob/main/docs/Low%20Level%20Design%20(LLD).pdf)
- [Architecture](https://github.com/rushin236/Ineuron_adult_census_income_prediction/blob/main/docs/Architechture_V1.0.pdf)
- [Wireframe](https://github.com/rushin236/Ineuron_adult_census_income_prediction/blob/main/docs/WireFrame.pdf)
- [Detailed Project Report](https://github.com/rushin236/Ineuron_adult_census_income_prediction/blob/main/docs/Detailed%20Project%20Report.pdf)

## Project Installation Guide

1. Clone the Git Repo
```bash
git clone https://github.com/rushin236/Ineuron_adult_census_income_prediction.git
```

2. Change Directory to Project Repo
```bash
cd Ineuron_adult_census_income_prediction
```

3. Create Conda Env
```bash
conda create -p venv python=3.10 -y
```

4. Activate conda Env
```bash
conda activate venv/
```

5. Install requirements
```bash
pip install -r requirements.txt
```

6. Follow the video

![demo build process](./demo/Adult-Census-Income-Prediction-Demo.gif)

## Author

Rushikesh Shinde: [LinkedIn](https://www.linkedin.com/in/rushikeshshinde987/)