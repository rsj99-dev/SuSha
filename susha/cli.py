import argparse
import sys
from pathlib import Path
from .predict import run_prediction

def main():
    parser = argparse.ArgumentParser(
        description="SuSha: A multimodal ensemble learning prediction tool for microbial salinity adaptation."
    )
    
    parser.add_argument(
        "-i", "--input", 
        required=True, 
        help="Input genome protein sequence file (.faa / .fasta)"
    )
    
    parser.add_argument(
        "-o", "--output", 
        required=True, 
        help="Output Excel/TSV file prefix for prediction results and interpretation"
    )

    args = parser.parse_args()

    input_file = Path(args.input)
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
        
    print(f"Running SuSha prediction for: {input_file.name}")
    run_prediction(input_file, args.output)

if __name__ == "__main__":
    main()
