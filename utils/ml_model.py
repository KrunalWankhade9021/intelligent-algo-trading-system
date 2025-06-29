import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from xgboost import XGBClassifier
import numpy as np
import pandas as pd

# Central logging function
def log(msg, level="info", verbose=True):
    if verbose:
        if level == "warn":
            print(f"⚠️ {msg}")
        elif level == "success":
            print(f"✅ {msg}")
        else:
            print(msg)

def enhanced_feature_engineering(df):
    try:
        df['Target'] = ((df['Close'].shift(-1) / df['Close'] - 1) > 0.005).astype(int)
        df['Price_Change'] = df['Close'].pct_change()
        df['RollingMean_5'] = df['Close'].rolling(5).mean()
        df['RollingStd_5'] = df['Close'].rolling(5).std()
        df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()

        df['BB_position'] = (df['Close'] - df['Close'].rolling(20).mean()) / (2 * df['Close'].rolling(20).std())
        df['RSI_momentum'] = df['RSI'].diff() if 'RSI' in df.columns else 0
        df['Volume_ratio'] = df['Volume'] / df['Volume'].rolling(20).mean() if 'Volume' in df.columns else 1
        df['Price_velocity'] = df['Close'].diff() / df['Close'].shift(1)

        if 'High' in df.columns and 'Low' in df.columns:
            df['High_Low_ratio'] = (df['High'] - df['Low']) / df['Close']
            df['Close_position'] = (df['Close'] - df['Low']) / (df['High'] - df['Low'])
        else:
            df['High_Low_ratio'] = 0
            df['Close_position'] = 0.5

        df['ROC_5'] = df['Close'].pct_change(periods=5)
        df['ROC_10'] = df['Close'].pct_change(periods=10)

        df = df.ffill().fillna(0)
        return df
    except Exception as e:
        print(f"Feature engineering error: {e}")
        return df

def train_model(df, ticker="UNKNOWN", ret=0.0, win_ratio=0.0, verbose=False):
    model, accuracy, auc_score = train_improved_model(df, verbose=verbose)

    if model is None:
        log(f"Model training failed for {ticker}", "warn", verbose=True)
        return None, None

    # Always show final summary
    log(f"Logged: {ticker} | Return: {ret:.2f}%, Win Ratio: {win_ratio:.2f}%, "
        f"ML Accuracy: {accuracy * 100:.2f}%, AUC: {auc_score:.3f} | Model: Enhanced Ensemble",
        "success", verbose=True)

    return model, accuracy

def train_improved_model(df, verbose=False):
    try:
        df = enhanced_feature_engineering(df)
        df = df.dropna()

        if len(df) < 50:
            log(f"Insufficient data: {len(df)} rows. Need at least 50.", "warn", verbose)
            return None, None, None

        log(f"Class distribution: {np.bincount(df['Target'])}", verbose=verbose)
        log(f"Percentage positive: {df['Target'].mean():.2%}", verbose=verbose)

        all_features = [
            'RSI', '20DMA', '50DMA', 'Volume', 'Price_Change',
            'RollingMean_5', 'RollingStd_5', 'MACD',
            'BB_position', 'RSI_momentum', 'Volume_ratio', 'Price_velocity',
            'High_Low_ratio', 'Close_position', 'ROC_5', 'ROC_10'
        ]
        available_features = [f for f in all_features if f in df.columns]
        log(f"Using {len(available_features)} features: {available_features}", verbose=verbose)

        if len(available_features) < 3:
            log("Too few features available", "warn", verbose)
            return None, None, None

        X = df[available_features]
        y = df['Target']

        if y.sum() < 5 or (len(y) - y.sum()) < 5:
            log("Severe class imbalance. Switching to simple model.", "warn", verbose)
            return train_simple_model(X, y, verbose=verbose)

        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

        if len(X_train) < 30:
            log("Training set too small. Using simple model.", "warn", verbose)
            return train_simple_model(X, y, verbose=verbose)

        try:
            return train_ensemble_model(X_train, X_test, y_train, y_test, available_features, verbose=verbose)
        except Exception as e:
            log(f"Ensemble failed: {e}. Trying simple model...", "warn", verbose)
            return train_simple_model(X, y, verbose=verbose)

    except Exception as e:
        log(f"Model training failed completely: {e}", "warn", verbose)
        return None, None, None

def train_ensemble_model(X_train, X_test, y_train, y_test, features, verbose=False):
    base_models = [
        ('rf', Pipeline([
            ('scaler', RobustScaler()),
            ('classifier', RandomForestClassifier(
                n_estimators=100,
                max_depth=8,
                min_samples_split=5,
                random_state=42
            ))
        ])),
        ('xgb', Pipeline([
            ('scaler', RobustScaler()),
            ('classifier', XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                use_label_encoder=False,
                eval_metric='logloss',
                verbosity=0,
                random_state=42
            ))
        ]))
    ]

    meta_model = LogisticRegression(max_iter=1000)

    if len(X_train) > 100:
        cv_splits = min(5, len(X_train) // 20)
        cv = TimeSeriesSplit(n_splits=cv_splits) if cv_splits >= 2 else 3
    else:
        cv = 3

    log(f"Using CV strategy: {cv}", verbose=verbose)

    ensemble_model = StackingClassifier(
        estimators=base_models,
        final_estimator=meta_model,
        cv=cv
    )

    log("Training ensemble model...", verbose=verbose)
    ensemble_model.fit(X_train, y_train)

    y_pred = ensemble_model.predict(X_test)
    y_pred_proba = ensemble_model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    try:
        auc_score = roc_auc_score(y_test, y_pred_proba)
    except:
        auc_score = 0.5

    log("\n=== Ensemble Model Performance ===", verbose=verbose)
    log(f"Accuracy: {accuracy:.4f}", verbose=verbose)
    log(f"AUC Score: {auc_score:.4f}", verbose=verbose)

    if len(np.unique(y_test)) > 1:
        log("\nDetailed Classification Report:", verbose=verbose)
        log(classification_report(y_test, y_pred), verbose=verbose)

    try:
        rf_model = ensemble_model.named_estimators_['rf']
        feature_importance = rf_model.named_steps['classifier'].feature_importances_
        importance_df = list(zip(features, feature_importance))
        importance_df.sort(key=lambda x: x[1], reverse=True)

        log("\nTop 5 Most Important Features:", verbose=verbose)
        for feature, importance in importance_df[:5]:
            log(f"{feature}: {importance:.4f}", verbose=verbose)
    except Exception as e:
        log(f"Could not extract feature importance: {e}", "warn", verbose)

    return ensemble_model, accuracy, auc_score

def train_simple_model(X, y, verbose=False):
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2, random_state=42)

        model = Pipeline([
            ('scaler', RobustScaler()),
            ('classifier', RandomForestClassifier(
                n_estimators=50,
                max_depth=5,
                random_state=42
            ))
        ])

        log("Training simple fallback model...", verbose=verbose)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(y_test, y_pred)
        try:
            auc_score = roc_auc_score(y_test, y_pred_proba)
        except:
            auc_score = 0.5

        log("\n=== Simple Model Performance ===", verbose=verbose)
        log(f"Accuracy: {accuracy:.4f}", verbose=verbose)
        log(f"AUC Score: {auc_score:.4f}", verbose=verbose)

        return model, accuracy, auc_score

    except Exception as e:
        log(f"Even simple model failed: {e}", "warn", verbose)
        return None, None, None
