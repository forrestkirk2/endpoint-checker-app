import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
from bs4 import BeautifulSoup

def fetch_data():
    url = url_entry.get()
    output_area.delete('1.0', tk.END)

    try:
        response = requests.get(url)
        content_type = response.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            try:
                data = response.json()
                output_area.insert(tk.END, "✅ JSON detected.\n\n")
                if isinstance(data, dict):
                    for key, value in data.items():
                        output_area.insert(tk.END, f"{key}: {value}\n")
                elif isinstance(data, list):
                    for i, item in enumerate(data[:10], start=1):
                        output_area.insert(tk.END, f"{i}. {item}\n")
                else:
                    output_area.insert(tk.END, str(data))
            except json.JSONDecodeError:
                output_area.insert(tk.END, "⚠️ Invalid JSON format.")
        elif 'text/html' in content_type:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No title"
            metas = soup.find_all('meta')
            meta_info = [f"{meta.get('name', 'N/A')}={meta.get('content', 'N/A')}" for meta in metas if meta.get('name')]
            output_area.insert(tk.END, "🌐 HTML detected.\n\n")
            output_area.insert(tk.END, f"Title: {title}\n\nMeta Tags:\n" + "\n".join(meta_info[:10]))
        elif 'text/plain' in content_type:
            output_area.insert(tk.END, "📄 Plain text detected:\n\n" + response.text[:500])
        else:
            output_area.insert(tk.END, f"⚠️ Unrecognized content type: {content_type}")
    except requests.RequestException as e:
        messagebox.showerror("Request Error", str(e))

# GUI Setup
window = tk.Tk()
window.title("API Endpoint Tester")

frame = ttk.Frame(window, padding="10")
frame.grid(row=0, column=0)

ttk.Label(frame, text="Enter API Endpoint:").grid(row=0, column=0, sticky=tk.W)
url_entry = ttk.Entry(frame, width=60)
url_entry.grid(row=1, column=0)
url_entry.insert(0, "https://jsonplaceholder.typicode.com/todos/1")

ttk.Button(frame, text="Fetch & Analyze", command=fetch_data).grid(row=2, column=0, pady=10, sticky=tk.W)

output_area = scrolledtext.ScrolledText(frame, width=80, height=20)
output_area.grid(row=3, column=0)

window.mainloop()