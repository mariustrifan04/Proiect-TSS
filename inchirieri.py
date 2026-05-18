class CalculatorInchirieri:
    def calculeaza_pret(self, varsta, este_student, zile):
        pret_baza = 200
        
        # Validare date (pentru analiza valorilor de frontiera)
        if varsta < 18 or varsta > 80:
            raise ValueError("Varsta nepermisa pentru condus")
        
        if zile <= 0:
            return 0

        # Regula 1: Reducere tineri sau studenti (pentru acoperire conditii)
        if varsta < 25 or este_student:
            pret_final = pret_baza * 0.8  # 20% reducere
        else:
            pret_final = pret_baza

        # Regula 2: Reducere perioada lunga
        if zile > 7:
            pret_final -= 20
            
        return pret_final * zile