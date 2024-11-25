from dataclasses import dataclass
from typing import List, Optional, Tuple
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class DESModes:
    def __init__(self, des_instance, block_size: int = 64):
        self.des = des_instance
        self.block_size = block_size
        self.bytes_in_block = block_size // 8

    def generate_iv(self) -> bytes:
        """Generate random initialization vector"""
        return os.urandom(self.bytes_in_block)

    def pad_data(self, data: bytes) -> bytes:
        """PKCS7 padding"""
        pad_len = self.bytes_in_block - (len(data) % self.bytes_in_block)
        return data + bytes([pad_len] * pad_len)

    def unpad_data(self, data: bytes) -> bytes:
        """Remove PKCS7 padding"""
        pad_len = data[-1]
        return data[:-pad_len]

    def cbc_encrypt(self, data: bytes, key: bytes, iv: bytes) -> bytes:
        """CBC mode encryption"""
        padded_data = self.pad_data(data)
        blocks = []
        prev_block = iv

        # Process each block
        for i in range(0, len(padded_data), self.bytes_in_block):
            current_block = padded_data[i:i + self.bytes_in_block]
            # XOR with previous ciphertext block
            xored = bytes(a ^ b for a, b in zip(current_block, prev_block))
            # Encrypt
            encrypted_block = self.des.encrypt_block(xored, key)
            blocks.append(encrypted_block)
            prev_block = encrypted_block

        return b''.join(blocks)

    def cbc_decrypt(self, data: bytes, key: bytes, iv: bytes) -> bytes:
        """CBC mode decryption"""
        blocks = []
        prev_block = iv

        # Process each block
        for i in range(0, len(data), self.bytes_in_block):
            current_block = data[i:i + self.bytes_in_block]
            # Decrypt
            decrypted_block = self.des.decrypt_block(current_block, key)
            # XOR with previous ciphertext block
            xored = bytes(a ^ b for a, b in zip(decrypted_block, prev_block))
            blocks.append(xored)
            prev_block = current_block

        decrypted_data = b''.join(blocks)
        return self.unpad_data(decrypted_data)

    def triple_des_encrypt(self, data: bytes, key1: bytes, key2: bytes, key3: bytes, iv: bytes) -> bytes:
        """Triple DES encryption with three keys in CBC mode"""
        padded_data = self.pad_data(data)
        blocks = []
        prev_block = iv

        for i in range(0, len(padded_data), self.bytes_in_block):
            current_block = padded_data[i:i + self.bytes_in_block]
            # XOR with previous block
            xored = bytes(a ^ b for a, b in zip(current_block, prev_block))
            # Triple encryption
            cipher1 = self.des.encrypt_block(xored, key1)
            cipher2 = self.des.encrypt_block(cipher1, key2)
            cipher3 = self.des.encrypt_block(cipher2, key3)
            blocks.append(cipher3)
            prev_block = cipher3

        return b''.join(blocks)

    def triple_des_decrypt(self, data: bytes, key1: bytes, key2: bytes, key3: bytes, iv: bytes) -> bytes:
        """Triple DES decryption with three keys in CBC mode"""
        blocks = []
        prev_block = iv

        for i in range(0, len(data), self.bytes_in_block):
            current_block = data[i:i + self.bytes_in_block]
            # Triple decryption
            plain1 = self.des.decrypt_block(current_block, key3)
            plain2 = self.des.decrypt_block(plain1, key2)
            plain3 = self.des.decrypt_block(plain2, key1)
            # XOR with previous block
            xored = bytes(a ^ b for a, b in zip(plain3, prev_block))
            blocks.append(xored)
            prev_block = current_block

        decrypted_data = b''.join(blocks)
        return self.unpad_data(decrypted_data)

    def analyze_avalanche(self, data: bytes, key: bytes, iv: bytes,
                          mode: str = 'CBC') -> List[List[int]]:
        """Analyze avalanche effect"""
        original = bytearray(data)
        changes = []

        # Test each bit position
        for byte_pos in range(len(data)):
            for bit_pos in range(8):
                # Flip bit
                test_data = bytearray(original)
                test_data[byte_pos] ^= (1 << bit_pos)

                original_cipher = self.cbc_encrypt(bytes(original), key, iv)
                modified_cipher = self.cbc_encrypt(bytes(test_data), key, iv)

                # Compare bits between original and modified ciphertext
                block_changes = []
                for i in range(0, len(original_cipher), self.bytes_in_block):
                    block_orig = original_cipher[i:i + self.bytes_in_block]
                    block_mod = modified_cipher[i:i + self.bytes_in_block]

                    diff = 0
                    for bo, bm in zip(block_orig, block_mod):
                        diff += bin(bo ^ bm).count('1')
                    block_changes.append(diff)

                changes.append(block_changes)

        return changes


