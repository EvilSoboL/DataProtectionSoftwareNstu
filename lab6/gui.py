import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
from crypto_app import CombinedEncryption, hex_view


class CryptoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №6")
        self.crypto = CombinedEncryption()

        # Создаем notebook для вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        # Создаем вкладки
        self.encrypt_frame = ttk.Frame(self.notebook)
        self.decrypt_frame = ttk.Frame(self.notebook)
        self.view_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.encrypt_frame, text="Шифрование")
        self.notebook.add(self.decrypt_frame, text="Дешифрование")
        self.notebook.add(self.view_frame, text="Просмотр")

        self._setup_encrypt_tab()
        self._setup_decrypt_tab()
        self._setup_view_tab()

    def _setup_encrypt_tab(self):
        # Фрейм для генерации ключей
        key_frame = ttk.LabelFrame(self.encrypt_frame, text="Управление ключами")
        key_frame.pack(padx=5, pady=5, fill="x")

        ttk.Button(key_frame, text="Сгенерировать ключи",
                   command=self._generate_keys).pack(pady=5)

        # Фрейм для шифрования
        encrypt_frame = ttk.LabelFrame(self.encrypt_frame, text="Шифрование файла")
        encrypt_frame.pack(padx=5, pady=5, fill="x")

        ttk.Button(encrypt_frame, text="Выбрать файл для шифрования",
                   command=self._select_file_to_encrypt).pack(pady=5)

        self.encrypt_status = ttk.Label(encrypt_frame, text="")
        self.encrypt_status.pack(pady=5)

    def _setup_decrypt_tab(self):
        decrypt_frame = ttk.LabelFrame(self.decrypt_frame, text="Дешифрование файла")
        decrypt_frame.pack(padx=5, pady=5, fill="x")

        ttk.Button(decrypt_frame, text="Выбрать файлы для дешифрования",
                   command=self._select_files_to_decrypt).pack(pady=5)

        self.decrypt_status = ttk.Label(decrypt_frame, text="")
        self.decrypt_status.pack(pady=5)

    def _setup_view_tab(self):
        # Фрейм выбора файла
        file_frame = ttk.Frame(self.view_frame)
        file_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(file_frame, text="Выбрать файл для просмотра",
                   command=self._select_file_to_view).pack(side="left", padx=5)

        # Фрейм для отображения содержимого
        content_frame = ttk.Frame(self.view_frame)
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Текстовые поля для hex и текстового представления
        hex_frame = ttk.LabelFrame(content_frame, text="Шестнадцатеричное представление")
        hex_frame.pack(fill="both", expand=True, pady=5)

        self.hex_text = scrolledtext.ScrolledText(hex_frame, height=10)
        self.hex_text.pack(fill="both", expand=True, padx=5, pady=5)

        text_frame = ttk.LabelFrame(content_frame, text="Символьное представление")
        text_frame.pack(fill="both", expand=True, pady=5)

        self.text_view = scrolledtext.ScrolledText(text_frame, height=10)
        self.text_view.pack(fill="both", expand=True, padx=5, pady=5)

    def _generate_keys(self):
        try:
            public_key_file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                title="Сохранить открытый ключ",
                filetypes=[("Text files", "*.txt")]
            )
            if not public_key_file:
                return

            private_key_file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                title="Сохранить закрытый ключ",
                filetypes=[("Text files", "*.txt")]
            )
            if not private_key_file:
                return

            self.crypto.save_keys(public_key_file, private_key_file)
            messagebox.showinfo("Успех", "Ключи успешно сгенерированы и сохранены")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при генерации ключей: {str(e)}")

    def _select_file_to_encrypt(self):
        try:
            input_file = filedialog.askopenfilename(
                title="Выберите файл для шифрования"
            )
            if not input_file:
                return

            encrypted_file = filedialog.asksaveasfilename(
                defaultextension=".bin",
                title="Сохранить зашифрованный файл",
                filetypes=[("Binary files", "*.bin")]
            )
            if not encrypted_file:
                return

            encrypted_key_file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                title="Сохранить зашифрованный ключ",
                filetypes=[("Text files", "*.txt")]
            )
            if not encrypted_key_file:
                return

            self.crypto.encrypt_file(input_file, encrypted_file, encrypted_key_file)
            self.encrypt_status.config(
                text=f"Файл успешно зашифрован\nРезультат: {encrypted_file}"
            )

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при шифровании: {str(e)}")

    def _select_files_to_decrypt(self):
        try:
            encrypted_file = filedialog.askopenfilename(
                title="Выберите зашифрованный файл",
                filetypes=[("Binary files", "*.bin")]
            )
            if not encrypted_file:
                return

            encrypted_key_file = filedialog.askopenfilename(
                title="Выберите файл с зашифрованным ключом",
                filetypes=[("Text files", "*.txt")]
            )
            if not encrypted_key_file:
                return

            decrypted_file = filedialog.asksaveasfilename(
                title="Сохранить расшифрованный файл"
            )
            if not decrypted_file:
                return

            self.crypto.decrypt_file(encrypted_file, decrypted_file, encrypted_key_file)
            self.decrypt_status.config(
                text=f"Файл успешно расшифрован\nРезультат: {decrypted_file}"
            )

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при дешифровании: {str(e)}")

    def _select_file_to_view(self):
        file_path = filedialog.askopenfilename(
            title="Выберите файл для просмотра"
        )
        if not file_path:
            return

        try:
            hex_content, text_content = hex_view(file_path)

            self.hex_text.delete(1.0, tk.END)
            self.hex_text.insert(tk.END, hex_content)

            self.text_view.delete(1.0, tk.END)
            self.text_view.insert(tk.END, text_content)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при чтении файла: {str(e)}")


def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = CryptoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
