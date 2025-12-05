import streamlit as st
from fpdf import FPDF
from datetime import datetime
import os

# --- CLASSE PDF (uguale a prima) ---
class PDFPreventivo(FPDF):
    def header(self):
        # Logo
        if os.path.exists('logo.jpg'):
            self.image('logo.jpg', 10, 8, 40)
        
        # Intestazione Azienda
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

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

# --- CONFIGURAZIONE PAGINA STREAMLIT ---
st.set_page_config(page_title="Preventivi 595 Rago Parts", page_icon="🚗")

st.title("🚗 Generatore Preventivi - 595 Rago Parts")

# --- GESTIONE STATO (MEMORIA) ---
# Serve per ricordare la lista dei prodotti quando clicchi i bottoni
if 'prodotti' not in st.session_state:
    st.session_state['prodotti'] = []

# --- INPUT DATI CLIENTE ---
col_cliente, col_data = st.columns([3, 1])
with col_cliente:
    cliente = st.text_input("Nome Cliente / Ragione Sociale")
with col_data:
    st.write(f"Data: **{datetime.now().strftime('%d/%m/%Y')}**")

st.divider()

# --- INPUT NUOVO PRODOTTO ---
st.subheader("Aggiungi Prodotto")
c1, c2, c3, c4 = st.columns([3, 1, 1, 1])

with c1:
    nome_prod = st.text_input("Descrizione Prodotto", key="input_nome")
with c2:
    qty_prod = st.number_input("Q.ta'", min_value=1, value=1, key="input_qty")
with c3:
    prezzo_prod = st.number_input("Prezzo Unit. (€)", min_value=0.0, format="%.2f", key="input_prezzo")
with c4:
    st.write("##") # Spaziatura per allineare il bottone
    if st.button("➕ Aggiungi"):
        if nome_prod:
            # Aggiunge alla lista in memoria
            st.session_state['prodotti'].append({
                "descrizione": nome_prod,
                "qty": qty_prod,
                "prezzo": prezzo_prod,
                "totale": qty_prod * prezzo_prod
            })
            st.success(f"Aggiunto: {nome_prod}")
            st.rerun() # Ricarica la pagina per aggiornare la tabella
        else:
            st.error("Inserisci il nome del prodotto!")

# --- VISUALIZZAZIONE LISTA PRODOTTI ---
if st.session_state['prodotti']:
    st.write("### Riepilogo Articoli")
    
    totale_imponibile = 0
    
    # Intestazione tabella a video
    h1, h2, h3, h4, h5 = st.columns([3, 1, 1, 1, 0.5])
    h1.markdown("**Descrizione**")
    h2.markdown("**Q.ta**")
    h3.markdown("**Prezzo**")
    h4.markdown("**Totale**")
    
    # Ciclo per mostrare i prodotti
    for i, p in enumerate(st.session_state['prodotti']):
        r1, r2, r3, r4, r5 = st.columns([3, 1, 1, 1, 0.5])
        r1.write(p["descrizione"])
        r2.write(p["qty"])
        r3.write(f"€ {p['prezzo']:.2f}")
        r4.write(f"€ {p['totale']:.2f}")
        
        # Bottone per eliminare riga
        if r5.button("🗑️", key=f"del_{i}"):
            st.session_state['prodotti'].pop(i)
            st.rerun()

        totale_imponibile += p["totale"]

    st.divider()

    # --- CALCOLI TOTALI ---
    iva = totale_imponibile * 0.22
    totale_finale = totale_imponibile + iva

    k1, k2 = st.columns([3, 1])
    with k2:
        st.markdown(f"**Imponibile:** € {totale_imponibile:.2f}")
        st.markdown(f"**IVA (22%):** € {iva:.2f}")
        st.markdown(f"### TOTALE: € {totale_finale:.2f}")

    # --- GENERAZIONE PDF ---
    st.write("---")
    if st.button("📄 Genera e Scarica Preventivo"):
        if not cliente:
            st.error("Inserisci il nome del cliente prima di scaricare!")
        else:
            # Creazione PDF in background
            pdf = PDFPreventivo()
            pdf.add_page()
            
            # Dati Cliente
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, f"Data: {datetime.now().strftime('%d/%m/%Y')}", 0, 1)
            pdf.cell(0, 10, f"Cliente: {cliente}", 0, 1)
            pdf.ln(10)

            # Intestazione Tabella
            pdf.set_fill_color(240, 240, 240)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(90, 10, "Descrizione", 1, 0, 'L', 1)
            pdf.cell(30, 10, "Q.ta'", 1, 0, 'C', 1)
            pdf.cell(35, 10, "Prezzo Unit.", 1, 0, 'R', 1)
            pdf.cell(35, 10, "Totale", 1, 1, 'R', 1)

            # Righe Tabella
            pdf.set_font("Arial", "", 11)
            for p in st.session_state['prodotti']:
                pdf.cell(90, 10, p['descrizione'], 1)
                pdf.cell(30, 10, str(p['qty']), 1, 0, 'C')
                pdf.cell(35, 10, f"{p['prezzo']:.2f}", 1, 0, 'R')
                pdf.cell(35, 10, f"{p['totale']:.2f}", 1, 1, 'R')

            # Totali
            pdf.ln(5)
            pdf.set_x(110)
            pdf.cell(45, 10, "Imponibile:", 0, 0, 'R')
            pdf.cell(35, 10, f"{totale_imponibile:.2f} euro", 1, 1, 'R')

            pdf.set_x(110)
            pdf.cell(45, 10, "IVA (22%):", 0, 0, 'R')
            pdf.cell(35, 10, f"{iva:.2f} euro", 1, 1, 'R')

            pdf.set_font("Arial", "B", 12)
            pdf.set_x(110)
            pdf.set_fill_color(255, 255, 0)
            pdf.cell(45, 10, "TOTALE:", 0, 0, 'R')
            pdf.cell(35, 10, f"{totale_finale:.2f} euro", 1, 1, 'R', 1)

            # Salvataggio temporaneo
            temp_filename = "preventivo_temp.pdf"
            pdf.output(temp_filename)

            # Leggiamo il file per il bottone di download
            with open(temp_filename, "rb") as f:
                pdf_data = f.read()

            st.download_button(
                label="📥 Clicca qui per scaricare il PDF",
                data=pdf_data,
                file_name=f"Preventivo_{cliente.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
            
            st.success("Preventivo generato con successo!")

else:
    st.info("Aggiungi il primo prodotto per iniziare il preventivo.")
