"""Basic usage example for patient-risk-predictor."""
from src.core import PatientRiskPredictor

def main():
    instance = PatientRiskPredictor(config={"verbose": True})

    print("=== patient-risk-predictor Example ===\n")

    # Run primary operation
    result = instance.track(input="example data", mode="demo")
    print(f"Result: {result}")

    # Run multiple operations
    ops = ["track", "predict", "forecast]
    for op in ops:
        r = getattr(instance, op)(source="example")
        print(f"  {op}: {"✓" if r.get("ok") else "✗"}")

    # Check stats
    print(f"\nStats: {instance.get_stats()}")

if __name__ == "__main__":
    main()
