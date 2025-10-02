"""Esqueletos de pruebas E2E para Registro con Selenium."""

import os
import unittest
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


KEEP_BROWSER_OPEN = False
CLOSE_DELAY_SECONDS = 5

class TestRegisterE2E(unittest.TestCase):
    """Casos de registro de usuarios (por implementar)."""

    driver: Optional[webdriver.Chrome] = None
    base_url: str = os.getenv("STUDENTPOINT_BASE_URL", "http://127.0.0.1:8000")

    @classmethod
    def setUpClass(cls) -> None:
        chrome_options = ChromeOptions()
        # chrome_options.add_argument("--headless=new")
        service = ChromeService(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)

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

    @unittest.skip("Por implementar: registro válido")
    def test_register_valido(self) -> None:
        pass

    @unittest.skip("Por implementar: validación de campos obligatorios")
    def test_register_validaciones(self) -> None:
        pass


