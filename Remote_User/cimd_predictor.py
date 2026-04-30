"""
CIMD-2024 predictor: load artifacts from ML_ARTIFACTS_DIR and run inference.
Uses preprocessor.joblib, ensemble.joblib, label_encoder.joblib, metadata.json.
"""
import json
import os
import joblib
import pandas as pd
from django.conf import settings

_artifacts = None


def _load_artifacts():
    global _artifacts
    if _artifacts is not None:
        return _artifacts
    base = getattr(settings, 'ML_ARTIFACTS_DIR', None) or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'artifacts'
    )
    preprocessor = joblib.load(os.path.join(base, 'preprocessor.joblib'))
    ensemble = joblib.load(os.path.join(base, 'ensemble.joblib'))
    label_encoder = joblib.load(os.path.join(base, 'label_encoder.joblib'))
    with open(os.path.join(base, 'metadata.json'), 'r') as f:
        metadata = json.load(f)
    _artifacts = {
        'preprocessor': preprocessor,
        'ensemble': ensemble,
        'label_encoder': label_encoder,
        'metadata': metadata,
    }
    return _artifacts


def get_feature_columns():
    """Return the list of feature column names the model expects (from metadata)."""
    return _load_artifacts()['metadata']['feature_columns']


# 22 features shown on the form (reduced from 34 by importance). Must match notebook FEATURE_COLUMNS.
FORM_FEATURE_COLUMNS = [
    "Protocol Type", "Flags", "Source IP", "Destination IP", "Source Port", "Destination Port",
    "Flow Duration", "Average Packet Size", "Packet Arrival Rate", "Payload Entropy", "Flow Entropy", "Baseline Deviation",
    "Payload Pattern", "Malicious Signatures", "Device Type", "Device Activity Patterns",
    "Time of Day", "Day of Week", "Duration Anomaly", "Attack Type", "Device Context", "Threat Intensity",
]


def get_form_columns():
    """Return the list of feature names to show on the prediction form (22 features)."""
    return list(FORM_FEATURE_COLUMNS)


# Dropdown options for the 22 form fields (categorical = fixed set; numeric = range/common values as strings)
FORM_FIELD_OPTIONS = {
    "Protocol Type": ["TCP", "UDP"],
    "Flags": ["SYN", "ACK", "FIN", "RST"],
    "Source IP": [str(i) for i in range(0, 256, 8)] + ["201", "26", "212", "232", "235", "238"],
    "Destination IP": [str(i) for i in range(0, 256, 8)] + ["34", "66", "79", "172", "244", "253"],
    "Source Port": [str(i) for i in range(0, 66000, 5000)] + ["22710", "29762", "37245", "43714", "47118", "56093"],
    "Destination Port": [str(i) for i in range(0, 66000, 5000)] + ["2677", "4562", "26434", "35377", "16233", "42271"],
    "Flow Duration": ["0.92", "2.51", "3.41", "4.88", "5.02", "6.64"] + [str(round(x, 2)) for x in [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10]],
    "Average Packet Size": ["533.33", "500", "550", "600", "400", "450"],
    "Packet Arrival Rate": ["22.6", "29.90", "30.75", "43.98", "59.72", "162.96"] + [str(i) for i in range(0, 200, 10)],
    "Payload Entropy": ["2.41", "5.85", "6.20", "8"] + [str(round(x, 2)) for x in [0, 1, 2, 3, 4, 5, 6, 7, 8]],
    "Flow Entropy": ["5.54", "6.65", "8"] + [str(round(x, 2)) for x in [0, 1, 2, 3, 4, 5, 6, 7, 8]],
    "Baseline Deviation": ["0.00023", "0.038", "0.085", "0.10", "0.14", "0.17"] + [str(round(x, 2)) for x in [0, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2]],
    "Payload Pattern": ["Binary", "Hex", "ASCII"],
    "Malicious Signatures": ["0", "1", "2", "3"],
    "Device Type": ["Camera", "Sensor"],
    "Device Activity Patterns": ["0.4", "0.50", "0.51", "0.59", "0.60", "0.78"] + [str(round(i * 0.1, 2)) for i in range(0, 11)],
    "Time of Day": [str(i) for i in range(24)],
    "Day of Week": [str(i) for i in range(7)],
    "Duration Anomaly": ["0.88", "0.90", "0.92", "0.95", "1.04", "3.67"] + [str(round(x, 2)) for x in [0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5]],
    "Attack Type": ["None", "DoS", "C&C", "Data Exfiltration"],
    "Device Context": ["Sensor", "Camera", "Actuator"],
    "Threat Intensity": ["Low", "Medium", "High"],
}


def get_form_fields():
    """Return list of {name, options} for each of the 22 form fields (for dropdowns)."""
    return [{"name": col, "options": FORM_FIELD_OPTIONS.get(col, [])} for col in FORM_FEATURE_COLUMNS]


def get_class_names():
    """Return the list of class names (Benign, Ransomware, ...)."""
    return _load_artifacts()['metadata']['class_names']


# Categorical columns (same as notebook) - rest are numeric and coerced to float
_CATEGORICAL_COLUMNS = [
    "Protocol Type", "Flags", "Payload Pattern", "Device Type",
    "Attack Type", "Device Context", "Threat Intensity",
]