class CryptoGUI:
    def __init__(self, des_modes):
        self.des_modes = des_modes
        self.window = tk.Tk()
        self.window.title("DES CBC Mode & Triple DES")
        self.setup_gui()

    def setup_gui(self):
        # Input frame
        input_frame = ttk.LabelFrame(self.window, text="Input")
        input_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        ttk.Button(input_frame, text="Load Plaintext", command=self.load_plaintext).grid(row=0, column=0, padx=5,
                                                                                         pady=5)
        ttk.Button(input_frame, text="Load Key", command=self.load_key).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(input_frame, text="Load IV", command=self.load_iv).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(input_frame, text="Generate IV", command=self.generate_iv).grid(row=0, column=3, padx=5, pady=5)

        # Text displays
        self.plaintext_hex = tk.Text(input_frame, height=5, width=50)
        self.plaintext_hex.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.plaintext_ascii = tk.Text(input_frame, height=5, width=50)
        self.plaintext_ascii.grid(row=1, column=2, columnspan=2, padx=5, pady=5)

        self.key_hex = tk.Text(input_frame, height=2, width=50)
        self.key_hex.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.iv_hex = tk.Text(input_frame, height=2, width=50)
        self.iv_hex.grid(row=2, column=2, columnspan=2, padx=5, pady=5)

        # Operation buttons
        ttk.Button(input_frame, text="CBC Encrypt", command=self.cbc_encrypt).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(input_frame, text="CBC Decrypt", command=self.cbc_decrypt).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(input_frame, text="Triple DES Encrypt", command=self.triple_des_encrypt).grid(row=3, column=2,
                                                                                                 padx=5, pady=5)
        ttk.Button(input_frame, text="Triple DES Decrypt", command=self.triple_des_decrypt).grid(row=3, column=3,
                                                                                                 padx=5, pady=5)

        # Output frame
        output_frame = ttk.LabelFrame(self.window, text="Output")
        output_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.output_hex = tk.Text(output_frame, height=5, width=50)
        self.output_hex.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.output_ascii = tk.Text(output_frame, height=5, width=50)
        self.output_ascii.grid(row=0, column=2, columnspan=2, padx=5, pady=5)

        # Avalanche analysis buttons
        ttk.Button(output_frame, text="Analyze Avalanche Effect", command=self.analyze_avalanche).grid(row=1, column=0,
                                                                                                       columnspan=4,
                                                                                                       padx=5, pady=5)

    def bytes_to_hex(self, data: bytes) -> str:
        return ' '.join(f'{b:02x}' for b in data)

    def hex_to_bytes(self, hex_str: str) -> bytes:
        hex_str = ''.join(hex_str.split())
        return bytes.fromhex(hex_str)

    def load_plaintext(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, 'rb') as f:
                data = f.read()
            self.plaintext_hex.delete('1.0', tk.END)
            self.plaintext_hex.insert('1.0', self.bytes_to_hex(data))
            self.plaintext_ascii.delete('1.0', tk.END)
            self.plaintext_ascii.insert('1.0', data.decode('latin-1'))

    def load_key(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, 'rb') as f:
                data = f.read()
            self.key_hex.delete('1.0', tk.END)
            self.key_hex.insert('1.0', self.bytes_to_hex(data))

    def load_iv(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, 'rb') as f:
                data = f.read()
            self.iv_hex.delete('1.0', tk.END)
            self.iv_hex.insert('1.0', self.bytes_to_hex(data))

    def generate_iv(self):
        iv = self.des_modes.generate_iv()
        self.iv_hex.delete('1.0', tk.END)
        self.iv_hex.insert('1.0', self.bytes_to_hex(iv))

    def cbc_encrypt(self):
        try:
            plaintext = self.hex_to_bytes(self.plaintext_hex.get('1.0', tk.END))
            key = self.hex_to_bytes(self.key_hex.get('1.0', tk.END))
            iv = self.hex_to_bytes(self.iv_hex.get('1.0', tk.END))

            ciphertext = self.des_modes.cbc_encrypt(plaintext, key, iv)

            self.output_hex.delete('1.0', tk.END)
            self.output_hex.insert('1.0', self.bytes_to_hex(ciphertext))
            self.output_ascii.delete('1.0', tk.END)
            self.output_ascii.insert('1.0', ciphertext.decode('latin-1'))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cbc_decrypt(self):
        try:
            ciphertext = self.hex_to_bytes(self.plaintext_hex.get('1.0', tk.END))
            key = self.hex_to_bytes(self.key_hex.get('1.0', tk.END))
            iv = self.hex_to_bytes(self.iv_hex.get('1.0', tk.END))

            plaintext = self.des_modes.cbc_decrypt(ciphertext, key, iv)

            self.output_hex.delete('1.0', tk.END)
            self.output_hex.insert('1.0', self.bytes_to_hex(plaintext))
            self.output_ascii.delete('1.0', tk.END)
            self.output_ascii.insert('1.0', plaintext.decode('latin-1'))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def analyze_avalanche(self):
        try:
            plaintext = self.hex_to_bytes(self.plaintext_hex.get('1.0', tk.END))
            key = self.hex_to_bytes(self.key_hex.get('1.0', tk.END))
            iv = self.hex_to_bytes(self.iv_hex.get('1.0', tk.END))

            changes = self.des_modes.analyze_avalanche(plaintext, key, iv)

            # Create a new window for the plot
            plot_window = tk.Toplevel(self.window)
            plot_window.title("Avalanche Effect Analysis")

            fig = Figure(figsize=(10, 6))
            ax = fig.add_subplot(111)

            # Plot changes for each block
            x = range(len(changes))
            for block_idx in range(len(changes[0])):
                block_changes = [change[block_idx] for change in changes]
                ax.plot(x, block_changes, label=f'Block {block_idx + 1}')

            ax.set_xlabel('Bit Position')
            ax.set_ylabel('Number of Changed Bits')
            ax.set_title('Avalanche Effect Analysis')
            ax.legend()

            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.draw()
            canvas.get_tk_widget().pack()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    des_modes = DESModes(des)
    gui = CryptoGUI(des_modes)
    gui.run()