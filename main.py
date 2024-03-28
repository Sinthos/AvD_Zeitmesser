import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime
from collections import deque
import xlsxwriter

#Notiz
class LightBarrierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lichtschranken-Zeiterfassung")

        self.timer_items = {}
        self.timer_queue = deque()

        # Tabelle erstellen
        self.tree = ttk.Treeview(root, columns=('Startzeit', 'Endzeit', 'Dauer'), show='headings')
        self.tree.heading('Startzeit', text='Startzeit')
        self.tree.heading('Endzeit', text='Endzeit')
        self.tree.heading('Dauer', text='Dauer (s)')
        self.tree.pack(expand=True, fill='both')

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
        item_id = self.tree.insert('', 'end', values=(start_time, 'Läuft...', '0.00 s'))
        self.timer_items[item_id] = start_time
        self.timer_queue.append(item_id)

    def set_end_time(self):
        if self.timer_queue:
            item_id = self.timer_queue.popleft()
            if item_id in self.timer_items:
                end_time = datetime.now()
                start_time = self.timer_items[item_id]
                duration = (end_time - start_time).total_seconds()
                self.tree.item(item_id, values=(start_time, end_time, '{:.2f} s'.format(duration)))
                del self.timer_items[item_id]

    def update_timer(self):
        now = datetime.now()
        for item_id, start_time in list(self.timer_items.items()):
            duration = (now - start_time).total_seconds()
            self.tree.item(item_id, values=(start_time, 'Läuft...', '{:.2f} s'.format(duration)))
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
            worksheet.write('A1', 'Startzeit')
            worksheet.write('B1', 'Endzeit')
            worksheet.write('C1', 'Dauer (s)')

            # Schreibe die Daten
            for i, item_id in enumerate(self.tree.get_children(), start=1):
                start_time, end_time, duration = self.tree.item(item_id)['values']
                worksheet.write(i, 0, str(start_time))
                worksheet.write(i, 1, str(end_time))
                worksheet.write(i, 2, str(duration))

            workbook.close()


if __name__ == '__main__':
    root = tk.Tk()
    app = LightBarrierApp(root)
    root.mainloop()
