import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# URL de resultados de Google Noticias (pagina 2)
SEARCH_URL = "https://www.google.com/search?q=noticias+politica+ecuador&sca_esv=d57f7703fbd643cb&tbs=qdr:d,sbd:1&tbm=nws&start=10"


def iniciar_driver():
    """Configura el navegador Chrome en modo headless y devuelve el driver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def extraer_enlaces(driver, url):
    """Visita la pagina de resultados y devuelve una lista de URLs de noticias."""
    driver.get(url)
    time.sleep(2)  # Espera que cargue la pagina
    soup = BeautifulSoup(driver.page_source, "html.parser")
    enlaces = []
    for a in soup.select('a[href]'):
        href = a.get('href')
        if href and href.startswith('http') and not href.startswith('https://webcache.googleusercontent.com'):
            enlaces.append(href)
    return list(dict.fromkeys(enlaces))


def extraer_contenido(driver, url):
    """Abre cada enlace de noticia y extrae su titulo h1 y parrafos."""
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    titulo_tag = soup.find('h1')
    titulo = titulo_tag.get_text(strip=True) if titulo_tag else ''

    parrafos = [p.get_text(strip=True) for p in soup.find_all('p')]
    contenido = '\n'.join(parrafos)
    return titulo, contenido


def guardar_csv(filas, archivo="noticias.csv"):
    """Guarda los resultados en un archivo CSV."""
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['url', 'titulo', 'contenido'])
        writer.writerows(filas)


def main():
    driver = iniciar_driver()
    try:
        enlaces = extraer_enlaces(driver, SEARCH_URL)
        datos = []
        for enlace in enlaces:
            try:
                titulo, contenido = extraer_contenido(driver, enlace)
                datos.append([enlace, titulo, contenido])
            except Exception as e:
                print(f"Error al procesar {enlace}: {e}")
        guardar_csv(datos)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
