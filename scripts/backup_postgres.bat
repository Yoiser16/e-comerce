@echo off
REM ==============================================================================
REM SCRIPT DE BACKUP PARA POSTGRESQL (Windows)
REM ==============================================================================
REM
REM Uso:
REM   backup_postgres.bat
REM
REM Variables de entorno requeridas:
REM   DB_HOST     - Host de PostgreSQL
REM   DB_PORT     - Puerto (default: 5432)
REM   DB_NAME     - Nombre de la base de datos
REM   DB_USER     - Usuario de PostgreSQL
REM   PGPASSWORD  - Password de PostgreSQL
REM
REM ==============================================================================

setlocal enabledelayedexpansion

REM Configuración
if "%DB_HOST%"=="" set DB_HOST=localhost
if "%DB_PORT%"=="" set DB_PORT=5432
if "%DB_NAME%"=="" set DB_NAME=ecommerce
if "%DB_USER%"=="" set DB_USER=postgres
if "%BACKUP_DIR%"=="" set BACKUP_DIR=.\backups

REM Timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,8%_%datetime:~8,6%
set BACKUP_FILENAME=backup_%DB_NAME%_%TIMESTAMP%.sql

echo.
echo ==============================================
echo   BACKUP POSTGRESQL - E-COMMERCE
echo   %date% %time%
echo ==============================================
echo.

REM Crear directorio de backups
if not exist "%BACKUP_DIR%" (
    echo [INFO] Creando directorio de backups...
    mkdir "%BACKUP_DIR%"
)

echo [INFO] Host: %DB_HOST%:%DB_PORT%
echo [INFO] Database: %DB_NAME%
echo [INFO] User: %DB_USER%
echo [INFO] Output: %BACKUP_DIR%\%BACKUP_FILENAME%
echo.

REM Verificar que pg_dump existe
where pg_dump >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] pg_dump no encontrado. Agregar PostgreSQL bin al PATH
    exit /b 1
)

REM Verificar PGPASSWORD
if "%PGPASSWORD%"=="" (
    echo [WARN] PGPASSWORD no definido. El backup puede fallar.
)

REM Realizar backup
echo [INFO] Ejecutando pg_dump...
pg_dump -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %DB_NAME% --no-owner --no-acl --clean --if-exists -f "%BACKUP_DIR%\%BACKUP_FILENAME%"

if %ERRORLEVEL% neq 0 (
    echo [ERROR] pg_dump falló
    exit /b 1
)

REM Verificar que se creó
if exist "%BACKUP_DIR%\%BACKUP_FILENAME%" (
    echo [INFO] Backup completado: %BACKUP_DIR%\%BACKUP_FILENAME%
    
    REM Mostrar tamaño
    for %%A in ("%BACKUP_DIR%\%BACKUP_FILENAME%") do echo [INFO] Tamaño: %%~zA bytes
) else (
    echo [ERROR] El archivo de backup no se creó
    exit /b 1
)

echo.
echo ==============================================
echo   BACKUP COMPLETADO EXITOSAMENTE
echo ==============================================
echo.
echo Para restaurar:
echo   psql -h %DB_HOST% -U %DB_USER% -d %DB_NAME% -f "%BACKUP_DIR%\%BACKUP_FILENAME%"
echo.

exit /b 0
