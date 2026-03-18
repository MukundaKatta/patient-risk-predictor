"""CLI for patient-risk-predictor."""
import sys, json, argparse
from .core import PatientRiskPredictor

def main():
    parser = argparse.ArgumentParser(description="Predict patient risk scores from EHR data for clinical decision support")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "run", "info"])
    parser.add_argument("--input", "-i", default="")
    args = parser.parse_args()
    instance = PatientRiskPredictor()
    if args.command == "status":
        print(json.dumps(instance.get_stats(), indent=2))
    elif args.command == "run":
        print(json.dumps(instance.track(input=args.input or "test"), indent=2, default=str))
    elif args.command == "info":
        print(f"patient-risk-predictor v0.1.0 — Predict patient risk scores from EHR data for clinical decision support")

if __name__ == "__main__":
    main()
