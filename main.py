import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime
from collections import deque
import xlsxwriter


class LightBarrierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lichtschranken-Zeiterfassung")

        self.timer_items = {}
        self.timer_queue = deque()

        # Tabelle erstellen
        self.tree = ttk.Treeview(root,
                                 columns=('Messungsname', 'Startzeit', 'Endzeit', 'Dauer', 'Strafzeit', 'Ergebnis'),
                                 show='headings')
        self.tree.heading('Messungsname', text='Messungsname')
        self.tree.heading('Startzeit', text='Startzeit')
        self.tree.heading('Endzeit', text='Endzeit')
        self.tree.heading('Dauer', text='Dauer (s)')
        self.tree.heading('Strafzeit', text='Strafzeit')
        self.tree.heading('Ergebnis', text='Ergebnis')
        self.tree.pack(expand=True, fill='both')

        # Doppelklick-Event für das Editieren von Messungsnamen und Strafzeiten
        self.tree.bind("<Double-1>", self.on_item_double_click)

        # Knöpfe für Start- und Endzeit
        self.start_button = tk.Button(root, text="Startzeit festlegen", command=self.set_start_time)
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.end_button = tk.Button(root, text="Endzeit festlegen", command=self.set_end_time)
        self.end_button.pack(side=tk.RIGHT, padx=10)

        # Reset-Button
        self.reset_button = tk.Button(root, text="Alles zurücksetzen", command=self.reset_timers)
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Export-Button (Excel)
        self.export_button = tk.Button(root, text="Als Excel exportieren", command=self.export_to_excel)
        self.export_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Timer aktualisieren
        self.update_timer()

    def set_start_time(self):
        start_time = datetime.now()
        item_id = self.tree.insert('', 'end', values=('Unbenannt', start_time, 'Läuft...', '0.00 s', '0', '0.00 s'))
        self.timer_items[item_id] = (start_time, 'Läuft...')
        self.timer_queue.append(item_id)

    def set_end_time(self):
        if self.timer_queue:
            item_id = self.timer_queue.popleft()
            if item_id in self.timer_items:
                end_time = datetime.now()
                start_time, _ = self.timer_items[item_id]
                duration = (end_time - start_time).total_seconds()
                strafzeit = float(self.tree.item(item_id, 'values')[4])
                ergebnis = duration + strafzeit
                self.tree.item(item_id, values=(
                'Unbenannt', start_time, end_time, '{:.2f} s'.format(duration), strafzeit, '{:.2f} s'.format(ergebnis)))
                del self.timer_items[item_id]

    def on_item_double_click(self, event):
        # Spalten-ID zu Index-Mapping
        column_id_to_index = {'#1': 0, '#2': 1, '#3': 2, '#4': 3, '#5': 4}

        column = self.tree.identify_column(event.x)
        if column in column_id_to_index:
            item_id = self.tree.identify_row(event.y)
            entry = tk.Entry(self.tree)
            entry.insert(0, self.tree.item(item_id, 'values')[column_id_to_index[column]])
            entry.bind("<Return>", lambda e: self.update_item(entry, item_id, column_id_to_index[column]))
            entry.bind("<FocusOut>", lambda e: entry.destroy())
            entry.place(x=event.x, y=event.y)
            entry.focus_set()

    def update_item(self, entry, item_id, column_index):
        values = list(self.tree.item(item_id, 'values'))
        values[column_index] = entry.get()

        # Berechne das Ergebnis neu, wenn die Strafzeit aktualisiert wird
        if column_index == 4:  # Strafzeit-Spalte
            try:
                strafzeit = float(entry.get())
                duration = float(values[3].split(' ')[0])
                values[5] = '{:.2f} s'.format(duration + strafzeit)
            except ValueError:
                values[5] = 'Fehler'

        self.tree.item(item_id, values=values)
        entry.destroy()

    def update_timer(self):
        now = datetime.now()
        for item_id, (start_time, _) in list(self.timer_items.items()):
            duration = (now - start_time).total_seconds()
            self.tree.item(item_id, values=(
            'Unbenannt', start_time, 'Läuft...', '{:.2f} s'.format(duration), '0', '{:.2f} s'.format(duration)))
        self.root.after(100, self.update_timer)

    def reset_timers(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.timer_items.clear()
        self.timer_queue.clear()

    def export_to_excel(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                filetypes=[("Excel Dateien", "*.xlsx"), ("Alle Dateien", "*.*")])
        if filename:
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet()

            # Schreibe die Kopfzeilen
            worksheet.write('A1', 'Messungsname')
            worksheet.write('B1', 'Startzeit')
            worksheet.write('C1', 'Endzeit')
            worksheet.write('D1', 'Dauer (s)')
            worksheet.write('E1', 'Strafzeit')
            worksheet.write('F1', 'Ergebnis')

            # Schreibe die Daten
            for i, item_id in enumerate(self.tree.get_children(), start=1):
                messungsname, start_time, end_time, duration, strafzeit, ergebnis = self.tree.item(item_id)['values']
                worksheet.write(i, 0, messungsname)
                worksheet.write(i, 1, str(start_time))
                worksheet.write(i, 2, str(end_time))
                worksheet.write(i, 3, duration)
                worksheet.write(i, 4, strafzeit)
                worksheet.write(i, 5, ergebnis)

            workbook.close()


if __name__ == '__main__':
    root = tk.Tk()
    app = LightBarrierApp(root)
    root.mainloop()
