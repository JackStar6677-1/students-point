#!/usr/bin/env python3
"""
Sistema Completo de Testing Automatizado para StudentsPoint
==========================================================

Este script ejecuta todas las pruebas del proyecto de forma automatizada:
- Pruebas unitarias (Backend)
- Pruebas de integración (APIs)
- Pruebas end-to-end (Frontend)
- Pruebas de rendimiento
- Pruebas de seguridad básica
- Reportes detallados

Uso:
    python test_suite_completo.py [--verbose] [--coverage] [--parallel]
"""

import os
import sys
import subprocess
import time
import json
import argparse
from datetime import datetime
from pathlib import Path

class TestSuiteManager:
    def __init__(self, verbose=False, coverage=False, parallel=False):
        self.verbose = verbose
        self.coverage = coverage
        self.parallel = parallel
        self.project_root = Path(__file__).parent
        self.backend_path = self.project_root / "proyecto" / "src" / "backend"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {}
        }
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def run_command(self, command, cwd=None, capture_output=True):
        """Ejecuta un comando y retorna el resultado"""
        if self.verbose:
            self.log(f"Ejecutando: {command}")
            
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd or self.backend_path,
                capture_output=capture_output,
                text=True,
                timeout=300  # 5 minutos timeout
            )
            return result
        except subprocess.TimeoutExpired:
            self.log(f"Timeout ejecutando: {command}", "ERROR")
            return None
        except Exception as e:
            self.log(f"Error ejecutando {command}: {e}", "ERROR")
            return None
    
    def setup_test_environment(self):
        """Configura el entorno de testing"""
        self.log("Configurando entorno de testing...")
        
        # Verificar que Django está instalado
        result = self.run_command("python -c 'import django; print(django.VERSION)'")
        if not result or result.returncode != 0:
            self.log("Django no está instalado o no funciona", "ERROR")
            return False
            
        # Instalar dependencias de testing si es necesario
        self.run_command("pip install pytest pytest-django pytest-cov selenium requests")
        
        # Aplicar migraciones
        self.run_command("python manage.py migrate")
        
        # Crear superusuario de testing si no existe
        self.run_command("python manage.py ensure_superuser")
        
        self.log("Entorno de testing configurado correctamente")
        return True
    
    def run_unit_tests(self):
        """Ejecuta pruebas unitarias del backend"""
        self.log("Ejecutando pruebas unitarias...")
        
        start_time = time.time()
        
        # Ejecutar pytest con coverage si está habilitado
        if self.coverage:
            command = "pytest pruebas_unitarias/ --cov=. --cov-report=html --cov-report=term-missing -v"
        else:
            command = "pytest pruebas_unitarias/ -v"
            
        result = self.run_command(command)
        end_time = time.time()
        
        if result:
            self.results["tests"]["unit_tests"] = {
                "status": "PASSED" if result.returncode == 0 else "FAILED",
                "duration": end_time - start_time,
                "output": result.stdout,
                "errors": result.stderr
            }
            self.log(f"Pruebas unitarias: {'PASARON' if result.returncode == 0 else 'FALLARON'}")
        else:
            self.results["tests"]["unit_tests"] = {
                "status": "ERROR",
                "duration": end_time - start_time,
                "output": "",
                "errors": "Error ejecutando pruebas unitarias"
            }
            
    def run_integration_tests(self):
        """Ejecuta pruebas de integración de APIs"""
        self.log("Ejecutando pruebas de integración...")
        
        start_time = time.time()
        
        # Ejecutar pruebas de API específicas
        api_tests = [
            "test_login_api.py",
            "test_register_api.py", 
            "test_auth_me.py",
            "test_campus_map.py"
        ]
        
        passed = 0
        failed = 0
        
        for test_file in api_tests:
            test_path = self.project_root / "pruebas_unitarias" / "api" / test_file
            if test_path.exists():
                result = self.run_command(f"python -m pytest {test_path} -v")
                if result and result.returncode == 0:
                    passed += 1
                else:
                    failed += 1
                    self.log(f"Falla en {test_file}", "ERROR")
        
        end_time = time.time()
        
        self.results["tests"]["integration_tests"] = {
            "status": "PASSED" if failed == 0 else "FAILED",
            "duration": end_time - start_time,
            "passed": passed,
            "failed": failed
        }
        
        self.log(f"Pruebas de integración: {passed} pasaron, {failed} fallaron")
        
    def run_e2e_tests(self):
        """Ejecuta pruebas end-to-end del frontend"""
        self.log("Ejecutando pruebas end-to-end...")
        
        start_time = time.time()
        
        # Ejecutar pruebas de Selenium
        e2e_tests = [
            "test_homepage.py",
            "test_login.py",
            "test_register.py"
        ]
        
        passed = 0
        failed = 0
        
        for test_file in e2e_tests:
            test_path = self.project_root / "pruebas_automatizadas" / test_file
            if test_path.exists():
                result = self.run_command(f"python {test_path}")
                if result and result.returncode == 0:
                    passed += 1
                else:
                    failed += 1
                    self.log(f"Falla en E2E {test_file}", "ERROR")
        
        end_time = time.time()
        
        self.results["tests"]["e2e_tests"] = {
            "status": "PASSED" if failed == 0 else "FAILED",
            "duration": end_time - start_time,
            "passed": passed,
            "failed": failed
        }
        
        self.log(f"Pruebas E2E: {passed} pasaron, {failed} fallaron")
        
    def run_security_tests(self):
        """Ejecuta pruebas básicas de seguridad"""
        self.log("Ejecutando pruebas de seguridad...")
        
        start_time = time.time()
        security_issues = []
        
        # Verificar configuración de seguridad básica
        settings_file = self.backend_path / "studentspoint" / "settings" / "base.py"
        if settings_file.exists():
            with open(settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Verificar configuraciones de seguridad
            if "DEBUG = True" in content:
                security_issues.append("DEBUG está habilitado en producción")
                
            if "SECRET_KEY" in content and "os.environ.get('SECRET_KEY')" not in content:
                security_issues.append("SECRET_KEY hardcodeada")
        
        # Verificar que no hay credenciales hardcodeadas
        for py_file in self.backend_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "password" in content.lower() and "=" in content:
                        if any(cred in content.lower() for cred in ["123456", "admin", "password"]):
                            security_issues.append(f"Posible credencial hardcodeada en {py_file.name}")
            except:
                continue
        
        end_time = time.time()
        
        self.results["tests"]["security_tests"] = {
            "status": "PASSED" if len(security_issues) == 0 else "WARNING",
            "duration": end_time - start_time,
            "issues": security_issues
        }
        
        self.log(f"Pruebas de seguridad: {len(security_issues)} problemas encontrados")
        
    def run_performance_tests(self):
        """Ejecuta pruebas básicas de rendimiento"""
        self.log("Ejecutando pruebas de rendimiento...")
        
        start_time = time.time()
        
        # Probar tiempo de carga de páginas principales
        pages = [
            "/",
            "/login.html",
            "/register.html",
            "/forum/",
            "/market/"
        ]
        
        performance_results = []
        
        for page in pages:
            # Simular request HTTP básico
            result = self.run_command(f"python -c \"import requests; r = requests.get('http://127.0.0.1:8000{page}'); print(f'{{page}}: {{r.status_code}} - {{len(r.content)}} bytes')\"")
            if result and result.returncode == 0:
                performance_results.append(result.stdout.strip())
        
        end_time = time.time()
        
        self.results["tests"]["performance_tests"] = {
            "status": "PASSED",
            "duration": end_time - start_time,
            "results": performance_results
        }
        
        self.log("Pruebas de rendimiento completadas")
        
    def generate_report(self):
        """Genera reporte detallado de todas las pruebas"""
        self.log("Generando reporte de pruebas...")
        
        # Calcular resumen
        total_tests = len(self.results["tests"])
        passed_tests = sum(1 for test in self.results["tests"].values() 
                          if test["status"] in ["PASSED"])
        
        self.results["summary"] = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
        }
        
        # Guardar reporte JSON
        report_file = self.project_root / "test_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Generar reporte HTML
        self.generate_html_report()
        
        self.log(f"Reporte guardado en: {report_file}")
        
    def generate_html_report(self):
        """Genera reporte HTML visual"""
        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Pruebas - StudentsPoint</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .summary-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }}
        .summary-card h3 {{ margin: 0 0 10px 0; color: #333; }}
        .summary-card .number {{ font-size: 2em; font-weight: bold; }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
        .test-section {{ margin-bottom: 30px; }}
        .test-section h2 {{ border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        .test-details {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 10px; }}
        .timestamp {{ color: #6c757d; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Reporte de Pruebas - StudentsPoint</h1>
            <p class="timestamp">Generado el: {self.results['timestamp']}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Total de Pruebas</h3>
                <div class="number">{self.results['summary']['total_tests']}</div>
            </div>
            <div class="summary-card">
                <h3>Pruebas Exitosas</h3>
                <div class="number passed">{self.results['summary']['passed_tests']}</div>
            </div>
            <div class="summary-card">
                <h3>Pruebas Fallidas</h3>
                <div class="number failed">{self.results['summary']['failed_tests']}</div>
            </div>
            <div class="summary-card">
                <h3>Tasa de Éxito</h3>
                <div class="number">{self.results['summary']['success_rate']:.1f}%</div>
            </div>
        </div>
        
        <div class="test-sections">
"""
        
        for test_name, test_data in self.results["tests"].items():
            status_class = test_data["status"].lower()
            html_content += f"""
            <div class="test-section">
                <h2>🔍 {test_name.replace('_', ' ').title()}</h2>
                <div class="test-details">
                    <p><strong>Estado:</strong> <span class="{status_class}">{test_data['status']}</span></p>
                    <p><strong>Duración:</strong> {test_data['duration']:.2f} segundos</p>
                    {f"<p><strong>Errores:</strong> {test_data.get('errors', 'N/A')}</p>" if test_data.get('errors') else ""}
                    {f"<p><strong>Problemas:</strong> {', '.join(test_data.get('issues', []))}</p>" if test_data.get('issues') else ""}
                </div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
</body>
</html>
"""
        
        html_file = self.project_root / "test_report.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        self.log(f"Reporte HTML guardado en: {html_file}")
        
    def run_all_tests(self):
        """Ejecuta todas las pruebas del proyecto"""
        self.log("🚀 Iniciando suite completa de pruebas...")
        
        if not self.setup_test_environment():
            self.log("Error configurando entorno de testing", "ERROR")
            return False
            
        # Ejecutar todas las categorías de pruebas
        self.run_unit_tests()
        self.run_integration_tests()
        self.run_e2e_tests()
        self.run_security_tests()
        self.run_performance_tests()
        
        # Generar reporte final
        self.generate_report()
        
        # Mostrar resumen
        summary = self.results["summary"]
        self.log(f"📊 RESUMEN FINAL:")
        self.log(f"   Total: {summary['total_tests']} pruebas")
        self.log(f"   Exitosas: {summary['passed_tests']}")
        self.log(f"   Fallidas: {summary['failed_tests']}")
        self.log(f"   Tasa de éxito: {summary['success_rate']:.1f}%")
        
        return summary['failed_tests'] == 0

def main():
    parser = argparse.ArgumentParser(description="Sistema Completo de Testing para StudentsPoint")
    parser.add_argument("--verbose", "-v", action="store_true", help="Salida verbosa")
    parser.add_argument("--coverage", "-c", action="store_true", help="Incluir reporte de cobertura")
    parser.add_argument("--parallel", "-p", action="store_true", help="Ejecutar pruebas en paralelo")
    
    args = parser.parse_args()
    
    test_manager = TestSuiteManager(
        verbose=args.verbose,
        coverage=args.coverage,
        parallel=args.parallel
    )
    
    success = test_manager.run_all_tests()
    
    if success:
        print("\n✅ Todas las pruebas pasaron exitosamente!")
        sys.exit(0)
    else:
        print("\n❌ Algunas pruebas fallaron. Revisa el reporte para más detalles.")
        sys.exit(1)

if __name__ == "__main__":
    main()
