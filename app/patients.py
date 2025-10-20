from typing import Dict, List, TypedDict


class PatientRecord(TypedDict):
    """Representation of a dashboard patient with their feature vector."""

    id: str
    name: str
    features: Dict[str, float]


PATIENT_RECORDS: List[PatientRecord] = [
    {
        "id": "T-001",
        "name": "Alex Johnson",
        "features": {
            "age": 0.038076,
            "sex": 0.05068,
            "bmi": 0.061696,
            "bp": 0.021872,
            "s1": -0.044223,
            "s2": -0.034821,
            "s3": -0.043401,
            "s4": -0.002592,
            "s5": 0.019907,
            "s6": -0.017646,
        },
    },
    {
        "id": "T-002",
        "name": "Morgan Patel",
        "features": {
            "age": -0.001882,
            "sex": -0.044642,
            "bmi": -0.051474,
            "bp": -0.026328,
            "s1": -0.008449,
            "s2": -0.019163,
            "s3": 0.074412,
            "s4": -0.039493,
            "s5": -0.068332,
            "s6": -0.092204,
        },
    },
    {
        "id": "T-003",
        "name": "Jamie Lee",
        "features": {
            "age": 0.085299,
            "sex": 0.05068,
            "bmi": 0.044451,
            "bp": -0.00567,
            "s1": -0.045599,
            "s2": -0.034194,
            "s3": -0.032356,
            "s4": -0.002592,
            "s5": 0.002861,
            "s6": -0.02593,
        },
    },
    {
        "id": "T-004",
        "name": "Riley Chen",
        "features": {
            "age": -0.089063,
            "sex": -0.044642,
            "bmi": -0.011595,
            "bp": -0.036656,
            "s1": 0.012191,
            "s2": 0.024991,
            "s3": -0.036038,
            "s4": 0.034309,
            "s5": 0.022688,
            "s6": -0.009362,
        },
    },
    {
        "id": "T-005",
        "name": "Casey Martinez",
        "features": {
            "age": 0.005383,
            "sex": -0.044642,
            "bmi": -0.036385,
            "bp": 0.021872,
            "s1": 0.003935,
            "s2": 0.015596,
            "s3": 0.008142,
            "s4": -0.002592,
            "s5": -0.031988,
            "s6": -0.046641,
        },
    },
]
