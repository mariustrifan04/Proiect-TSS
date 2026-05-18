import pytest
from membership import MembershipSystem

class TestMembershipEquivalence:
    """
    TESTARE BLACK-BOX: CLASE DE ECHIVALENȚĂ (EP)
    """
    def setup_method(self):
        self.system = MembershipSystem()

    def test_student_discount(self):
        # Student, age=20, vechime=0 -> base_fee devine 50.0 (nu scade sub 45.0, rămâne 50.0)
        assert self.system.calculate_fee(20, "STUDENT", 0) == 50.0

    def test_senior_discount_by_status(self):
        # Senior, age=40, vechime=0 -> base_fee devine 60.0
        assert self.system.calculate_fee(40, "SENIOR", 0) == 60.0

    def test_regular_fee(self):
        # Regular, age=30, vechime=0 -> base_fee rămâne 100.0
        assert self.system.calculate_fee(30, "REGULAR", 0) == 100.0

    def test_invalid_age_negative(self):
        with pytest.raises(ValueError, match="Date de intrare invalide."):
            self.system.calculate_fee(-5, "REGULAR", 0)

    def test_invalid_status(self):
        with pytest.raises(ValueError, match="Date de intrare invalide."):
            self.system.calculate_fee(25, "GUEST", 0)

    def test_invalid_years_active(self):
        with pytest.raises(ValueError, match="Date de intrare invalide."):
            self.system.calculate_fee(30, "REGULAR", -1)


class TestMembershipBVA:
    """
    TESTARE BLACK-BOX: VALORI DE FRONTIERĂ (BVA)
    """
    def setup_method(self):
        self.system = MembershipSystem()

    # Frontiera age minim absolut
    def test_age_boundary_negative(self):
        with pytest.raises(ValueError, match="Date de intrare invalide."):
            self.system.calculate_fee(-1, "REGULAR", 0)

    def test_age_boundary_min_valid(self):
        assert self.system.calculate_fee(0, "REGULAR", 0) == 100.0

    # Frontiera prag Student
    def test_student_boundary_25(self):
        assert self.system.calculate_fee(25, "STUDENT", 0) == 50.0

    def test_student_boundary_26(self):
        assert self.system.calculate_fee(26, "STUDENT", 0) == 100.0

    # Frontiera prag Senior
    def test_senior_boundary_64(self):
        assert self.system.calculate_fee(64, "REGULAR", 0) == 100.0

    def test_senior_boundary_65(self):
        assert self.system.calculate_fee(65, "REGULAR", 0) == 60.0

    # Frontiera age maxim absolut
    def test_age_boundary_max_valid(self):
        assert self.system.calculate_fee(120, "REGULAR", 0) == 60.0

    def test_age_boundary_above_max(self):
        with pytest.raises(ValueError, match="Date de intrare invalide."):
            self.system.calculate_fee(121, "REGULAR", 0)

    # Frontiera ani vechime
    def test_years_active_boundary_plafonare(self):
        # 100.0 RON cu 4 ani vechime (plafonare la 3 ani -> 15% reducere) = 85.0 RON
        assert self.system.calculate_fee(30, "REGULAR", 4) == 85.0

class TestMembershipStructural:
    """
    TESTARE STRUCTURALĂ: DECIZII ȘI BUCLE
    """
    def setup_method(self):
        self.system = MembershipSystem()

    def test_loyalty_discount_applied(self):
        # 2 ani vechime pentru Regular -> 10% reducere din 100.0 = 90.0 RON
        assert self.system.calculate_fee(30, "REGULAR", 2) == 90.0

    def test_minimum_fee_cutoff(self):
        # Student (50.0 RON) + 3 ani vechime (15% discount) = 42.5 RON
        # Deoarece 42.5 < 45.0, se activează decizia D4 și returnează fix 45.0 RON!
        assert self.system.calculate_fee(20, "STUDENT", 3) == 45.0
        
class TestMembershipMutation:
    def setup_method(self):
        self.system = MembershipSystem()

    def test_kill_string_mutant_unified_strict(self):
        with pytest.raises(ValueError, match="^Date de intrare invalide.$"):
            self.system.calculate_fee(-1, "REGULAR", 0)

    def test_kill_senior_conditions(self):
        assert self.system.calculate_fee(40, "SENIOR", 0) == 60.0
        assert self.system.calculate_fee(65, "REGULAR", 0) == 60.0

    def test_kill_loop_and_min_mutants(self):
        assert self.system.calculate_fee(30, "REGULAR", 1) == 95.0
        assert self.system.calculate_fee(30, "REGULAR", 2) == 90.0
        assert self.system.calculate_fee(30, "REGULAR", 3) == 85.0
        assert self.system.calculate_fee(30, "REGULAR", 4) == 85.0
        assert self.system.calculate_fee(30, "REGULAR", 5) == 85.0

    def test_kill_cutoff_mutants(self):
        # Student + 2 ani vechime = EXACT 45.0. Ucide mutanții '<' vs '<=' de la D4
        assert self.system.calculate_fee(20, "STUDENT", 2) == 45.0
        # Student + 1 an vechime = 47.5 (Trebuie să NU fie modificat de pragul de 45)
        assert self.system.calculate_fee(20, "STUDENT", 1) == 47.5

    def test_kill_student_exact_boundary_26(self):
        assert self.system.calculate_fee(26, "STUDENT", 0) == 100.0

    def test_kill_loyalty_zero_explicit(self):
        assert self.system.calculate_fee(30, "REGULAR", 0) == 100.0