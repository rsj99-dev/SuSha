import os
from pathlib import Path

# Package root directory
PACKAGE_ROOT = Path(__file__).parent.absolute()

# Model paths
MODEL_DIR = PACKAGE_ROOT / "models"
DEFAULT_MODEL_PATH = MODEL_DIR / "Ensemble1_ET_RF_Bag.pkl"

# Feature Definition (24 Dimensions)
AA_MAP = {
    "A": "丙氨酸 (Ala)", "C": "半胱氨酸 (Cys)", "D": "天冬氨酸 (Asp)", "E": "谷氨酸 (Glu)", "F": "苯丙氨酸 (Phe)",
    "G": "甘氨酸 (Gly)", "H": "组氨酸 (His)", "I": "异亮氨酸 (Ile)", "K": "赖氨酸 (Lys)", "L": "亮氨酸 (Leu)",
    "M": "甲硫氨酸 (Met)", "N": "天冬酰胺 (Asn)", "P": "脯氨酸 (Pro)", "Q": "谷氨酰胺 (Gln)", "R": "精氨酸 (Arg)",
    "S": "丝氨酸 (Ser)", "T": "苏氨酸 (Thr)", "V": "缬氨酸 (Val)", "W": "色氨酸 (Trp)", "Y": "酪氨酸 (Tyr)"
}
AA_KEY_TO_COL = {k: f"{v.split(' ')[0]}比例" for k, v in AA_MAP.items()}

AA_GROUPS = {
    "Acidic": ["D", "E"],
    "Basic": ["K", "R", "H"],
    "PolarUncharged": ["S", "T", "C", "Y", "N", "Q"],
    "Hydrophobic": ["A", "V", "L", "I", "M", "F", "W", "P"], 
    "Hydrophilic": ["S", "T", "C", "Y", "N", "Q", "D", "E", "K", "R", "H"]
}

AA_COLS = [f"{v.split(' ')[0]}比例" for k, v in AA_MAP.items()] 
AGG_COLS = [
    "酸性氨基酸总和比例",
    "酸碱氨基酸总和比例",
    "亲水性氨基酸总和比例",
    "疏水性氨基酸总和比例"
]
FEATURE_COLS = AA_COLS + AGG_COLS

LABEL_MAP = {
    0: "Salt-sensitive",
    1: "Halotolerant",
    2: "Slight halophilic",
    3: "Moderate halophilic",
    4: "Extreme halophilic"
}
