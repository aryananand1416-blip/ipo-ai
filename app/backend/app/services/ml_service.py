
import os
import json
import joblib
import numpy as np
import pandas as pd


MODEL_DIR = "/content/drive/MyDrive/IPO_AI/models"

CLASSIFIER_PATH = os.path.join(
    MODEL_DIR,
    "ipo_ai_v1_classifier.joblib"
)

REGRESSOR_PATH = os.path.join(
    MODEL_DIR,
    "ipo_ai_v1_regressor.joblib"
)

FEATURES_PATH = os.path.join(
    MODEL_DIR,
    "ipo_ai_v1_features.json"
)

CONFIG_PATH = os.path.join(
    MODEL_DIR,
    "ipo_ai_v1_config.json"
)


# ------------------------------------------------------------
# LOAD PRODUCTION MODELS
# ------------------------------------------------------------

ipo_classifier = joblib.load(
    CLASSIFIER_PATH
)

ipo_regressor = joblib.load(
    REGRESSOR_PATH
)

with open(FEATURES_PATH, "r") as f:
    ipo_features = json.load(f)

with open(CONFIG_PATH, "r") as f:
    ipo_config = json.load(f)


# ------------------------------------------------------------
# AI SCORE
# ------------------------------------------------------------

def calculate_ai_score(
    positive_probability,
    predicted_return,
    day1_return,
    day2_return
):

    probability_score = (
        positive_probability * 100
    )

    return_score = (
        ((predicted_return + 5) / 10) * 100
    )

    return_score = np.clip(
        return_score,
        0,
        100
    )

    momentum = (
        day1_return + day2_return
    ) / 2

    momentum_score = (
        ((momentum + 10) / 20) * 100
    )

    momentum_score = np.clip(
        momentum_score,
        0,
        100
    )

    risk_penalty = max(
        0,
        min(
            (-momentum) * 3,
            30
        )
    )

    ai_score = (
        0.50 * probability_score +
        0.30 * return_score +
        0.20 * momentum_score -
        risk_penalty
    )

    ai_score = float(
        np.clip(ai_score, 0, 100)
    )

    if ai_score >= 75:
        risk = "LOW"
        signal = "STRONG WATCH"
    elif ai_score >= 65:
        risk = "MODERATE"
        signal = "WATCH"
    elif ai_score >= 50:
        risk = "HIGH"
        signal = "AVOID"
    else:
        risk = "VERY_HIGH"
        signal = "AVOID"

    return {
        "positive_probability": round(
            float(positive_probability),
            4
        ),
        "predicted_return": round(
            float(predicted_return),
            4
        ),
        "momentum": round(
            float(momentum),
            4
        ),
        "ai_score": round(
            ai_score,
            2
        ),
        "risk": risk,
        "signal": signal
    }


# ------------------------------------------------------------
# PREDICTION
# ------------------------------------------------------------

def predict_ipo_api(ipo_data):

    input_df = pd.DataFrame(
        [ipo_data]
    )

    # Convert API field names to production model names
    input_df = input_df.rename(columns={
        "IPO_Price": "IPO Price",
        "IPO_Size": "IPO Size",
        "P_E": "P/E"
    })

    input_df = input_df[
        ipo_features
    ]

    positive_probability = (
        ipo_classifier.predict_proba(
            input_df
        )[0][1]
    )

    predicted_return = (
        ipo_regressor.predict(
            input_df
        )[0]
    )

    day1_return = float(
        ipo_data["Day1_Return"]
    )

    day2_return = float(
        ipo_data["Day2_Return"]
    )

    result = calculate_ai_score(
        positive_probability,
        predicted_return,
        day1_return,
        day2_return
    )

    result["model_version"] = (
        ipo_config["model_version"]
    )

    result["prediction_stage"] = (
        ipo_config["prediction_stage"]
    )

    result["threshold"] = (
        ipo_config["threshold"]
    )

    return result
