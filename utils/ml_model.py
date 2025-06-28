from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_model(df):
    # Target: Predict if next day's Close > today’s Close
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)

    # Feature engineering
    df['Price_Change'] = df['Close'].pct_change()
    df['RollingMean_5'] = df['Close'].rolling(5).mean()
    df['RollingStd_5'] = df['Close'].rolling(5).std()
    df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()

    df.dropna(inplace=True)

    features = ['RSI', '20DMA', '50DMA', 'Volume', 'Price_Change', 'RollingMean_5', 'RollingStd_5', 'MACD']
    X = df[features]
    y = df['Target']

    # Time-series aware split
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    # Define base models
    base_models = [
        ('rf', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)),
        ('xgb', XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42))
    ]

    # Define meta-learner
    meta_model = LogisticRegression()

    # Create stacking ensemble
    ensemble_model = StackingClassifier(
        estimators=base_models,
        final_estimator=meta_model,
        cv=5
    )

    # Train ensemble
    ensemble_model.fit(X_train, y_train)

    # Evaluate accuracy
    y_pred = ensemble_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return ensemble_model, accuracy
