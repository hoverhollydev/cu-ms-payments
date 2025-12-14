# Variables
$namespace = "hoverdev-dev"
$allowedLabel = "app=cu-ms-payments"
$targetHost = "mi-postgres-postgresql-primary.hoverdev-dev.svc.cluster.local"
$targetPort = 5432
$dbUser = "postgres"
$dbPassword = "MiPasswordSeguro123"
$dbName = "postgres"

Write-Host "=== Comprobando NetworkPolicy payments → Postgres ===`n"

# 1️⃣ Listar pods permitidos
$allowedPods = oc get pods -n $namespace -l $allowedLabel -o jsonpath='{.items[*].metadata.name}' | Out-String
$allowedPods = $allowedPods -split "\s+"

foreach ($pod in $allowedPods) {
    if ($pod) {
        Write-Host "[+] Probando desde pod permitido: $pod"
        try {
            $result = oc exec -n $namespace $pod -- python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='$targetHost',
        port=$targetPort,
        user='$dbUser',
        password='$dbPassword',
        dbname='$dbName'
    )
    print('OK')
    conn.close()
except:
    print('FAIL')
"
            if ($result -eq "OK") {
                Write-Host "    Conexión permitida ✅" -ForegroundColor Green
            } else {
                Write-Host "    Conexión FALLIDA ❌" -ForegroundColor Red
            }
        } catch {
            Write-Host "    Error al ejecutar prueba: $_" -ForegroundColor Red
        }
    }
}

# 2️⃣ Probar desde pod NO permitido (temporal)
Write-Host "`n[+] Probando desde pod NO permitido (temporal)..."

try {
    $cmd = "psql ""host=$targetHost port=$targetPort user=$dbUser password=$dbPassword dbname=$dbName"" -c '\conninfo'"
    oc run test-pod --rm -i --tty --image=postgres:15 --restart=Never -- $cmd
} catch {
    Write-Host "    Error al probar pod temporal: $_" -ForegroundColor Red
}

Write-Host "`n=== Prueba de NetworkPolicy finalizada ==="
