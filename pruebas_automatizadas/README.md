# Pruebas automatizadas (Selenium)

Guía rápida para ejecutar las pruebas E2E con Selenium sobre StudentsPoint.

## Requisitos
- Python 3.11+
- Google Chrome instalado
- Dependencias de prueba:

```bash
python -m pip install selenium webdriver-manager
```

## Levantar el backend
Asegúrate de tener el servidor corriendo antes de ejecutar cualquier prueba:

```bash
python proyecto\src\backend\manage.py runserver 127.0.0.1:8000
```

## Ejecutar todas las pruebas
Descubrimiento de pruebas en la carpeta `pruebas_automatizadas`:

```bash
python run_pruebas.py
```

## Ejecutar por archivo, clase o método
- Por archivo (módulo):
```bash
python -m unittest pruebas_automatizadas.test_homepage
python -m unittest pruebas_automatizadas.test_login
python -m unittest pruebas_automatizadas.test_register
```

- Por clase:
```bash
python -m unittest pruebas_automatizadas.test_login.TestLoginE2E
```

- Por método (ejemplo dado):
```bash
python -m unittest pruebas_automatizadas.test_login.TestLoginE2E.test_login_valido
```

- Por patrón (Python ≥ 3.12):
```bash
python -m unittest -k login_valido
```

## Comportamiento del navegador (ver ejecución)
Cada test define al inicio dos constantes que controlan el cierre del navegador:

- `KEEP_BROWSER_OPEN = False`  → Ponlo en `True` para que no se cierre al terminar.
- `CLOSE_DELAY_SECONDS = 5`    → Segundos a esperar antes de cerrar (útil para observar).

Si necesitas pausas intermedias de depuración, puedes usar `time.sleep(segundos)` dentro del test.

## URLs y credenciales de ejemplo
- Login: `http://127.0.0.1:8000/login.html`
- Home: `http://127.0.0.1:8000/` o `http://127.0.0.1:8000/index.html`
- Credenciales admin (demo): `admin@studentspoint.app` / `admin123`

## Estructura
- `pruebas_automatizadas/test_homepage.py`  → Verifica carga de la página principal
- `pruebas_automatizadas/test_login.py`     → Flujo de inicio de sesión
- `pruebas_automatizadas/test_register.py`  → Esqueletos para registro (por implementar)
- `run_pruebas.py`                           → Runner de descubrimiento y ejecución

## Problemas comunes
- Se abre `data:,` en Chrome: verifica que el test no esté marcado con `@unittest.skip` y que el servidor esté corriendo.
- No descarga el driver: la primera ejecución puede tardar; requiere Internet para `webdriver-manager`.
- No redirige tras login: espera unos segundos; el `login.html` guarda tokens y luego redirige a `/` → el test acepta también `index.html`.
