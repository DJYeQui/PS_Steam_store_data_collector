import tkinter as tk
from tkinter import ttk, messagebox
import threading

# Mevcut modüllerinizi kullanmak için gerekli importlar
# Main.py dosyasındaki fonksiyonları direkt kullanmak yerine,
# dosya adını çıktı olarak alabilmek için kısmi işlevsellikleri buraya taşıyoruz.
import collect_game_data_from_link as collect
import steamDB as db
import game_link_list_collector as glc
import Main  # Bu dosyayı, eğer gerekiyorsa __name__ kontrolüyle düzenleyin

def collect_one_game_thread(link, filename):
    try:
        # Tek oyun için veri toplama
        game_data_list = []
        game_data = collect.collect_game_data_with_url(link)
        game_data["link"] = link
        game_data_list.append(game_data)
        game_final_data = db.collect_steamDB_selling_data(game_data_list)
        # Çıktıyı kullanıcı tarafından belirlenen dosyaya yazdırıyoruz
        Main.write_game_info_to_csv(game_final_data, filename=filename)
        messagebox.showinfo("Başarılı", f"Veriler '{filename}' dosyasına eklendi.")
    except Exception as e:
        messagebox.showerror("Hata", f"Tek oyun verisi toplanırken hata:\n{e}")

def collect_many_games_thread(filename):
    try:
        # Çoklu oyun için veri toplama
        link_list = glc.collect_link_from_steam_game_list("https://store.steampowered.com/charts/topselling/TR")
        game_data_list = []
        for name, link in link_list.items():
            game_data = collect.collect_game_data_with_url(link, name)
            game_data["link"] = link
            game_data_list.append(game_data)
        game_final_data = db.collect_steamDB_selling_data(game_data_list)
        Main.write_game_info_to_csv(game_final_data, filename=filename)
        messagebox.showinfo("Başarılı", f"Veriler '{filename}' dosyasına eklendi.")
    except Exception as e:
        messagebox.showerror("Hata", f"Çoklu oyun verisi toplanırken hata:\n{e}")

def start_collection():
    filename = filename_entry.get().strip()
    if not filename:
        messagebox.showerror("Hata", "Lütfen çıktı dosya ismini giriniz!")
        return

    collection_type = collection_var.get()
    if collection_type == "Tek Oyun":
        link = link_entry.get().strip()
        if not link:
            messagebox.showerror("Hata", "Lütfen oyun linkini giriniz!")
            return
        # Arayüzün donmasını önlemek için işlemi ayrı bir thread'de çalıştırıyoruz.
        threading.Thread(target=collect_one_game_thread, args=(link, filename), daemon=True).start()
    elif collection_type == "Birçok Oyun":
        threading.Thread(target=collect_many_games_thread, args=(filename,), daemon=True).start()
    else:
        messagebox.showerror("Hata", "Geçersiz seçim!")

def toggle_link_entry():
    # "Tek Oyun" seçildiğinde link alanı aktif, "Birçok Oyun" seçildiğinde pasif olsun.
    if collection_var.get() == "Tek Oyun":
        link_entry.config(state="normal")
    else:
        link_entry.config(state="disabled")

# Tkinter arayüzünü hazırlıyoruz.
root = tk.Tk()
root.title("Steam Oyun Verisi Toplayıcı")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Toplama Türü seçim alanı
collection_var = tk.StringVar(value="Tek Oyun")
ttk.Label(frame, text="Toplama Türü:").grid(row=0, column=0, sticky=tk.W, pady=5)
radio_one = ttk.Radiobutton(frame, text="Tek Oyun", variable=collection_var, value="Tek Oyun", command=toggle_link_entry)
radio_one.grid(row=0, column=1, sticky=tk.W)
radio_many = ttk.Radiobutton(frame, text="Birçok Oyun", variable=collection_var, value="Birçok Oyun", command=toggle_link_entry)
radio_many.grid(row=0, column=2, sticky=tk.W)

# Oyun Linki girişi (sadece "Tek Oyun" seçeneği için)
ttk.Label(frame, text="Oyun Linki:").grid(row=1, column=0, sticky=tk.W, pady=5)
link_entry = ttk.Entry(frame, width=60)
link_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E))

# Çıktı Dosya İsmi girişi
ttk.Label(frame, text="Çıktı Dosya İsmi:").grid(row=2, column=0, sticky=tk.W, pady=5)
filename_entry = ttk.Entry(frame, width=60)
filename_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E))

# Başlat butonu
start_button = ttk.Button(frame, text="Başlat", command=start_collection)
start_button.grid(row=3, column=0, columnspan=3, pady=10)

toggle_link_entry()  # İlk durumda doğru alanın aktif olup olmadığını ayarla.

root.mainloop()
