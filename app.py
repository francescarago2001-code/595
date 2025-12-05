from fpdf import FPDF
from datetime import datetime
import os

class PDFPreventivo(FPDF):
    def header(self):
        # --- LOGO ---
        # Verifica se il logo esiste, altrimenti salta
        if os.path.exists('logo.jpg'):
            # (nome_file, x, y, larghezza)
            self.image('logo.jpg', 10, 8, 40) 
        
        # --- INTESTAZIONE AZIENDA (Lato Destro) ---
        self.set_font('Arial', 'B', 14)
        self.cell(80) # Spazio vuoto per superare il logo
        self.cell(0, 10, '595 RAGO PARTS', 0, 1, 'R')
        
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Via Taverna, 82', 0, 1, 'R')
        self.cell(0, 5, 'Montaquila (IS)', 0, 1, 'R')
        self.cell(0, 5, 'Tel: 339 8180199', 0, 1, 'R')
        
        # Titolo documento
        self.ln(20) # A capo
        self.set_font('Arial', 'B', 20)
        self.cell(0, 10, 'PREVENTIVO', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        # Posizione a 1.5 cm dal fondo
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

def crea_preventivo():
    pdf = PDFPreventivo()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- DATI CLIENTE ---
    print("-" * 30)
    print("NUOVO PREVENTIVO - 595 RAGO PARTS")
    print("-" * 30)
    cliente = input("Inserisci nome/ragione sociale cliente: ")
    data_oggi = datetime.now().strftime("%d/%m/%Y")

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Data: {data_oggi}", 0, 1)
    pdf.cell(0, 10, f"Cliente: {cliente}", 0, 1)
    pdf.ln(10)

    # --- INTESTAZIONE TABELLA ---
    pdf.set_fill_color(240, 240, 240) # Grigio chiaro
    pdf.set_font("Arial", "B", 12)
    # Larghezze colonne: Prodotto, Quantità, Prezzo Unitario, Totale Riga
    pdf.cell(90, 10, "Descrizione Prodotto", 1, 0, 'L', 1)
    pdf.cell(30, 10, "Q.ta'", 1, 0, 'C', 1)
    pdf.cell(35, 10, "Prezzo Unit.", 1, 0, 'R', 1)
    pdf.cell(35, 10, "Totale", 1, 1, 'R', 1)

    # --- INSERIMENTO PRODOTTI ---
    totale_imponibile = 0
    pdf.set_font("Arial", "", 11)

    while True:
        descrizione = input("\nNome prodotto (o scrivi 'fine' per terminare): ")
        if descrizione.lower() == 'fine':
            break
        
        try:
            qty = int(input("Quantità: "))
            prezzo = float(input("Prezzo unitario (senza IVA): "))
        except ValueError:
            print("Errore: Inserisci numeri validi per quantità e prezzo.")
            continue

        subtotale_riga = qty * prezzo
        totale_imponibile += subtotale_riga

        # Aggiunta riga al PDF
        pdf.cell(90, 10, descrizione, 1)
        pdf.cell(30, 10, str(qty), 1, 0, 'C')
        pdf.cell(35, 10, f"{prezzo:.2f} euro", 1, 0, 'R')
        pdf.cell(35, 10, f"{subtotale_riga:.2f} euro", 1, 1, 'R')

    # --- CALCOLI FINALI ---
    iva_percentuale = 22
    totale_iva = totale_imponibile * (iva_percentuale / 100)
    totale_finale = totale_imponibile + totale_iva

    pdf.ln(5) # Spazio

    # Tabella riassuntiva a destra
    # Spostiamo il cursore a destra per allineare i totali
    pdf.set_x(110) 
    pdf.cell(45, 10, "Imponibile:", 0, 0, 'R')
    pdf.cell(35, 10, f"{totale_imponibile:.2f} euro", 1, 1, 'R')

    pdf.set_x(110)
    pdf.cell(45, 10, f"IVA ({iva_percentuale}%):", 0, 0, 'R')
    pdf.cell(35, 10, f"{totale_iva:.2f} euro", 1, 1, 'R')

    pdf.set_font("Arial", "B", 12)
    pdf.set_x(110)
    pdf.cell(45, 10, "TOTALE:", 0, 0, 'R')
    pdf.set_fill_color(255, 255, 0) # Giallo evidenziatore per il totale (richiamo al brand)
    pdf.cell(35, 10, f"{totale_finale:.2f} euro", 1, 1, 'R', 1)

    # --- SALVATAGGIO ---
    nome_file = f"Preventivo_{cliente.replace(' ', '_')}.pdf"
    pdf.output(nome_file)
    print(f"\n[SUCCESSO] Il file '{nome_file}' è stato creato correttamente nella cartella!")

if __name__ == "__main__":
    crea_preventivo()
