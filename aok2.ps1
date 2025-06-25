# exportar_proyecto_estructurado.ps1
# Genera un archivo markdown estructurado ideal para compartir con IA

$directorioBase = "C:\tesis\pharma-traceability-backend"
$archivoSalida = "$directorioBase\PROYECTO_COMPLETO.md"

# Configuración de archivos a incluir/excluir
$extensionesIncluir = @('.js', '.ts', '.jsx', '.tsx', '.py', '.java', '.cs', '.php', '.rb', '.go', '.rs', '.cpp', '.c', '.h', '.sql', '.json', '.xml', '.yaml', '.yml', '.md', '.txt', '.env.example', '.gitignore', '.dockerignore', 'Dockerfile', 'docker-compose.yml', 'package.json', 'requirements.txt', 'pom.xml', '.csproj', 'Gemfile', 'go.mod', 'Cargo.toml')
$carpetasExcluir = @('node_modules', 'env', 'venv', '.git', '.vs', '.vscode', 'bin', 'obj', 'target', 'build', 'dist', '__pycache__', '.pytest_cache', 'coverage')

# Función para verificar si un archivo debe incluirse
function Should-Include-File($archivo) {
    $nombre = $archivo.Name
    $extension = $archivo.Extension
    $rutaCompleta = $archivo.FullName
    
    # Excluir carpetas específicas
    foreach ($carpeta in $carpetasExcluir) {
        if ($rutaCompleta -match "\\$carpeta\\") {
            return $false
        }
    }
    
    # Incluir archivos sin extensión importantes (como Dockerfile)
    if ($extension -eq "" -and $nombre -in @('Dockerfile', 'Makefile', 'Procfile')) {
        return $true
    }
    
    # Incluir por extensión
    return $extension -in $extensionesIncluir
}

# Función para obtener el tipo de archivo
function Get-File-Type($archivo) {
    $extension = $archivo.Extension.ToLower()
    switch ($extension) {
        {$_ -in @('.js', '.jsx')} { return 'javascript' }
        {$_ -in @('.ts', '.tsx')} { return 'typescript' }
        '.py' { return 'python' }
        '.java' { return 'java' }
        '.cs' { return 'csharp' }
        '.php' { return 'php' }
        '.rb' { return 'ruby' }
        '.go' { return 'go' }
        '.rs' { return 'rust' }
        {$_ -in @('.cpp', '.cc', '.cxx')} { return 'cpp' }
        '.c' { return 'c' }
        '.h' { return 'c' }
        '.sql' { return 'sql' }
        '.json' { return 'json' }
        '.xml' { return 'xml' }
        {$_ -in @('.yaml', '.yml')} { return 'yaml' }
        '.md' { return 'markdown' }
        '.sh' { return 'bash' }
        '.ps1' { return 'powershell' }
        '.dockerfile' { return 'dockerfile' }
        default { 
            if ($archivo.Name -eq 'Dockerfile') { return 'dockerfile' }
            return 'text' 
        }
    }
}

Write-Host "🔍 Analizando estructura del proyecto..." -ForegroundColor Yellow

# Obtener todos los archivos
$archivos = Get-ChildItem -Path $directorioBase -Recurse -File | Where-Object { Should-Include-File $_ }

# Crear contenido markdown
$contenido = @"
# 📋 PROYECTO COMPLETO: Pharma Traceability Backend

> **Generado automáticamente el:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
> **Directorio base:** $directorioBase
> **Total de archivos:** $($archivos.Count)

## 📁 ESTRUCTURA DEL PROYECTO

``````
$(tree $directorioBase /F /A | Out-String)
``````

## 📊 RESUMEN DE ARCHIVOS

"@

# Agrupar archivos por tipo
$archivosPorTipo = $archivos | Group-Object { Get-File-Type $_ } | Sort-Object Name

foreach ($grupo in $archivosPorTipo) {
    $contenido += "`n### $($grupo.Name.ToUpper()) ($($grupo.Count) archivos)`n"
    foreach ($archivo in $grupo.Group | Sort-Object Name) {
        $rutaRelativa = $archivo.FullName.Replace($directorioBase + "\", "") -replace "\\", "/"
        $contenido += "- ``$rutaRelativa```n"
    }
}

$contenido += "`n`n## 📄 CONTENIDO DE ARCHIVOS`n`n"

# Agregar contenido de cada archivo
foreach ($archivo in $archivos | Sort-Object FullName) {
    $rutaRelativa = $archivo.FullName.Replace($directorioBase + "\", "") -replace "\\", "/"
    $tipoArchivo = Get-File-Type $archivo
    
    Write-Host "📄 Procesando: $rutaRelativa" -ForegroundColor Green
    
    $contenido += "### 📄 ``$rutaRelativa```n`n"
    
    try {
        $contenidoArchivo = Get-Content $archivo.FullName -Raw -Encoding UTF8
        
        # Escapar caracteres especiales de markdown si es necesario
        if ($tipoArchivo -eq 'markdown') {
            $contenido += "$contenidoArchivo`n`n"
        } else {
            $contenido += "``````$tipoArchivo`n$contenidoArchivo`n```````n`n"
        }
    }
    catch {
        $contenido += "*[Error al leer el archivo: $($_.Exception.Message)]*`n`n"
    }
    
    $contenido += "---`n`n"
}

# Agregar información adicional útil para la IA
$contenido += @"
## 🤖 INFORMACIÓN PARA IA

### Contexto del Proyecto
- **Nombre:** Pharma Traceability Backend
- **Tipo:** Sistema de trazabilidad farmacéutica
- **Propósito:** Backend para rastrear medicamentos en la cadena de suministro

### Instrucciones para Modificaciones
1. **Siempre especifica el archivo exacto** usando la ruta relativa mostrada arriba
2. **Mantén la estructura existente** del proyecto
3. **Considera las dependencias** entre archivos al hacer cambios
4. **Respeta los patrones** de código existentes
5. **Incluye manejo de errores** apropiado

### Archivos Clave a Considerar
- Archivos de configuración (package.json, requirements.txt, etc.)
- Archivos de entrada principal (main.py, index.js, etc.)
- Archivos de rutas/endpoints
- Modelos de datos
- Archivos de pruebas

### Tecnologías Detectadas
$($archivosPorTipo | ForEach-Object { "- $($_.Name): $($_.Count) archivos" } | Out-String)

---
**Fin del documento**
"@

# Guardar archivo
try {
    Set-Content -Path $archivoSalida -Value $contenido -Encoding UTF8
    Write-Host "✅ Archivo generado exitosamente: PROYECTO_COMPLETO.md" -ForegroundColor Green
    Write-Host "📁 Ubicación: $archivoSalida" -ForegroundColor Cyan
    Write-Host "📊 Archivos procesados: $($archivos.Count)" -ForegroundColor Yellow
    
    # Mostrar tamaño del archivo
    $tamano = (Get-Item $archivoSalida).Length
    $tamanoMB = [Math]::Round($tamano / 1MB, 2)
    Write-Host "📏 Tamaño del archivo: $tamanoMB MB" -ForegroundColor Magenta
}
catch {
    Write-Host "❌ Error al generar el archivo: $($_.Exception.Message)" -ForegroundColor Red
}


