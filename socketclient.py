#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import websockets
import tkinter as tk
from threading import Thread
from tkinter import ttk

class WebSocketClient:
    def __init__(self, master):
        self.master = master
        master.title("CMPE 280 Assignment - Web Sockets and GPT Models")

        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 14), background='#d0e0f0')
        self.style.configure('TButton', font=('Arial', 12), relief=tk.FLAT)
        self.style.configure('TFrame', background='#d0e0f0')
        self.style.configure('TText', font=('Arial', 12), padding=5, background='#d0e0f0', borderwidth=2, relief="solid")

        self.master.configure(background='#d0e0f0')

        self.label = ttk.Label(master, text="CMPE 280 - WebSocket Client Interface")
        self.label.pack(pady=10)

        self.start_button = ttk.Button(master, text="Start", command=self.start, style='TButton')
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(master, text="Stop", command=self.stop, state=tk.DISABLED, style='TButton')
        self.stop_button.pack(pady=5)

        self.log_frame = ttk.Frame(master)
        self.log_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.log_label = ttk.Label(self.log_frame, text="Response Logs")
        self.log_label.pack(pady=(0, 5))

        self.log = tk.Text(self.log_frame, height=10, width=50, state=tk.DISABLED, wrap=tk.WORD)
        self.log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.log_frame, command=self.log.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log['yscrollcommand'] = self.scrollbar.set

        self.running = False

    def start(self):
        self.running = True
        self.start_button['state'] = tk.DISABLED
        self.stop_button['state'] = tk.NORMAL
        self.thread = Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
        self.start_button['state'] = tk.NORMAL
        self.stop_button['state'] = tk.DISABLED

    async def hello(self):
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            for i in range(1, 10001):
                if not self.running:
                    break
                await websocket.send("Request [" + str(i) + "] Hello world!")
                message = await websocket.recv()
                self.log['state'] = tk.NORMAL
                self.log.insert(tk.END, f"Received: {message}\n")
                self.log.yview(tk.END)
                self.log['state'] = tk.DISABLED

    def run(self):
        asyncio.run(self.hello())

root = tk.Tk()
client = WebSocketClient(root)
root.mainloop()

