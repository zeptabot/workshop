import requests
import json
import os

json_url = 'https://raw.githubusercontent.com/bogdanfazakas/datasets/refs/heads/main/data.json'
output_folder = '/data/outputs'
output_file = os.path.join(output_folder, 'results.json')


import requests
import json
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import datetime

json_url = 'https://raw.githubusercontent.com/bogdanfazakas/datasets/refs/heads/main/data.json'
output_folder = '/data/outputs'
output_file = os.path.join(output_folder, 'results.json')


def load_and_prepare_data(url):
    response = requests.get(url)
    response.raise_for_status()
    properties = response.json()

    rows = []
    for prop in properties:
        info = prop.get("info", prop)  # fallback to prop if 'info' not present

        # Convert createdOn to days since listing
        created_on = info.get("createdOn")
        days_since = None
        if created_on:
            try:
                date_obj = datetime.datetime.strptime(created_on, "%d %B %Y")
                days_since = (datetime.datetime.now() - date_obj).days
            except Exception:
                days_since = None

        rows.append({
            "ccy": info.get("ccy"),
            "type": info.get("type"),
            "zone": info.get("zone"),
            "refNo": info.get("refNo"),
            "roomsNo": info.get("roomsNo"),
            "surface": info.get("surface"),
            "createdOn_days": days_since,
            "bathroomsNo": info.get("bathroomsNo"),
            "price": info.get("price")
        })

    df = pd.DataFrame(rows)
    print("📊 DataFrame before dropping NA:\n", df.head())

    # Drop rows with missing values in important columns
    df = df.dropna(subset=[
        "ccy", "type", "zone", "refNo", "roomsNo", "surface", "createdOn_days", "bathroomsNo", "price"
    ])

    if df.empty:
        raise ValueError("No data left after dropping rows with missing values. Please check your dataset.")

    # Drop 'url' (not useful for prediction)
    X = df.drop(["price", "url"], axis=1, errors='ignore')
    y = df["price"]

    # One-hot encode categorical features
    X = pd.get_dummies(X, columns=["ccy", "type", "zone", "refNo"])

    # Scale numerical features
    scaler = StandardScaler()
    X[["roomsNo", "surface", "createdOn_days", "bathroomsNo"]] = scaler.fit_transform(
        X[["roomsNo", "surface", "createdOn_days", "bathroomsNo"]]
    )

    return X, y

# Prepare data
X, y = load_and_prepare_data(json_url)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Regressor
rf = RandomForestRegressor(n_estimators=10, random_state=42)
rf.fit(X_train, y_train)

# Predict on test set
y_pred = rf.predict(X_test)

# Prepare terminal output
sample_predictions_df = pd.DataFrame({"Actual": y_test, "Predicted": y_pred}).head()
r2 = r2_score(y_test, y_pred)
terminal_output = [
    f"✅ Random Forest predictions written to: {output_file}",
    "📊 Sample predictions:\n" + sample_predictions_df.to_string(index=False),
    f"R^2 prediction accuracy: {r2:.4f}"
]
print("\n".join(terminal_output))


# Save everything to output file
os.makedirs(output_folder, exist_ok=True)
with open(output_file, "w") as f:
    json.dump({
        "R^2 prediction accuracy": r2,
        "results": [
            {"Actual": float(a), "Predicted": float(p)}
            for a, p in zip(y_test, y_pred)
        ]
    }, f, indent=2)
