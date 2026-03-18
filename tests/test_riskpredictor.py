"""Tests for RiskPredictor."""
import pytest
from src.riskpredictor import RiskPredictor

def test_init():
    obj = RiskPredictor()
    stats = obj.get_stats()
    assert stats["total_ops"] == 0

def test_operation():
    obj = RiskPredictor()
    result = obj.load_patient(input="test")
    assert result["processed"] is True
    assert result["operation"] == "load_patient"

def test_multiple_ops():
    obj = RiskPredictor()
    for m in ['load_patient', 'engineer_features', 'predict_readmission']:
        getattr(obj, m)(data="test")
    assert obj.get_stats()["total_ops"] == 3

def test_caching():
    obj = RiskPredictor()
    r1 = obj.load_patient(key="same")
    r2 = obj.load_patient(key="same")
    assert r2.get("cached") is True

def test_reset():
    obj = RiskPredictor()
    obj.load_patient()
    obj.reset()
    assert obj.get_stats()["total_ops"] == 0

def test_stats():
    obj = RiskPredictor()
    obj.load_patient(x=1)
    obj.engineer_features(y=2)
    stats = obj.get_stats()
    assert stats["total_ops"] == 2
    assert "ops_by_type" in stats
