import os
import joblib
import pandas as pd
import numpy as np
import shap
import warnings
from Bio import SeqIO
from collections import Counter
from pathlib import Path

from .config import (
    DEFAULT_MODEL_PATH,
    AA_MAP, AA_KEY_TO_COL, AA_GROUPS, FEATURE_COLS, LABEL_MAP
)

warnings.filterwarnings("ignore")

def calculate_features(seq):
    seq = seq.upper()
    valid_aas = set(AA_MAP.keys())
    filtered_seq = [aa for aa in seq if aa in valid_aas]
    length = len(filtered_seq)
    
    if length == 0:
        return {col: 0.0 for col in FEATURE_COLS}
    
    counts = Counter(filtered_seq)
    features = {}
    
    # 1. Individual AA Ratios
    for aa, col in AA_KEY_TO_COL.items():
        features[col] = counts.get(aa, 0) / length
        
    # 2. Aggregated Ratios
    def get_sum_ratio(aas):
        return sum(counts.get(aa, 0) for aa in aas) / length
        
    features["酸性氨基酸总和比例"] = get_sum_ratio(AA_GROUPS["Acidic"])
    features["酸碱氨基酸总和比例"] = get_sum_ratio(AA_GROUPS["Acidic"] + AA_GROUPS["Basic"])
    features["亲水性氨基酸总和比例"] = get_sum_ratio(AA_GROUPS["Hydrophilic"])
    features["疏水性氨基酸总和比例"] = get_sum_ratio(AA_GROUPS["Hydrophobic"])
    
    return features

def process_fasta(file_path):
    try:
        records = list(SeqIO.parse(file_path, "fasta"))
        if not records:
            return None
        full_seq = "".join([str(r.seq) for r in records])
        features = calculate_features(full_seq)
        return features
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def interpret_model(model_pipeline, X_df, predicted_class_idx):
    print(f"\n--- Interpreting Prediction (Class: {LABEL_MAP[predicted_class_idx]}) ---")
    voting_clf = model_pipeline
    estimators_to_analyze = [
        ("ExtraTrees", voting_clf.named_estimators_['et']),
        ("RandomForest", voting_clf.named_estimators_['rf'])
    ]
    
    feature_contributions = {}
    
    for name, pipe in estimators_to_analyze:
        scaler = pipe.named_steps['scaler']
        clf = pipe.named_steps['clf']
        X_scaled = scaler.transform(X_df)
        explainer = shap.TreeExplainer(clf)
        shap_values = explainer.shap_values(X_scaled)
        
        # Handle SHAP output shape
        if isinstance(shap_values, list):
            shap_vals_target = shap_values[predicted_class_idx][0]
        elif len(shap_values.shape) == 3:
            shap_vals_target = shap_values[0, :, predicted_class_idx]
        else:
            shap_vals_target = shap_values[0] # Fallback
            
        sorted_indices = np.argsort(np.abs(shap_vals_target))[::-1]
        
        contributions = []
        for idx in sorted_indices:
            feat_name = FEATURE_COLS[idx]
            val = X_df.iloc[0, idx]
            shap_val = shap_vals_target[idx]
            
            if abs(shap_val) > 0.001:
                contributions.append({
                    "Feature": feat_name,
                    "Value": val,
                    "Contribution (SHAP)": shap_val,
                    "Effect": f"Supports '{LABEL_MAP[predicted_class_idx]}'" if shap_val > 0 else f"Opposes '{LABEL_MAP[predicted_class_idx]}'"
                })
        
        feature_contributions[name] = contributions
    return feature_contributions

def explain_rejections(model_pipeline, X_df, predicted_class_idx):
    pipe = model_pipeline.named_estimators_['et']
    scaler = pipe.named_steps['scaler']
    clf = pipe.named_steps['clf']
    X_scaled = scaler.transform(X_df)
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(X_scaled)
    
    rejection_reasons = {}
    
    for label_id, label_name in LABEL_MAP.items():
        if label_id == predicted_class_idx: continue
        
        if isinstance(shap_values, list):
             shap_vals_class = shap_values[label_id][0]
        elif len(shap_values.shape) == 3:
             shap_vals_class = shap_values[0, :, label_id]
        else:
             shap_vals_class = shap_values[0]
             
        sorted_indices = np.argsort(shap_vals_class)
        
        reasons = []
        for idx in sorted_indices[:5]:
            shap_val = shap_vals_class[idx]
            if shap_val < -0.001:
                reasons.append({
                    "Feature": FEATURE_COLS[idx],
                    "Value": X_df.iloc[0, idx],
                    "Negative Contribution": shap_val
                })
        
        rejection_reasons[label_name] = reasons
    return rejection_reasons

def run_prediction(input_file, output_prefix):
    if not DEFAULT_MODEL_PATH.exists():
        print(f"Error: Model file not found at {DEFAULT_MODEL_PATH}")
        return
        
    print("Loading SuSha Ensemble Model...")
    model = joblib.load(DEFAULT_MODEL_PATH)
    
    features = process_fasta(input_file)
    if not features:
        print("Failed to extract features.")
        return
        
    X_df = pd.DataFrame([features])[FEATURE_COLS]
    
    # Predict
    pred_idx = model.predict(X_df)[0]
    pred_label = LABEL_MAP.get(pred_idx, str(pred_idx))
    
    probs = model.predict_proba(X_df)[0]
    max_prob = np.max(probs)
    
    print(f"\n>>> Prediction Result: {pred_label} (Confidence: {max_prob:.2%}) <<<\n")
    
    # Interpret
    contributions = interpret_model(model, X_df, pred_idx)
    rejections = explain_rejections(model, X_df, pred_idx)
    
    # Save Results
    output_excel = f"{output_prefix}_SuSha_Result.xlsx"
    output_tsv = f"{output_prefix}_SuSha_Summary.tsv"
    
    # Summary TSV
    with open(output_tsv, "w", encoding="utf-8") as f:
        f.write(f"Genome\tPredicted_Salinity\tConfidence\n")
        f.write(f"{input_file.name}\t{pred_label}\t{max_prob:.4f}\n")
        
    # Detailed Excel
    with pd.ExcelWriter(output_excel) as writer:
        # Prediction Summary
        pd.DataFrame([{
            "Genome": input_file.name,
            "Predicted Salinity": pred_label,
            "Confidence": max_prob
        }]).to_excel(writer, sheet_name="Summary", index=False)
        
        # Support
        rows = []
        for model_name, contribs in contributions.items():
            for c in contribs:
                c["Model Component"] = model_name
                rows.append(c)
        pd.DataFrame(rows).to_excel(writer, sheet_name=f"Why {pred_label}", index=False)
        
        # Rejection
        rows_rej = []
        for label, reasons in rejections.items():
            for r in reasons:
                r["Rejected Class"] = label
                rows_rej.append(r)
        pd.DataFrame(rows_rej).to_excel(writer, sheet_name="Why Not Others", index=False)
        
        # Raw Features
        pd.DataFrame([features]).to_excel(writer, sheet_name="Raw Features", index=False)
        
    print(f"Results successfully saved to:\n  - {output_tsv}\n  - {output_excel}")
