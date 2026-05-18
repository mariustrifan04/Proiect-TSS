class MembershipSystem:
    def calculate_fee(self, age: int, status: str, years_active: int) -> float:
        """
        Specificație pentru Testarea Funcțională:
        -----------------------------------------
        Precondiții:
            - age (int): [0, 120]
            - status (str): {'STUDENT', 'SENIOR', 'REGULAR'}
            - years_active (int): >= 0
        Postcondiții:
            - Returnează taxa calculată (float).
            - Aruncă ValueError dacă datele de intrare încalcă precondițiile.
        """
        base_fee = 100.0
        valid_statuses = ["STUDENT", "SENIOR", "REGULAR"]

        # DECIZIA D1: Validare intrări
        if status not in valid_statuses or age < 0 or age > 120 or years_active < 0:
            raise ValueError("Date de intrare invalide.")
        else:
            # DECIZIA D2: Reducere Student
            if status == "STUDENT" and age < 26:
                base_fee = base_fee * 0.5
            # DECIZIA D3: Reducere Senior
            elif status == "SENIOR" or age >= 65:
                base_fee = base_fee * 0.6

        # Instruțiunea repetitivă: Calcul discount fidelitate (5% pe an, max 3 ani)
        loyalty_discount = 0.0
        iterations = min(years_active, 3) 
        
        while iterations > 0:
            loyalty_discount += 0.05
            iterations -= 1

        base_fee = base_fee * (1 - loyalty_discount)

        # DECIZIA D4: Prag minim de plată setat la 45.0 RON
        if base_fee < 45.0:
            base_fee = 45.0

        return base_fee