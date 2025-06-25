# exportar_a_json.ps1

$directorioBase = "C:\tesis\pharma-traceability-backend"
$archivos = Get-ChildItem -Path $directorioBase -Recurse -File | Where-Object {
    $_.FullName -notmatch "\\env\\" -and $_.FullName -notmatch "\\.git\\"
}
$resultado = @()

foreach ($archivo in $archivos) {
    $rutaRelativa = $archivo.FullName.Replace($directorioBase + "\", "") -replace "\\", "/"
    $contenido = Get-Content $archivo.FullName -Raw
    $resultado += [pscustomobject]@{
        path    = $rutaRelativa
        content = $contenido
    }
}

# Convertir a JSON y guardar
$json = $resultado | ConvertTo-Json -Depth 3
Set-Content -Path "$directorioBase\estructura_proyecto.json" -Value $json -Encoding UTF8

Write-Host "✅ Archivo JSON generado: estructura_proyecto.json"
