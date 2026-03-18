"""Patient data models and processing."""
import hashlib, time, logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, date

logger = logging.getLogger(__name__)

class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Vitals:
    heart_rate: Optional[int] = None  # bpm
    blood_pressure_sys: Optional[int] = None  # mmHg
    blood_pressure_dia: Optional[int] = None
    temperature: Optional[float] = None  # Celsius
    oxygen_saturation: Optional[float] = None  # percentage
    respiratory_rate: Optional[int] = None  # breaths/min
    recorded_at: float = field(default_factory=time.time)

    def assess_risk(self) -> RiskLevel:
        flags = 0
        if self.heart_rate and (self.heart_rate < 50 or self.heart_rate > 120): flags += 2
        if self.blood_pressure_sys and self.blood_pressure_sys > 180: flags += 2
        if self.temperature and (self.temperature < 35.0 or self.temperature > 39.5): flags += 2
        if self.oxygen_saturation and self.oxygen_saturation < 92: flags += 3
        if self.respiratory_rate and self.respiratory_rate > 25: flags += 1
        if flags >= 5: return RiskLevel.CRITICAL
        if flags >= 3: return RiskLevel.HIGH
        if flags >= 1: return RiskLevel.MODERATE
        return RiskLevel.LOW

@dataclass
class Patient:
    id: str
    name_hash: str  # PHI-safe hashed name
    age: int
    sex: str
    conditions: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    vitals_history: List[Vitals] = field(default_factory=list)

    @staticmethod
    def create_deidentified(name: str, age: int, sex: str, **kwargs) -> "Patient":
        name_hash = hashlib.sha256(name.lower().encode()).hexdigest()[:16]
        pid = f"PT-{name_hash[:8]}"
        return Patient(id=pid, name_hash=name_hash, age=age, sex=sex, **kwargs)

    @property
    def latest_vitals(self) -> Optional[Vitals]:
        return self.vitals_history[-1] if self.vitals_history else None

    @property
    def risk_level(self) -> RiskLevel:
        if not self.vitals_history:
            return RiskLevel.LOW
        return self.latest_vitals.assess_risk()

class RiskCalculator:
    """Calculate patient risk scores from clinical data."""

    CONDITION_WEIGHTS = {
        "diabetes": 2, "hypertension": 2, "copd": 3, "heart_failure": 4,
        "cancer": 3, "kidney_disease": 3, "liver_disease": 2, "stroke_history": 3,
        "immunocompromised": 3, "obesity": 1,
    }

    def calculate_risk_score(self, patient: Patient) -> Dict[str, Any]:
        base_score = 0
        factors = []

        # Age factor
        if patient.age >= 80: base_score += 4; factors.append("age>=80")
        elif patient.age >= 65: base_score += 2; factors.append("age>=65")

        # Conditions
        for condition in patient.conditions:
            weight = self.CONDITION_WEIGHTS.get(condition.lower(), 1)
            base_score += weight
            factors.append(f"{condition}(+{weight})")

        # Polypharmacy risk
        if len(patient.medications) >= 5:
            base_score += 2
            factors.append(f"polypharmacy({len(patient.medications)} meds)")

        # Vitals
        if patient.latest_vitals:
            vitals_risk = patient.latest_vitals.assess_risk()
            if vitals_risk == RiskLevel.CRITICAL: base_score += 5
            elif vitals_risk == RiskLevel.HIGH: base_score += 3
            elif vitals_risk == RiskLevel.MODERATE: base_score += 1

        # Normalize to 0-100
        normalized = min(100, base_score * 5)
        risk_level = (RiskLevel.CRITICAL if normalized >= 75 else
                     RiskLevel.HIGH if normalized >= 50 else
                     RiskLevel.MODERATE if normalized >= 25 else RiskLevel.LOW)

        return {"score": normalized, "risk_level": risk_level.value,
                "factors": factors, "conditions_count": len(patient.conditions),
                "medications_count": len(patient.medications)}
