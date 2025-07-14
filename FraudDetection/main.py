import pandas as pd
import numpy as np
import lightgbm as lgb
import shap
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os
import warnings
warnings.filterwarnings("ignore", message="LightGBM binary classifier with TreeExplainer shap values output has changed to a list of ndarray")
import argparse
import json
import sys

class FraudDetector:
    def __init__(self, model_path=None):
        self.model = None
        self.label_encoders = {}
        if model_path and os.path.exists(model_path):
            self.model, self.label_encoders = joblib.load(model_path)
        elif model_path:
            raise FileNotFoundError(f"Model file not found: {model_path}")

    def load_data(self, path_trans, path_id):
        df_trans = pd.read_csv(path_trans)
        df_id    = pd.read_csv(path_id)
        return df_trans.merge(df_id, on='TransactionID', how='left')

    def preprocess(self, df):
        df = df.copy()
        df.fillna(-999, inplace=True)
        cat_cols = df.select_dtypes('object').columns
        for col in cat_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            self.label_encoders[col] = le
        X = df.drop(['isFraud', 'TransactionID'], axis=1)
        y = df['isFraud'].astype(int)
        return X, y

    def train(self, train_trans_path, train_id_path, model_out_path='fraud_detector.pkl'):
        print("[INFO] Loading data...")
        df = self.load_data(train_trans_path, train_id_path)
        print("[INFO] Preprocessing...")
        X, y = self.preprocess(df)
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, stratify=y, random_state=42
        )
        print("[INFO] Training model...")
        train_data = lgb.Dataset(X_train, label=y_train)
        val_data   = lgb.Dataset(X_val,   label=y_val, reference=train_data)
        params = {
            'objective': 'binary',
            'metric': 'auc',
            'boosting_type': 'gbdt',
            'num_leaves': 64,
            'learning_rate': 0.05,
            'feature_fraction': 0.8,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'verbosity': -1
        }
        callbacks = [
            lgb.early_stopping(stopping_rounds=50),
            lgb.log_evaluation(period=100)
        ]
        self.model = lgb.train(
            params,
            train_data,
            num_boost_round=1000,
            valid_sets=[train_data, val_data],
            callbacks=callbacks
        )
        joblib.dump((self.model, self.label_encoders), model_out_path)
        print(f"[INFO] Model + encoders saved to {model_out_path}")

    def predict_and_explain(self, trans_dict, top_k=5):
        if self.model is None:
            raise ValueError("No model loaded. Train first or provide a valid model_path.")
        df = pd.DataFrame([trans_dict])
        df.fillna(-999, inplace=True)
        for col, le in self.label_encoders.items():
            if col in df.columns:
                mapping = {cls: idx for idx, cls in enumerate(le.classes_)}
                df[col] = df[col].map(lambda x: mapping.get(x, -1)).astype(int)
        feature_names = self.model.feature_name()
        aligned = {feat: df.get(feat, -999) for feat in feature_names}
        X = pd.DataFrame(aligned)
        proba = float(self.model.predict(X)[0])
        is_fraud = int(proba > 0.5)
        explainer = shap.TreeExplainer(self.model)
        raw_shap = explainer.shap_values(X)
        if isinstance(raw_shap, list) and len(raw_shap) > 1:
            shap_vals = raw_shap[1]
        else:
            shap_vals = raw_shap
        vals = shap_vals[0]
        feat_imp = sorted(
            zip(feature_names, vals), key=lambda x: abs(x[1]), reverse=True
        )[:top_k]
        explanation = [{'feature': f, 'shap_value': float(v)} for f, v in feat_imp]
        return {'is_fraud': is_fraud, 'fraud_probability': proba, 'explanation': explanation}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', action='store_true')
    parser.add_argument('--model', default='fraud_detector.pkl')
    parser.add_argument('--train-trans', default='train_transaction.csv')
    parser.add_argument('--train-id', default='train_identity.csv')
    args, _ = parser.parse_known_args()
    if args.train:
        FraudDetector().train(args.train_trans, args.train_id, args.model)
        return
    try:
        fd = FraudDetector(model_path=args.model)
    except FileNotFoundError:
        print(f"[WARN] Model not found; training...")
        FraudDetector().train(args.train_trans, args.train_id, args.model)
        fd = FraudDetector(model_path=args.model)

    input_data = sys.stdin.read().strip()
    if not input_data:
        input_data = input("Enter transaction JSON or filename: ")

    try:
        if os.path.exists(input_data):
            with open(input_data, 'r') as f:
                new_trans = json.load(f)
        else:
            new_trans = json.loads(input_data)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"File not found: {input_data}")
        sys.exit(1)

    result = fd.predict_and_explain(new_trans)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()