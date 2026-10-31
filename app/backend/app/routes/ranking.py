
from fastapi import APIRouter

import pandas as pd

from app.services.ml_service import predict_ipo_api
from app.services.database import get_connection


router = APIRouter(
    prefix="/ranking",
    tags=["Ranking"]
)


@router.get("/status")
def ranking_status():

    return {
        "status": "ok",
        "service": "IPO ranking",
        "model_version": "IPO_AI_v1"
    }


@router.post("/")
def rank_ipos(
    data: list[dict]
):

    results = []

    # --------------------------------------------------------
    # Generate predictions
    # --------------------------------------------------------

    for ipo in data:

        prediction = predict_ipo_api(
            ipo
        )

        results.append({

            "IPO_ID": str(
                ipo.get(
                    "IPO_ID",
                    ipo.get(
                        "~id",
                        "UNKNOWN"
                    )
                )
            ),

            "IPO_Name": ipo.get(
                "IPO_Name",
                "Unknown"
            ),

            "positive_probability":
                prediction[
                    "positive_probability"
                ],

            "predicted_return":
                prediction[
                    "predicted_return"
                ],

            "momentum":
                prediction[
                    "momentum"
                ],

            "ai_score":
                prediction[
                    "ai_score"
                ],

            "risk":
                prediction[
                    "risk"
                ],

            "signal":
                prediction[
                    "signal"
                ]
        })

    # --------------------------------------------------------
    # Sort by AI Score
    # --------------------------------------------------------

    ranking_df = pd.DataFrame(
        results
    )

    ranking_df = ranking_df.sort_values(
        "ai_score",
        ascending=False
    ).reset_index(
        drop=True
    )

    ranking_df["rank"] = (
        ranking_df.index + 1
    )

    # --------------------------------------------------------
    # Save rankings to database
    # --------------------------------------------------------

    conn = get_connection()

    cursor = conn.cursor()

    for _, row in ranking_df.iterrows():

        cursor.execute(
            """
            INSERT INTO rankings (
                ipo_id,
                model_version,
                ai_rank,
                ai_score
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                str(row["IPO_ID"]),
                "IPO_AI_v1",
                int(row["rank"]),
                float(row["ai_score"])
            )
        )

    conn.commit()

    conn.close()

    # --------------------------------------------------------
    # API response
    # --------------------------------------------------------

    return {

        "status": "success",

        "model_version":
            "IPO_AI_v1",

        "count":
            len(ranking_df),

        "ranking":
            ranking_df.to_dict(
                orient="records"
            )
    }