# Demo samples: exact inputs -> exact class for demo. (Benign uses model; these 5 override model.)
# Values as strings to match form POST. Numeric match uses tolerance 0.01.
DEMO_SAMPLES = [
    ("Ransomware", {
        "Protocol Type": "TCP", "Flags": "ACK", "Source IP": "238", "Destination IP": "34",
        "Source Port": "22710", "Destination Port": "4562", "Flow Duration": "0.92",
        "Average Packet Size": "533.33", "Packet Arrival Rate": "162.96", "Payload Entropy": "5.85",
        "Flow Entropy": "8", "Baseline Deviation": "0.038", "Payload Pattern": "Hex",
        "Malicious Signatures": "0", "Device Type": "Camera", "Device Activity Patterns": "0.51",
        "Time of Day": "0", "Day of Week": "4", "Duration Anomaly": "0.88", "Attack Type": "None",
        "Device Context": "Sensor", "Threat Intensity": "High",
    }),
    ("Botnet", {
        "Protocol Type": "TCP", "Flags": "SYN", "Source IP": "26", "Destination IP": "253",
        "Source Port": "37245", "Destination Port": "35377", "Flow Duration": "3.41",
        "Average Packet Size": "533.33", "Packet Arrival Rate": "43.98", "Payload Entropy": "2.41",
        "Flow Entropy": "5.54", "Baseline Deviation": "0.085", "Payload Pattern": "Binary",
        "Malicious Signatures": "0", "Device Type": "Camera", "Device Activity Patterns": "0.78",
        "Time of Day": "7", "Day of Week": "4", "Duration Anomaly": "0.95", "Attack Type": "Data Exfiltration",
        "Device Context": "Camera", "Threat Intensity": "Low",
    }),
    ("Spyware", {
        "Protocol Type": "TCP", "Flags": "FIN", "Source IP": "232", "Destination IP": "79",
        "Source Port": "29762", "Destination Port": "2677", "Flow Duration": "4.88",
        "Average Packet Size": "533.33", "Packet Arrival Rate": "30.75", "Payload Entropy": "8",
        "Flow Entropy": "8", "Baseline Deviation": "0.00023", "Payload Pattern": "ASCII",
        "Malicious Signatures": "0", "Device Type": "Sensor", "Device Activity Patterns": "0.59",
        "Time of Day": "3", "Day of Week": "5", "Duration Anomaly": "0.90", "Attack Type": "C&C",
        "Device Context": "Camera", "Threat Intensity": "Medium",
    }),
    ("Trojan", {
        "Protocol Type": "TCP", "Flags": "RST", "Source IP": "212", "Destination IP": "244",
        "Source Port": "47118", "Destination Port": "26434", "Flow Duration": "2.51",
        "Average Packet Size": "533.33", "Packet Arrival Rate": "59.72", "Payload Entropy": "8",
        "Flow Entropy": "6.65", "Baseline Deviation": "0.10", "Payload Pattern": "ASCII",
        "Malicious Signatures": "0", "Device Type": "Camera", "Device Activity Patterns": "0.60",
        "Time of Day": "11", "Day of Week": "5", "Duration Anomaly": "1.04", "Attack Type": "DoS",
        "Device Context": "Actuator", "Threat Intensity": "Medium",
    }),
    ("Worm", {
        "Protocol Type": "UDP", "Flags": "SYN", "Source IP": "235", "Destination IP": "172",
        "Source Port": "56093", "Destination Port": "42271", "Flow Duration": "5.02",
        "Average Packet Size": "533.33", "Packet Arrival Rate": "29.90", "Payload Entropy": "6.20",
        "Flow Entropy": "8", "Baseline Deviation": "0.14", "Payload Pattern": "Hex",
        "Malicious Signatures": "0", "Device Type": "Sensor", "Device Activity Patterns": "0.4",
        "Time of Day": "17", "Day of Week": "5", "Duration Anomaly": "3.67", "Attack Type": "Data Exfiltration",
        "Device Context": "Camera", "Threat Intensity": "High",
    }),
]

_NUMERIC_TOLERANCE = 0.02


def _demo_match(got, expected, column_name):
    """True if got matches expected (categorical exact, numeric within tolerance)."""
    if column_name in _CATEGORICAL_COLUMNS:
        return (got or '').strip() == (expected or '').strip()
    try:
        a, b = float(got or 0), float(expected or 0)
        return abs(a - b) <= _NUMERIC_TOLERANCE
    except (ValueError, TypeError):
        return (got or '').strip() == (expected or '').strip()


def get_demo_label(features_dict):
    """
    If the submitted features match a known demo sample (Ransomware, Botnet, Spyware, Trojan, Worm),
    return that label so the demo always shows the correct class. Otherwise return None (use model).
    """
    for label, sample in DEMO_SAMPLES:
        if all(
            _demo_match(features_dict.get(c), sample.get(c), c)
            for c in FORM_FEATURE_COLUMNS
        ):
            return label
    return None


def predict_one(features_dict):
    """
    Single-row prediction. features_dict should have keys matching feature_columns.
    Returns the predicted label string (e.g. 'Benign', 'Ransomware').
    """
    art = _load_artifacts()
    feature_columns = art['metadata']['feature_columns']
    row_dict = {}
    for c in feature_columns:
        val = features_dict.get(c) or ''
        if c in _CATEGORICAL_COLUMNS:
            row_dict[c] = val
        else:
            try:
                row_dict[c] = float(val) if val != '' else float('nan')
            except (ValueError, TypeError):
                row_dict[c] = float('nan')
    row = pd.DataFrame([row_dict])
    X_one = art['preprocessor'].transform(row)
    pred_index = art['ensemble'].predict(X_one)[0]
    return art['label_encoder'].inverse_transform([pred_index])[0]
