class MembershipSystem:
    def calculate_fee(self, age: int, status: str) -> float:
        """
        Calculează taxa de membru. Taxa de bază este 100 RON.
        - Vârstă invalidă: < 0 sau > 120 (aruncă eroare)
        - Studenți (status='STUDENT') sub 26 ani: 50% reducere
        - Seniori (status='SENIOR') sau persoane peste 65 ani: 40% reducere
        - Restul: Taxă întreagă (100 RON)
        """
        base_fee = 100.0
        valid_statuses = ["STUDENT", "SENIOR", "REGULAR"]

        if status not in valid_statuses:
            raise ValueError("Status invalid.")

        if age < 0 or age > 120:
            raise ValueError("Vârstă invalidă.")

        # Logica de reducere (pentru testare structurală/coverage)
        if status == "STUDENT" and age < 26:
            return base_fee * 0.5
            
        if status == "SENIOR" or age >= 65:
            return base_fee * 0.6

        return base_fee