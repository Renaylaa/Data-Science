# Student Academic Status Prediction

Multiclass classification to predict whether a student will Dropout, remain Enrolled, or Graduate, intended as an early warning tool for academic support.

## Overview
- Dataset: Predict Students' Dropout and Academic Success (UCI ML Repository, dataset 697, CC BY 4.0)
- Size: 4,424 students, 36 features, 3 classes
- Task: supervised multiclass classification
- Tools: Python, pandas, scikit-learn, XGBoost, SHAP, Google Colab

## Business Problem
Universities hold student data but usually analyze it after students have already dropped out. This project identifies at-risk students early so that academic mentoring or financial support can be offered in time.

## Methodology
1. Business understanding and success criteria
2. Data collection and validation (missing values, duplicates, data types, decimal format)
3. Exploratory data analysis and hypotheses
4. Data cleaning and feature engineering (pass rate ratio features, 38 features total)
5. Modeling: Decision Tree, Random Forest (GridSearchCV, 5-fold), XGBoost; stratified 80:20 split
6. Evaluation and interpretation (classification report, confusion matrix, SHAP)

## Results
| Model | Accuracy | Macro F1 | Dropout Recall | Dropout F1 |
|---|---|---|---|---|
| Decision Tree | 68.36% | 0.62 | 0.72 | 0.76 |
| Random Forest (tuned) | 77.74% | 0.70 | 0.76 | 0.80 |
| XGBoost | 76.95% | 0.71 | 0.75 | 0.78 |

Key factors: approved curricular units in semester 2, then tuition payment status.

## Early Prediction Scenario (Semester 1 Only)
Semester 2 features were removed to simulate prediction at the end of semester 1. Accuracy stayed at 72% to 74% and Dropout recall at 0.72 to 0.73, giving the institution one semester more to intervene.

## Limitations and Next Steps
- Enrolled class is the weakest (F1 0.46) and class imbalance is not yet handled.
- Single institution and single train-test split.
- Planned: class weights or oversampling, XGBoost tuning, stratified k-fold evaluation, and a fairness check on sensitive attributes.

## Author
Renajwa Naylafasya | LinkedIn: http://www.linkedin.com/in/renajwa-n | Email: renanylaa22@gmail.com

