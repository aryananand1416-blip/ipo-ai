
from fastapi import APIRouter

from app.models.ipo_request import IPOPredictionRequest
from app.services.ml_service import predict_ipo_api
from app.services.database import (
    save_prediction,
    save_ipo
)


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


@router.get("/status")
def prediction_status():

    return {
        "status": "ready",
        "model_version": "IPO_AI_v1",
        "prediction_stage": "end_of_day_2"
    }


@router.post("/")
def predict_ipo_endpoint(
    data: IPOPredictionRequest
):

    ipo_data = data.model_dump(
        by_alias=True
    )

    prediction = predict_ipo_api(
        ipo_data
    )

    # --------------------------------------------------------
    # IPO identification
    # --------------------------------------------------------

    ipo_id = str(
        ipo_data.get(
            "IPO_ID",
            ipo_data.get(
                "~id",
                ipo_data.get(
                    "IPO_Name",
                    "UNKNOWN"
                )
            )
        )
    )

    ipo_name = str(
        ipo_data.get(
            "IPO_Name",
            "Unknown"
        )
    )

    listing_date = ipo_data.get(
        "Listing_Date"
    )

    listing_price = ipo_data.get(
        "Listing_Price"
    )

    day1_return = ipo_data.get(
        "Day1_Return"
    )

    day2_return = ipo_data.get(
        "Day2_Return"
    )

    # --------------------------------------------------------
    # Save IPO
    # --------------------------------------------------------

    save_ipo(
        ipo_id=ipo_id,
        ipo_name=ipo_name,
        listing_date=listing_date,
        listing_price=listing_price,
        day1_return=day1_return,
        day2_return=day2_return
    )

    # --------------------------------------------------------
    # Save prediction
    # --------------------------------------------------------

    prediction_id = save_prediction(
        ipo_id=ipo_id,
        model_version=prediction["model_version"],
        prediction_stage=prediction["prediction_stage"],
        positive_probability=prediction["positive_probability"],
        predicted_return=prediction["predicted_return"],
        momentum=prediction["momentum"],
        ai_score=prediction["ai_score"],
        risk=prediction["risk"],
        signal=prediction["signal"]
    )

    return {
        "status": "success",
        "prediction_id": prediction_id,
        "ipo_id": ipo_id,
        "ipo_name": ipo_name,
        "model_version": prediction["model_version"],
        "prediction_stage": prediction["prediction_stage"],
        "threshold": prediction["threshold"],
        "positive_probability": prediction["positive_probability"],
        "predicted_return": prediction["predicted_return"],
        "momentum": prediction["momentum"],
        "ai_score": prediction["ai_score"],
        "risk": prediction["risk"],
        "signal": prediction["signal"]
    }
