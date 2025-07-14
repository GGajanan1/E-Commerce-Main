# Fraud Detection System

A machine learning-based fraud detection system using LightGBM with SHAP explanations for transaction analysis.

## Dataset

### Required Dataset Files:
- `train_transaction.csv` - Training transaction data
- `train_identity.csv` - Training identity data

### Dataset Links:
- **Direct Dataset Link**: https://drive.google.com/drive/folders/1rcLPaRXxkkMHrjqlxY_21EjsydRckVVG?usp=sharing


## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Making Predictions
```bash
python main.py
```

Then provide transaction data as JSON input or specify a JSON file path.


## Input Format

The system expects transaction data in JSON format with the following structure: (use this json for testing purposes)
```json
{
  "TransactionID": 2000000004,
  "TransactionDT": 43200,
  "TransactionAmt": 123456.78,
  "ProductCD": "H",
  "card1": 5555,
  "card2": 555.5,
  "addr1": 555,
  "addr2": 55,
  "dist1": 999.9,
  "P_emaildomain": "mailer.pro",
  "R_emaildomain": "mail.pro",
  "DeviceType": "tablet",
  "DeviceInfo": "SuspiciousTablet"
}

```

## Output Format

The system returns predictions in JSON format:
```json
{
  "is_fraud": 1,
  "fraud_probability": 0.5879322341027382,
  "explanation": [
    {
      "feature": "C13",
      "shap_value": 1.094956490694899
    },
    {
      "feature": "TransactionAmt",
      "shap_value": 0.977993984044388
    },
    {
      "feature": "TransactionDT",
      "shap_value": -0.9426508531297074
    },
    {
      "feature": "ProductCD",
      "shap_value": 0.44236892648583503
    },
    {
      "feature": "C14",
      "shap_value": 0.4278349461082419
    }
  ]
}
```

## Features

- **LightGBM Model**: Fast gradient boosting framework
- **SHAP Explanations**: Understand why predictions were made
- **Automatic Preprocessing**: Handles missing values and categorical encoding
- **Model Persistence**: Save and load trained models
- **Command Line Interface**: Easy to use from terminal

## Requirements

- Python 3.7+
- pandas
- numpy
- lightgbm
- shap
- joblib
- scikit-learn

## Dataset Information

The Fraud Detection dataset contains:
- **Transaction Table**: 590,540 training samples with 394 features
- **Target Variable**: `isFraud` (binary classification)
