import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

# =====================================
# LOAD SNAPSHOT TRAINING TABLE
# =====================================
df = pd.read_csv("training_table.csv")

print("Rows:", len(df))

# =====================================
# SELECT FEATURES (MATCH APP INPUTS)
# =====================================
features = df[[
    "batting_team",
    "bowling_team",
    "city",
    "runs_left",
    "balls_left",
    "wickets_left",
    "runs_target",
    "crr",
    "rrr"
]]

target = df["batting_win"]

# =====================================
# ONE HOT ENCODE
# =====================================
X = pd.get_dummies(features)

print("Feature columns:", len(X.columns))

# =====================================
# TRAIN TEST SPLIT
# =====================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    target,
    test_size=0.2,
    random_state=42,
    stratify=target
)

print("Train:", len(X_train), "Test:", len(X_test))

# =====================================
# MODEL (TUNED FOR PROBABILITY)
# =====================================
model = RandomForestClassifier(
    n_estimators=700,
    max_depth=18,
    min_samples_leaf=20,
    class_weight="balanced",
    n_jobs=-1,
    random_state=42
)

model.fit(X_train, y_train)

# =====================================
# EVALUATE
# =====================================
pred = model.predict(X_test)
prob = model.predict_proba(X_test)[:,1]

acc = accuracy_score(y_test, pred)
auc = roc_auc_score(y_test, prob)

print("Accuracy:", round(acc,4))
print("ROC AUC:", round(auc,4))

# =====================================
# SAVE MODEL
# =====================================
pickle.dump(model, open("model.pkl","wb"))
pickle.dump(X.columns, open("columns.pkl","wb"))

print("✅ model.pkl saved")
print("✅ columns.pkl saved")
