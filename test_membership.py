import pytest
from membership import MembershipSystem

class TestMembershipEquivalence:
    def setup_method(self):
        self.system = MembershipSystem()

    # Clase de Echivalență Valide
    def test_student_discount(self):
        # EP: status='STUDENT', age < 26 (ex: 20)
        assert self.system.calculate_fee(20, "STUDENT") == 50.0

    def test_senior_discount_by_status(self):
        # EP: status='SENIOR' (ex: age 40)
        assert self.system.calculate_fee(40, "SENIOR") == 60.0

    def test_regular_fee(self):
        # EP: status='REGULAR', age între 26 și 65 (ex: 30)
        assert self.system.calculate_fee(30, "REGULAR") == 100.0

    # Clase de Echivalență Invalide (Așteptăm erori)
    def test_invalid_age_negative(self):
        # EP: age < 0
        with pytest.raises(ValueError, match="Vârstă invalidă."):
            self.system.calculate_fee(-5, "REGULAR")

    def test_invalid_status(self):
        # EP: status invalid (ex: 'GUEST')
        with pytest.raises(ValueError, match="Status invalid."):
            self.system.calculate_fee(25, "GUEST")
            
            
            
class TestMembershipBVA:
    def setup_method(self):
        self.system = MembershipSystem()

    # Frontiere pentru vârstă invalidă (Min/Max)
    def test_age_boundary_negative(self):
        with pytest.raises(ValueError, match="Vârstă invalidă."):
            self.system.calculate_fee(-1, "REGULAR")

    def test_age_boundary_min_valid(self):
        assert self.system.calculate_fee(0, "REGULAR") == 100.0

    def test_age_boundary_max_valid(self):
        #assert self.system.calculate_fee(120, "REGULAR") == 100.0
        assert self.system.calculate_fee(120, "REGULAR") == 60.0

    def test_age_boundary_above_max(self):
        with pytest.raises(ValueError, match="Vârstă invalidă."):
            self.system.calculate_fee(121, "REGULAR")

    # Frontiere pentru reduceri (Student < 26)
    def test_student_boundary_25(self):
        # La 25 de ani încă primește reducere
        assert self.system.calculate_fee(25, "STUDENT") == 50.0

    def test_student_boundary_26(self):
        # La 26 de ani NU mai primește reducere de student
        assert self.system.calculate_fee(26, "STUDENT") == 100.0

    # Frontiere pentru reduceri (Senior >= 65)
    def test_senior_boundary_64(self):
        # La 64 de ani încă e tarif întreg (dacă statusul e REGULAR)
        assert self.system.calculate_fee(64, "REGULAR") == 100.0

    def test_senior_boundary_65(self):
        # La fix 65 de ani se aplică reducerea de senior (vârstă)
        assert self.system.calculate_fee(65, "REGULAR") == 60.0
        

class TestMembershipStructural:
    def setup_method(self):
        self.system = MembershipSystem()

    # Test pentru Decision Coverage: status STUDENT dar vârstă peste limită
    def test_student_over_age(self):
        assert self.system.calculate_fee(27, "STUDENT") == 100.0

    # Test pentru Decision Coverage: status REGULAR dar vârstă de senior
    def test_regular_senior_age(self):
        assert self.system.calculate_fee(70, "REGULAR") == 60.0

    # Test pentru Decision Coverage: status SENIOR dar vârstă tânără
    def test_senior_status_young_age(self):
        assert self.system.calculate_fee(30, "SENIOR") == 60.0

class TestMembershipMutation:
    def setup_method(self):
        self.system = MembershipSystem()

    def test_kill_mutant_12(self):
        # Fixează granița de student: la 26 de ani NU trebuie să aibă reducere.
        # Dacă mutantul 12 a schimbat < în <=, acest test va pica pe codul mutat.
        assert self.system.calculate_fee(26, "STUDENT") == 100.0

    def test_kill_mutant_21(self):
        # Fixează granița de senior: la 65 de ani TREBUIE să aibă reducere.
        # Dacă mutantul 21 a schimbat >= în >, la 65 de ani ar returna greșit 100.0.
        assert self.system.calculate_fee(65, "REGULAR") == 60.0
    
    # ==========================================
    # TESTE PENTRU A OMORÎ MUTANȚII SUPRAVIEȚUITORI
    # ==========================================

    def test_kill_string_mutant_age(self):
        # Folosim ^ și $ pentru a verifica EXACT string-ul.
        # Dacă mutmut adaugă "XX" la mesaj, testul va pica și mutantul moare.
        with pytest.raises(ValueError, match="^Vârstă invalidă.$"):
            self.system.calculate_fee(-1, "REGULAR")

    def test_kill_string_mutant_status(self):
        with pytest.raises(ValueError, match="^Status invalid.$"):
            self.system.calculate_fee(25, "GUEST")

    def test_kill_float_boundary_mutant_min(self):
        # Dacă mutmut schimbă 'age < 0' în 'age <= -1':
        # -0.1 dă eroare corect (omoară mutantul), pe când -1 trecea neobservat.
        with pytest.raises(ValueError, match="^Vârstă invalidă.$"):
            self.system.calculate_fee(-0.1, "REGULAR")

    def test_kill_float_boundary_mutant_max(self):
        # Dacă mutmut schimbă 'age > 120' în 'age >= 121':
        # 120.1 dă eroare corect.
        with pytest.raises(ValueError, match="^Vârstă invalidă.$"):
            self.system.calculate_fee(120.1, "REGULAR")
            
    def test_kill_float_boundary_student(self):
        # Dacă mutmut schimbă 'age < 26' în 'age <= 25':
        # 25.5 trebuie să primească reducere (50.0). Mutantul i-ar da tarif întreg (100.0).
        assert self.system.calculate_fee(25.5, "STUDENT") == 50.0