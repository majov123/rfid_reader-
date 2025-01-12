import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import socket
import threading


php_url = "http://localhost/script.php"

user_data = {}

# Funkcia na získanie údajov z PHP skriptu
def get_user_data(isic_id):
    try:
        response = requests.post(php_url, data={"isic_id": isic_id})
        data = response.json()
        if "error" in data:
            return {"error": data["error"]}
        return {
            "meno": data["meno"],
            "priezvisko": data["priezvisko"],
            "cislo_izby": data["cislo_izby"],
            "bezdr_pripojenie_mac": data.get("bezdr_pripojenie_mac", "neevidovane"),
            "bezdr_pripojenie_ip": data.get("bezdr_pripojenie_ip", "neevidovane"),
            "pevne_pripojenie_ip": data.get("pevne_pripojenie_ip", "neevidovane"),
            "pevne_pripojenie_mac": data.get("pevne_pripojenie_mac", "neevidovane")
        }
    except Exception as e:
        return {"error": f"Chyba pripojenia: {e}"}

# Funkcia na spracovanie priloženia ISIC karty
def handle_isic(isic_id):
    global user_data
    user_data = get_user_data(isic_id)

    if "error" in user_data:
        messagebox.showerror("Chyba", f"ISIC karta sa nenašla: {user_data['error']}")

# Simulácia čítania ISIC karty z čítačky (socket server)
def read_from_reader():
    try:
        # Nastav socket pre čítačku
        reader_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        reader_socket.bind(("0.0.0.0", 12345))  # Port čítačky
        reader_socket.listen(1)
        print("Čakám na pripojenie čítačky...")

        while True:
            conn, addr = reader_socket.accept()
            print(f"Pripojené: {addr}")
            isic_id = conn.recv(1024).decode().strip()
            if isic_id:
                print(f"Prijaté ISIC ID: {isic_id}")
                handle_isic(isic_id)
            conn.close()
    except Exception as e:
        print(f"Čítačka nie je dostupná: {e}")


def show_user_info(info_type):
    if not user_data:
        messagebox.showerror("Error", "Priložte ISIC alebo zadajte ISIC ID!")
        return

    popup = tk.Toplevel(app)
    popup.title(info_type)
    popup.geometry("400x300")

    if info_type == "Meno a priezvisko":
        message = f"Meno: {user_data['meno']}\nPriezvisko: {user_data['priezvisko']}"
    elif info_type == "Číslo izby":
        message = f"Číslo izby: {user_data['cislo_izby']}"
    elif info_type == "Zariadenia":
        message = (
            f"Bezdrôtové pripojenie MAC: {user_data['bezdr_pripojenie_mac']}\n"
            f"Bezdrôtové pripojenie IP: {user_data['bezdr_pripojenie_ip']}\n"
            f"Pevné pripojenie IP: {user_data['pevne_pripojenie_ip']}\n"
            f"Pevné pripojenie MAC: {user_data['pevne_pripojenie_mac']}"
        )
   

    label = tk.Label(popup, text=message, font=("Arial", 14))
    label.pack(pady=20)

    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)

def manual_input():
    isic_id = manual_entry.get().strip()
    if isic_id:
        handle_isic(isic_id)
    else:
        messagebox.showerror("Error", "Isic sa nenasiel!")


app = tk.Tk()
app.title("Vala-Informacie")
app.geometry("600x400")
app.configure(bg="#F5DEB3")


image = Image.open("C:/Users/majov/Desktop/vala.png")
image = image.resize((130, 130))
img = ImageTk.PhotoImage(image)


button1 = tk.Button(app, text="Meno a priezvisko", command=lambda: show_user_info("Meno a priezvisko"), padx=50, pady=10, bg="#F5DEB3")
button1.pack(pady=10)

button2 = tk.Button(app, text="Číslo izby", command=lambda: show_user_info("Číslo izby"), padx=50, pady=10, bg="#F5DEB3")
button2.pack(pady=10)

button3 = tk.Button(app, text="Zariadenia", command=lambda: show_user_info("Zariadenia"), padx=50, pady=10, bg="#F5DEB3")
button3.pack(pady=10)


manual_label = tk.Label(app, text="Manuálne zadanie ISIC ID:", bg="#F5DEB3")
manual_label.pack(pady=5)

manual_entry = tk.Entry(app, width=30)
manual_entry.pack(pady=5)

manual_button = tk.Button(app, text="Odoslať", command=manual_input, padx=50, pady=10, bg="#F5DEB3")
manual_button.pack(pady=10)


img_label_main = tk.Label(app, image=img, bg="#F5DEB3")
img_label_main.place(relx=1.0, rely=1.0, anchor="se")  


reader_thread = threading.Thread(target=read_from_reader, daemon=True)
reader_thread.start()

app.mainloop()
