import os
import sys

# --- INSTALLAZIONE AUTOMATICA LIBRERIA ---
# Questo pezzo serve per installare fpdf automaticamente su GitHub Codespaces
try:
    from fpdf import FPDF
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf"])
    from fpdf import FPDF

from datetime import datetime

class PDFPreventivo(FPDF):
    def header(self):
        # --- LOGO ---
        # Cerca il file logo.jpg nella stessa cartella
        if os.path.exists('logo.jpg'):
            self.image('logo.jpg', 10, 8, 40)
        else:
            # Se non trova il logo, scrive solo il nome
            self.set_font('Arial', 'B', 12)
            self.cell(50, 10, "[LOGO QUI]", 1, 0, 'C')

        # --- INTESTAZIONE AZIENDA ---
        self.set_font('Arial', 'B', 14)
        self.cell(80) 
        self.cell(0, 10, '595 RAGO PARTS', 0, 1, 'R')
        
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Via Taverna, 82', 0, 1, 'R')
        self.cell(0, 5, 'Montaquila (IS)', 0, 1, 'R')
        self.cell(0, 5, 'Tel: 339 8180199', 0, 1, 'R')
        
        self.ln(20)
        self.set_font('Arial', 'B', 20)
        self.cell(0, 10, 'PREVENTIVO', 0, 1, 'C')
        self.ln(10)

def crea_preventivo():
    pdf = PDFPreventivo()
    pdf.add_page()
    
    print("\n" + "="*40)
    print("   CREAZIONE PREVENTIVO 595 RAGO PARTS")
    print("="*40)
    
    cliente = input("Inserisci nome Cliente: ")
    data_oggi = datetime.now().strftime("%d/%m/%Y")

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Data: {data_oggi}", 0, 1)
    pdf.cell(0, 10, f"Cliente: {cliente}", 0, 1)
    pdf.ln(10)

    # Intestazione Tabella
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(90, 10, "Descrizione", 1, 0, 'L', 1)
    pdf.cell(30, 10, "Q.ta'", 1, 0, 'C', 1)
    pdf.cell(35, 10, "Prezzo Unit.", 1, 0, 'R', 1)
    pdf.cell(35, 10, "Totale", 1, 1, 'R', 1)

    totale_imponibile = 0
    pdf.set_font("Arial", "", 11)

    while True:
        descrizione = input("\nNome prodotto (o scrivi 'fine'): ")
        if descrizione.lower() == 'fine':
            break
        
        try:
            qty = int(input("Quantità: "))
            prezzo = float(input("Prezzo (IVA esclusa): "))
        except ValueError:
            print("Errore: usa solo numeri (usa il punto per i decimali, es. 10.50)")
            continue

        subtotale = qty * prezzo
        totale_imponibile += subtotale

        pdf.cell(90, 10, descrizione, 1)
        pdf.cell(30, 10, str(qty), 1, 0, 'C')
        pdf.cell(35, 10, f"{prezzo:.2f}", 1, 0, 'R')
        pdf.cell(35, 10, f"{subtotale:.2f}", 1, 1, 'R')

    # Totali
    iva = totale_imponibile * 0.22
    totale = totale_imponibile + iva

    pdf.ln(5)
    pdf.set_x(110)
    pdf.cell(45, 10, "Imponibile:", 0, 0, 'R')
    pdf.cell(35, 10, f"{totale_imponibile:.2f}", 1, 1, 'R')

    pdf.set_x(110)
    pdf.cell(45, 10, "IVA (22%):", 0, 0, 'R')
    pdf.cell(35, 10, f"{iva:.2f}", 1, 1, 'R')

    pdf.set_font("Arial", "B", 12)
    pdf.set_x(110)
    pdf.set_fill_color(255, 255, 0) 
    pdf.cell(45, 10, "TOTALE:", 0, 0, 'R')
    pdf.cell(35, 10, f"{totale:.2f} euro", 1, 1, 'R', 1)

    nome_file = f"Preventivo_{cliente.replace(' ', '_')}.pdf"
    pdf.output(nome_file)
    print(f"\n[OK] Fatto! Trovi il file '{nome_file}' nella colonna a sinistra.")

if __name__ == "__main__":
    crea_preventivo()
