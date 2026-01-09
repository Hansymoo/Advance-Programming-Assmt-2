import tkinter as tk
from tkinter import ttk, messagebox
import requests


class CurrencyConverter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.freecurrencyapi.com/v1/latest"

    def get_exchange_rate(self, base_currency, target_currency):
        params = {
            "apikey": self.api_key,
            "base_currency": base_currency
        }

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()

        return data["data"][target_currency]

    def convert(self, amount, base_currency, target_currency):
        if base_currency == target_currency:
            return amount

        rate = self.get_exchange_rate(base_currency, target_currency)
        return amount * rate


class CurrencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.api_key = "fca_live_t45NKIuWI7ZNIiKqDIAyzFRcwlurFr1syLSyb5Cj"
        self.converter = CurrencyConverter(self.api_key)

        self.currencies = [
            "USD", "EUR", "GBP", "JPY", "AUD",
            "CAD", "CHF", "CNY", "NZD"
        ]

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Currency Converter",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        amount_label = tk.Label(self.root, text="Amount:")
        amount_label.pack()

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack(pady=5)

        currency_frame = tk.Frame(self.root)
        currency_frame.pack(pady=10)

        self.base_currency = ttk.Combobox(
            currency_frame,
            values=self.currencies,
            state="readonly"
        )
        self.base_currency.set("USD")
        self.base_currency.grid(row=0, column=0, padx=5)

        self.target_currency = ttk.Combobox(
            currency_frame,
            values=self.currencies,
            state="readonly"
        )
        self.target_currency.set("EUR")
        self.target_currency.grid(row=0, column=1, padx=5)

        convert_button = tk.Button(
            self.root,
            text="Convert",
            command=self.convert_currency
        )
        convert_button.pack(pady=10)

        self.result_label = tk.Label(
            self.root,
            text="Converted Amount:",
            font=("Arial", 12)
        )
        self.result_label.pack(pady=10)

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            base = self.base_currency.get()
            target = self.target_currency.get()

            result = self.converter.convert(amount, base, target)

            self.result_label.config(
                text=f"{amount:.2f} {base} = {result:.2f} {target}"
            )

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
        except requests.exceptions.RequestException:
            messagebox.showerror(
                "API Error",
                "Failed to retrieve exchange rates.\nCheck your internet connection or API key."
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyApp(root)
    root.mainloop()
