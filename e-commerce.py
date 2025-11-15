import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import requests
from bs4 import BeautifulSoup
import csv

def scrape_data():
    url = url_entry.get().strip()

    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0"
        })
        soup = BeautifulSoup(response.text, "html.parser")

        products = []

        items = soup.select(".product_pod")
        
        for item in items:
            name = item.h3.a["title"]
            price = item.select_one(".price_color").text
            rating = item.p["class"][1] 

            products.append([name, price, rating])

        if not products:
            messagebox.showerror("No Data", "Could not extract product information!")
            return

        
        for row in tree.get_children():
            tree.delete(row)

       
        for product in products:
            tree.insert("", tk.END, values=product)

        save_button.config(state="normal")

        global scraped_data
        scraped_data = products
        messagebox.showinfo("Success", "Scraping Completed!")

    except Exception as e:
        messagebox.showerror("Error", f"An issue occurred:\n{e}")


def save_csv():
    if not scraped_data:
        messagebox.showerror("Error", "No data to save!")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return

    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Product Name", "Price", "Rating"])
            writer.writerows(scraped_data)

        messagebox.showinfo("Saved", "CSV file saved successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file:\n{e}")




root = tk.Tk()
root.title("E-commerce Product Scraper")
root.geometry("700x500")
root.configure(bg="#f5f5f5")

scraped_data = []

title_label = tk.Label(root, text="E-commerce Product Scraper", font=("Arial", 18, "bold"), bg="#f5f5f5")
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#f5f5f5")
frame.pack(pady=10)

url_label = tk.Label(frame, text="Enter Product Page URL:", font=("Arial", 12), bg="#f5f5f5")
url_label.grid(row=0, column=0, padx=5)

url_entry = tk.Entry(frame, width=50, font=("Arial", 12))
url_entry.grid(row=0, column=1, padx=5)

scrape_button = tk.Button(frame, text="Scrape Data", command=scrape_data, font=("Arial", 12), bg="#4caf50", fg="white")
scrape_button.grid(row=0, column=2, padx=5)

columns = ("Name", "Price", "Rating")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)

tree.pack(pady=10)

save_button = tk.Button(root, text="Save as CSV", state="disabled", command=save_csv, font=("Arial", 12), bg="#2196f3", fg="white")
save_button.pack(pady=10)

root.mainloop()
