"""
Pruebas E2E básicas con Selenium para verificar que la homepage carga.

Requisitos locales (una vez):
  pip install selenium webdriver-manager

Notas:
- Debes tener Google Chrome instalado.
- Asegúrate de que el servidor esté corriendo en http://127.0.0.1:8000
  (puedes iniciarlo con: python proyecto\\src\\backend\\manage.py runserver 127.0.0.1:8000)
"""

import os
import unittest
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


KEEP_BROWSER_OPEN = False
CLOSE_DELAY_SECONDS = 5

class TestHomepageE2E(unittest.TestCase):
    """Verifica carga de la página principal y título no vacío."""

    driver: Optional[webdriver.Chrome] = None
    base_url: str = os.getenv("STUDENTPOINT_BASE_URL", "http://127.0.0.1:8000")

    @classmethod
    def setUpClass(cls) -> None:
        chrome_options = ChromeOptions()
        # chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        chrome_options.add_experimental_option("useAutomationExtension", False)
        service = ChromeService(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.set_window_size(1366, 900)

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.driver is None:
            return
        if KEEP_BROWSER_OPEN:
            print("[E2E] KEEP_BROWSER_OPEN=True: Dejando el navegador abierto.")
            return
        if CLOSE_DELAY_SECONDS > 0:
            print(f"[E2E] Esperando {CLOSE_DELAY_SECONDS}s antes de cerrar el navegador...")
            time.sleep(CLOSE_DELAY_SECONDS)
        cls.driver.quit()

    def test_homepage_load(self) -> None:
        assert self.driver is not None

        self.driver.get(self.base_url)

        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        page_title = (self.driver.title or "").strip()
        self.assertGreaterEqual(len(page_title), 1)


