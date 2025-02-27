from pyzbar.pyzbar import decode
from PIL import Image
import pyqrcode
import os
import asyncio
import threading
import aiohttp
import time
from dotenv import load_dotenv

load_dotenv()

output_widget = None
api_key = os.getenv('ALPHAVANTAGE_API_KEY')
symbols = ["A", "AA", "AAA", "AAAU", "AACBU", "AACG", "AACT", "AACT-U", "AACT-WS", "AADI", "AADR", "AAL", "AAM", "AAM-U", "AAM-WS", "AAME", "AAMI", "AAOI", "AAON", "AAP", "AAPB", "AAPD", "AAPG", "AAPGV", "AAPL", "AAPR", "AAPU", "AAPW", "AAPX", "AAPY", "AARD", "AAT", "AAVM", "AAXJ", "AB", "ABAT", "ABBV", "ABCB", "ABCL", "ABCS", "ABEO", "ABEQ", "ABEV", "ABFL", "ABG", "ABHY", "ABL", "ABLD", "ABLG", "ABLLL", "ACLS", ]
results = []

def set_output_widget(widget):
    global output_widget
    output_widget = widget

def write_output(text):
    if output_widget:
        output_widget.insert('end', text + "\n")
        output_widget.see("end")
    else:
        print(text)

def clear():
    if output_widget:
        output_widget.delete("1.0", "end")

def create():
    """Generate multiple QR codes, one per symbol."""
    for symbol in symbols:
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'
        qr = pyqrcode.create(url)
        qr.png(f'qr_{symbol}.png', scale=6)
        write_output(f"QR created for symbol: {symbol}")

def delete():
    """Delete all QR code images."""
    root = '.'
    deleted_files = 0
    for filename in os.listdir(root):
        if filename.startswith("qr_") and filename.endswith('.png'):
            os.remove(os.path.join(root, filename))
            deleted_files += 1
    write_output(f'Deleted {deleted_files} QR Code files')

def scan():
    """Start scanning process in a separate thread."""
    threading.Thread(target=run_async_scan, daemon=True).start()

def run_async_scan():
    asyncio.run(get_symbols())

async def get_symbols():
    start_time = time.time()  # Start time tracking

    async with aiohttp.ClientSession() as session:
        tasks = []
        for symbol in symbols:
            decoded_url = decode_qr(f"qr_{symbol}.png")
            if decoded_url:
                tasks.append(asyncio.create_task(fetch_data(session, decoded_url, symbol)))

        if tasks:
            await asyncio.gather(*tasks)

    end_time = time.time()  # End time tracking
    elapsed_time = end_time - start_time
    write_output(f"Scan completed in {elapsed_time:.2f} seconds")

def decode_qr(filename):
    """Decode the URL from a QR code image."""
    try:
        decoded_data = decode(Image.open(filename))
        if decoded_data:
            return decoded_data[0].data.decode('utf-8')
        else:
            write_output(f"QR Code not found in {filename}")
            return None
    except Exception as e:
        write_output(f"Error decoding {filename}: {e}")
        return None

async def fetch_data(session, url, symbol):
    """Fetch API data for a given symbol."""
    try:
        async with session.get(url, ssl=False) as response:
            data = await response.json()
            results.append(data)
            write_output(f"Fetched data for {symbol}")
    except Exception as e:
        write_output(f"Error fetching {symbol}: {e}")
