#  Quick Start - StudentsPoint

Comandos rápidos para desarrolladores

##  Iniciar el Proyecto

### Desarrollo (Windows)
```powershell
# Terminal 1 - Backend
cd proyecto\src\backend
python manage.py runserver

# Terminal 2 - Logs (opcional)
cd proyecto\src\backend
Get-Content logs\general.log -Wait -Tail 50
```

### Linux/Mac
```bash
# Terminal 1 - Backend
cd proyecto/src/backend
python manage.py runserver

# Terminal 2 - Logs (opcional)
tail -f logs/general.log
```

##  Tests

```bash
# Ejecutar todos los tests
python run_pytest.py

# Tests específicos
pytest pruebas_unitarias/api/test_forum_api.py
pytest pruebas_unitarias/api/test_profile_api.py -v
```

##  Monitoreo

```bash
# Monitor en tiempo real (actualiza cada 60s)
python monitor_logs.py

# Una sola vez
python monitor_logs.py --once

# Ver últimos 10 errores
python monitor_logs.py --recent 10

# Análisis detallado
python analyze_logs.py --hours 24

# Sistema de alertas
python alert_system.py
```

##  Base de Datos

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell de Django
python manage.py shell
```

##  Archivos Estáticos

```bash
# Recolectar estáticos
python manage.py collectstatic --noinput

# Limpiar y recolectar
python manage.py collectstatic --noinput --clear
```

##  Debugging

```bash
# Ver logs de errores
Get-Content logs\errors.log -Wait -Tail 20  # Windows
tail -f logs/errors.log  # Linux/Mac

# Ver logs de API
Get-Content logs\api.log -Wait  # Windows

# Ver logs de autenticación
tail -f logs/auth.log  # Linux/Mac

# Verificar sistema
python manage.py check
python manage.py check --deploy  # Para producción
```

##  Utilidades

```bash
# Limpiar cache
python manage.py clear_cache

# Ver URLs disponibles
python manage.py show_urls  # Si está instalado django-extensions

# Crear datos de prueba
python create_sample_data.py

# Ver configuración
python manage.py diffsettings
```

##  URLs Importantes

- **Frontend**: http://127.0.0.1:8000
- **Admin**: http://127.0.0.1:8000/admin/
- **API Docs**: http://127.0.0.1:8000/api/docs/
- **Health**: http://127.0.0.1:8000/health/

**Credenciales por defecto:**
- Email: `admin@studentspoint.app`
- Password: `admin123`

##  Git

```bash
# Ver estado
git status

# Ver cambios
git diff

# Agregar cambios
git add .

# Commit
git commit -m "Descripción"

# Push
git push origin main

# Ver logs
git log --oneline --graph --decorate -n 10
```

##  Troubleshooting Rápido

### Error: Port already in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID [PID] /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Error: Database locked
```bash
# Cerrar todas las conexiones
python manage.py dbshell
.quit
```

### Error: Static files not found
```bash
python manage.py collectstatic --noinput --clear
```

### Error: Permission denied (logs)
```bash
# Windows (ejecutar PowerShell como Admin)
icacls logs /grant Users:F /T

# Linux/Mac
chmod -R 755 logs/
```

##  Tips Rápidos

1. **Logs en tiempo real**: Usa `monitor_logs.py` en lugar de `tail`
2. **Performance**: Agrega `?debug=performance` a cualquier URL
3. **Cache**: El frontend usa cache automático (5 min por defecto)
4. **Lazy loading**: Las imágenes con `data-src` cargan automáticamente
5. **Debugging**: Los headers HTTP incluyen `X-DB-Query-Count`

##  Enlaces Útiles

- [Documentación Completa](Documentacion/)
- [Sistema de Logging](Documentacion/guias/SISTEMA-LOGGING.md)
- [Deployment](Documentacion/guias/DEPLOYMENT-PRODUCTION.md)
- [Proyecto Masterizado](PROYECTO-MASTERIZADO.md)

##  Soporte

Si algo no funciona:
1. Revisa `logs/errors.log`
2. Ejecuta `python manage.py check`
3. Verifica `python monitor_logs.py --once`
4. Consulta `PROYECTO-MASTERIZADO.md`

---

**¡Listo para desarrollar!** 

