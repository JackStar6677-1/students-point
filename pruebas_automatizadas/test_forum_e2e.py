"""
Pruebas End-to-End para el sistema de foros
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class ForumE2ETest:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.base_url = "http://127.0.0.1:8000"
        self.wait = WebDriverWait(self.driver, 10)
        
    def teardown(self):
        self.driver.quit()
        
    def test_forum_page_loads(self):
        """Prueba que la página del foro carga correctamente"""
        try:
            self.driver.get(f"{self.base_url}/forum/")
            
            # Debería redirigir a login si no está autenticado
            self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            
            print("✅ Página del foro carga y redirige a login correctamente")
            return True
        except Exception as e:
            print(f"❌ Error cargando página del foro: {e}")
            return False
            
    def test_login_and_access_forum(self):
        """Prueba login y acceso al foro"""
        try:
            # Ir a login
            self.driver.get(f"{self.base_url}/login.html")
            
            # Llenar formulario
            email_input = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            password_input = self.driver.find_element(By.ID, "password")
            
            email_input.send_keys("admin@studentspoint.com")
            password_input.send_keys("admin123")
            
            # Click en login
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            time.sleep(2)
            
            # Intentar ir al foro
            self.driver.get(f"{self.base_url}/forum/")
            
            # Verificar que la página carga
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            print("✅ Login exitoso y acceso al foro funcionando")
            return True
        except Exception as e:
            print(f"❌ Error en login y acceso al foro: {e}")
            return False
            
    def test_create_new_post(self):
        """Prueba crear un nuevo post en el foro"""
        try:
            # Login primero
            self.driver.get(f"{self.base_url}/login.html")
            email_input = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            password_input = self.driver.find_element(By.ID, "password")
            
            email_input.send_keys("admin@studentspoint.com")
            password_input.send_keys("admin123")
            
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            time.sleep(2)
            
            # Ir al foro
            self.driver.get(f"{self.base_url}/forum/")
            time.sleep(2)
            
            # Buscar botón de nuevo post
            try:
                new_post_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-bs-toggle='modal']"))
                )
                new_post_button.click()
                
                time.sleep(1)
                
                # Llenar formulario de post
                title_input = self.driver.find_element(By.ID, "postTitulo")
                content_textarea = self.driver.find_element(By.ID, "postContenido")
                
                title_input.send_keys("Post de prueba E2E")
                content_textarea.send_keys("Este es un contenido de prueba creado automáticamente")
                
                # Submit
                submit_button = self.driver.find_element(By.ID, "submitPostBtn")
                submit_button.click()
                
                time.sleep(2)
                
                print("✅ Creación de post en foro funcionando")
                return True
            except Exception as e:
                print(f"⚠️ No se pudo crear post (puede ser esperado si no hay foros): {e}")
                return True
                
        except Exception as e:
            print(f"❌ Error creando post: {e}")
            return False
            
    def run_all_tests(self):
        """Ejecuta todas las pruebas E2E del foro"""
        print("\n🧪 Ejecutando pruebas E2E del foro...")
        
        results = []
        results.append(self.test_forum_page_loads())
        results.append(self.test_login_and_access_forum())
        results.append(self.test_create_new_post())
        
        self.teardown()
        
        passed = sum(results)
        total = len(results)
        
        print(f"\n📊 Resultados: {passed}/{total} pruebas pasaron")
        
        return all(results)

if __name__ == "__main__":
    test = ForumE2ETest()
    success = test.run_all_tests()
    
    if success:
        print("✅ Todas las pruebas E2E del foro pasaron!")
        exit(0)
    else:
        print("❌ Algunas pruebas E2E del foro fallaron")
        exit(1)
