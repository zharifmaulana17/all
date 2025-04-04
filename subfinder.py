import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if not os.path.exists("Results"):
    os.makedirs("Results")

def find_subdomains(domain, api_key):
    """
    Mencari subdomain untuk domain tertentu menggunakan API.
    """
    url = f"https://v1.eclipsesec.tech/api?subdomain={domain}&apikey={api_key}"
    try:
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return domain, data
        else:
            print(f"--> {domain} [ ERROR ]")
            return domain, None
    except requests.RequestException as e:
        print(f"--> {domain} [ REQUESTS FAILED ]")
        return domain, None

def extract_domains(json_data):
    """
    Mengekstrak daftar subdomain dari data JSON.
    """
    if json_data and 'domains' in json_data:
        return json_data['domains']
    else:
        return []

def read_domains_from_file(file_path):
    """
    Membaca daftar domain dari file.
    """
    with open(file_path, 'r') as file:
        domains = file.read().splitlines()
    return domains

def save_to_file(data, output_file):
    """
    Menyimpan hasil subdomain ke file.
    """
    with open(output_file, 'a') as file:
        for item in data:
            file.write(item + "\n")

input_file = input("Masukkan nama file input (contoh: list.txt): ").strip()
api_key = "@Batosay1337"

domains = read_domains_from_file(input_file)

subfinder_file = "Results/Subfinder.txt"
open(subfinder_file, 'w').close()  

def process_domain(domain):
    """
    Memproses setiap domain untuk mencari subdomain.
    """
    print(f"--> {domain} [ PROCESSING ]")

    domain, subdomain_data = find_subdomains(domain, api_key)
    if subdomain_data:
        subdomains = extract_domains(subdomain_data)
        print(f"--> {domain} [ {len(subdomains)} SUBDOMAINS FOUND ]")
        save_to_file(subdomains, subfinder_file)
    else:
        print(f"--> {domain} [ NO SUBDOMAINS FOUND ]")

with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(process_domain, domain) for domain in domains]

    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Error occurred: {e}")