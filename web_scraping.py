import requests
from bs4 import BeautifulSoup
import os
import zipfile
import tempfile

# URL da página
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
}

# Cria uma pasta temporária para armazenar os PDFs
with tempfile.TemporaryDirectory() as output_folder:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        pdf_links = [a['href'] for a in soup.find_all('a', href=True) if "Anexo" in a.text]

        downloaded_files = []
        for link in pdf_links:
            pdf_url = link if link.startswith("http") else f"https://www.gov.br{link}"
            pdf_name = os.path.join(output_folder, pdf_url.split("/")[-1])

            pdf_response = requests.get(pdf_url, headers=headers)
            if pdf_response.status_code == 200:
                with open(pdf_name, "wb") as f:
                    f.write(pdf_response.content)
                downloaded_files.append(pdf_name)
                print(f"Baixado: {pdf_name}")
            else:
                print(f"Erro ao baixar {pdf_url} (status code: {pdf_response.status_code})")

        if downloaded_files:
            zip_filename = "anexos.zip"
            with zipfile.ZipFile(zip_filename, "w") as zipf:
                for file in downloaded_files:
                    zipf.write(file, os.path.basename(file))
            print(f"Arquivos compactados em {zip_filename}")
        else:
            print("Nenhum arquivo PDF foi baixado.")
    else:
        print("Erro ao acessar a página. Status code:", response.status_code)
