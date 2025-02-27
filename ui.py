import tkinter as tk
from qr import *

root = tk.Tk()
root.title('QR Gate System')
root.geometry("900x500")

main_fr = tk.Frame(root)
main_fr.pack(fill="both", expand=True)

left_fr = tk.Frame(main_fr, width=250, height=500)
left_fr.pack(side="left", fill="both", expand=True)

right_fr = tk.Frame(main_fr, width=250, height=500, bg="white")
right_fr.pack(side="right", fill="both", expand=True)

output_text = tk.Text(right_fr, wrap="word")
output_text.pack(fill="both", expand=True, padx=10, pady=10)

set_output_widget(output_text)

btn_fr = tk.Frame(left_fr)
btn_fr.pack(expand=True)

create_btn = tk.Button(btn_fr, text='Create', width=25, command=create)
scan_btn = tk.Button(btn_fr, text='Scan', width=25, command=scan)
reset_btn = tk.Button(btn_fr, text='Reset', width=25, command=clear)
del_btn = tk.Button(btn_fr, text='Delete', width=25, command=delete)

create_btn.grid(row=0, column=0, padx=10, pady=10)
scan_btn.grid(row=0, column=1, padx=10, pady=10)
reset_btn.grid(row=1, column=0, padx=10, pady=10)
del_btn.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
