import pytest
from inchirieri import CalculatorInchirieri

def test_clase_echivalenta_si_frontiera():
    calc = CalculatorInchirieri()
    # Frontiera: fix 18 ani (valid)
    assert calc.calculeaza_pret(18, False, 1) == 160 
    # Frontiera: 17 ani (ar trebui sa dea eroare)
    with pytest.raises(ValueError):
        calc.calculeaza_pret(17, False, 1)

def test_acoperire_decizii_si_conditii():
    calc = CalculatorInchirieri()
    # Testam conditia compusa: varsta < 25 OR este_student
    # 1. Varsta < 25 (True), Student (False) -> Intra pe reducere
    assert calc.calculeaza_pret(20, False, 1) == 160
    # 2. Varsta >= 25 (False), Student (True) -> Intra pe reducere
    assert calc.calculeaza_pret(30, True, 1) == 160
    # 3. Ambele False -> Pret intreg
    assert calc.calculeaza_pret(30, False, 1) == 200

def test_circuite_independente_si_zile_lungi():
    calc = CalculatorInchirieri()
    # Drumul care trece prin reducerea de peste 7 zile
    # (30 ani, nu e student, 10 zile) -> 200 pret - 20 reducere = 180 * 10 = 1800
    assert calc.calculeaza_pret(30, False, 10) == 1800