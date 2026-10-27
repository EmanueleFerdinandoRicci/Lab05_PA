import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)

    # Inserimento nuovo strumento
    input_tipo = ft.TextField(label="Tipo", width=250)
    input_marca = ft.TextField(label="Marca", width=250)
    input_anno = ft.TextField(label="Anno di acquisto", width=250)

    # Contatore per il valore in euro dello strumento
    valore_strumento = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100, read_only=True)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento

    # Handlers per il contatore del valore
    def decrementa_valore(e):
        attuale = float(valore_strumento.value)
        if attuale >= 10:
            valore_strumento.value = str(int(attuale - 10))
        elif attuale > 0:
            valore_strumento.value = "0"
        page.update()

    def incrementa_valore(e):
        attuale = float(valore_strumento.value)
        valore_strumento.value = str(int(attuale + 10))
        page.update()

    # Handler per aggiungere un nuovo strumento
    def aggiungi_strumento(e):
        tipo = input_tipo.value.strip() if input_tipo.value else ""
        marca = input_marca.value.strip() if input_marca.value else ""
        anno_str = input_anno.value.strip() if input_anno.value else ""

        if not tipo or not marca or not anno_str:
            alert.show_alert("Compilare tutti i campi per inserire lo strumento.")
            return

        try:
            anno = int(anno_str)
        except ValueError:
            alert.show_alert("L'anno di acquisto deve essere un valore numerico intero.")
            return

        try:
            valore = float(valore_strumento.value)
        except ValueError:
            alert.show_alert("Il valore dello strumento non è valido.")
            return

        if valore <= 0:
            alert.show_alert("Il valore dello strumento deve essere maggiore di zero.")
            return

        # Aggiunta nel sistema
        deposito.aggiungi_strumento(tipo, marca, anno, valore)
        # Reset dei campi
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        valore_strumento.value = "0"
        # Aggiornamento vista
        aggiorna_lista_strumenti()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento

    btn_meno = ft.IconButton(icon=ft.Icons.REMOVE, on_click=decrementa_valore)
    btn_piu = ft.IconButton(icon=ft.Icons.ADD, on_click=incrementa_valore)
    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=aggiungi_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3: Aggiunta di Nuovi Strumenti
        ft.Divider(),
        ft.Text("Aggiungi Nuovo Strumento", size=20),
        ft.Row(
            controls=[input_tipo, input_marca, input_anno],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ),
        ft.Row(
            controls=[
                ft.Text("Valore (€):", size=16),
                btn_meno,
                valore_strumento,
                btn_piu,
                pulsante_aggiungi_strumento
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
