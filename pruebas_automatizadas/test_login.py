"""Esqueletos de pruebas E2E para Login con Selenium."""

import os
import unittest
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


KEEP_BROWSER_OPEN = False
CLOSE_DELAY_SECONDS = 5

class TestLoginE2E(unittest.TestCase):
    """Casos de autenticación (por implementar)."""

    driver: Optional[webdriver.Chrome] = None
    base_url: str = os.getenv("STUDENTPOINT_BASE_URL", "http://127.0.0.1:8000")

    @classmethod
    def setUpClass(cls) -> None:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
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

    def test_login_valido(self) -> None:
        assert self.driver is not None

        login_url = "http://127.0.0.1:8000/login.html"
        self.driver.get(login_url)

        # Esperar campos visibles
        wait = WebDriverWait(self.driver, 20)
        email_input = wait.until(EC.visibility_of_element_located((By.ID, "email")))
        password_input = wait.until(EC.visibility_of_element_located((By.ID, "password")))

        # Completar credenciales
        email_input.clear()
        email_input.send_keys("admin@studentspoint.app")
        time.sleep(2) 
        password_input.clear()
        password_input.send_keys("admin123")
        time.sleep(2) 

        # Enviar formulario
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "form#loginForm button[type='submit']")
        submit_btn.click()

        # Esperar éxito: token en localStorage o alerta de éxito
        def login_success(driver: webdriver.Chrome) -> bool:
            try:
                token_present = driver.execute_script("return !!window.localStorage.getItem('access_token');")
            except Exception:
                token_present = False
            alert_success = len(driver.find_elements(By.CSS_SELECTOR, ".alert.alert-success")) > 0
            return token_present or alert_success

        wait.until(login_success)

        # Esperar redirección a home (index.html o /)
        allowed_urls = {
            "http://127.0.0.1:8000/",
            "http://127.0.0.1:8000",
            "http://127.0.0.1:8000/index.html",
        }

        def redirected_home(driver: webdriver.Chrome) -> bool:
            return driver.current_url in allowed_urls

        wait.until(redirected_home)

        # Asserts finales
        token_value = self.driver.execute_script("return window.localStorage.getItem('access_token');")
        self.assertIsNotNone(token_value)
        self.assertIn(self.driver.current_url, allowed_urls, msg=f"URL actual no es home: {self.driver.current_url}")

    @unittest.skip("Por implementar: credenciales inválidas")
    def test_login_invalido(self) -> None:
        pass


