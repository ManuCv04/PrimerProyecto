class AIModule:
    def __init__(self, db):
        self.db = db

    def analyze(self, text):
        text = text.lower()

        # =========================
        # 🔴 GRAVE (EMERGENCIAS)
        # =========================
        grave = [
            "dolor en el pecho", "falta de aire", "no puedo respirar",
            "fractura", "hueso roto", "me rompí",
            "convulsión", "desmayo", "pérdida de conciencia",
            "sangrado abundante", "hemorragia",
            "presión en la nuca", "rigidez de cuello",
            "dolor intenso abdominal", "apendicitis",
            "quemadura grave", "descarga eléctrica",
            "parálisis", "no puedo mover",
            "ataque", "infarto", "derrame",
            "dolor torácico", "asfixia"
        ]

        if any(x in text for x in grave):
            return {
                "diagnosis": "Condición potencialmente grave",
                "recommendation": "⚠️ ACUDA A EMERGENCIAS O CONSULTE UN MÉDICO INMEDIATAMENTE"
            }

        # =========================
        # 🟡 MODERADO
        # =========================
        if any(x in text for x in ["dolor persistente", "infección", "fiebre alta"]):
            return {
                "diagnosis": "Condición moderada",
                "recommendation": "Consulte médico si no mejora en 24-48 horas"
            }

        # =========================
        # 🟢 LEVE / OTC
        # =========================

        conditions = [
            # cabeza
            ("cabeza", "Dolor de cabeza", "Paracetamol, ibuprofeno"),
            ("migraña", "Migraña", "Ibuprofeno, reposo en oscuridad"),
            ("mareo", "Mareo", "Hidratación, reposo"),
            
            # respiratorio
            ("tos", "Tos", "Jarabe para la tos"),
            ("gripe", "Gripe", "Antigripales"),
            ("resfriado", "Resfriado común", "Vitamina C, líquidos"),
            ("congestión", "Congestión nasal", "Descongestionantes"),
            ("asma leve", "Crisis leve", "Inhalador (si tiene)"),

            # digestivo
            ("nausea", "Náuseas", "Dimenhidrinato"),
            ("náusea", "Náuseas", "Dimenhidrinato"),
            ("vomito", "Vómitos", "Suero oral"),
            ("diarrea", "Diarrea", "Loperamida, suero"),
            ("gastritis", "Gastritis", "Omeprazol"),
            ("acidez", "Acidez", "Antiácidos"),
            ("indigestión", "Indigestión", "Digestivos"),

            # muscular
            ("muscular", "Dolor muscular", "Ibuprofeno"),
            ("espalda", "Dolor lumbar", "Diclofenaco"),
            ("contractura", "Contractura", "Masajes, calor"),

            # piel
            ("alergia", "Alergia", "Loratadina"),
            ("picazón", "Irritación", "Antihistamínicos"),
            ("quemadura leve", "Quemadura leve", "Aloe vera"),
            ("corte", "Herida leve", "Desinfectar"),

            # general
            ("fiebre", "Fiebre leve", "Paracetamol"),
            ("fatiga", "Fatiga", "Descanso"),
            ("cansancio", "Cansancio", "Vitaminas"),
            ("deshidratación", "Deshidratación", "Suero oral"),

            # garganta
            ("garganta", "Dolor de garganta", "Pastillas, paracetamol"),

            # oído
            ("oído", "Dolor de oído", "Analgésicos"),

            # ojos
            ("ojos", "Irritación ocular", "Lágrimas artificiales"),

            # dental
            ("diente", "Dolor dental", "Ibuprofeno (ver dentista)"),

            # más (expandido)
            ("calambre", "Calambres", "Magnesio"),
            ("estrés", "Estrés", "Relajación"),
            ("ansiedad", "Ansiedad leve", "Respiración guiada"),
            ("insomnio", "Insomnio", "Higiene del sueño"),
            ("golpe leve", "Contusión", "Hielo"),
            ("torcedura", "Esguince leve", "Reposo, hielo"),
            ("inflamación", "Inflamación", "Ibuprofeno"),
            ("ardor", "Irritación", "Cremas tópicas"),
            ("resequedad", "Piel seca", "Hidratante"),
            ("sudoración", "Exceso sudor", "Hidratación"),
        ]

        for keyword, diagnosis, treatment in conditions:
            if keyword in text:
                return {
                    "diagnosis": diagnosis,
                    "recommendation": treatment
                }

        # =========================
        # ❓ DEFAULT
        # =========================
        return {
            "diagnosis": "No identificado",
            "recommendation": "No se pudo determinar. Consulte con un médico."
        }