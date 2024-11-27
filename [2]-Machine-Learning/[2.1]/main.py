import tkinter as tk
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# Veri listeleri
data_points = []  # [(x, y, class), ...]
current_class = 0  # Mevcut sınıf

# Tkinter arayüzü
window = tk.Tk()
window.title("Makine Öğrenmesi Gözlem Aracı")
window.geometry("600x600")

# Tuval oluştur
canvas = tk.Canvas(window, width=500, height=500, bg="white")
canvas.pack(pady=10)

# Sınıfı değiştiren düğme
def change_class():
    global current_class
    current_class = (current_class + 1) % 2  # Sınıfı 0 ve 1 arasında değiştir
    class_label.config(text=f"Mevcut Sınıf: {current_class}")

class_button = tk.Button(window, text="Sınıfı Değiştir", command=change_class)
class_button.pack()

class_label = tk.Label(window, text=f"Mevcut Sınıf: {current_class}")
class_label.pack()

# Nokta ekleme
def add_point(event):
    global data_points
    x, y = event.x, event.y
    data_points.append((x, y, current_class))
    color = "red" if current_class == 0 else "blue"
    canvas.create_oval(x-3, y-3, x+3, y+3, fill=color, outline=color)

canvas.bind("<Button-1>", add_point)

# Model eğitimi
def train_model():
    global knn_model
    if len(data_points) < 2:
        result_label.config(text="Eğitim için yeterli veri yok!")
        return
    
    # Verileri ayrıştır
    X = np.array([[p[0], p[1]] for p in data_points])
    y = np.array([p[2] for p in data_points])
    
    # KNN modelini eğit
    knn_model = KNeighborsClassifier(n_neighbors=3)
    knn_model.fit(X, y)
    result_label.config(text="Model Eğitildi!")

train_button = tk.Button(window, text="Modeli Eğit", command=train_model)
train_button.pack()

# Nokta sınıflandırma
def classify_point(event):
    if 'knn_model' not in globals():
        result_label.config(text="Önce modeli eğit!")
        return
    
    x, y = event.x, event.y
    prediction = knn_model.predict([[x, y]])[0]
    color = "red" if prediction == 0 else "blue"
    canvas.create_oval(x-3, y-3, x+3, y+3, fill=color, outline="black")
    result_label.config(text=f"Yeni nokta {prediction} sınıfında!")

canvas.bind("<Button-3>", classify_point)

# Sonuç etiketi
result_label = tk.Label(window, text="")
result_label.pack()

# Arayüzü çalıştır
window.mainloop()
