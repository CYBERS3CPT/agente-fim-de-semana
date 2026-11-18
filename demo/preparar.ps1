<#
preparar.ps1 — a versão Windows (PowerShell) do preparar.sh.

Monta a pasta da demo "construir um agente do zero": só as ferramentas (as
"mãos", que já vêm feitas) e os dados. O CLAUDE.md e a skill escrevem-se ao vivo.

  .\demo\preparar.ps1                     # cria $HOME\fds-ao-vivo
  .\demo\preparar.ps1 -Destino C:\ensaio  # ou onde quiseres
  .\demo\preparar.ps1 -Etapa 3            # salta para o fim da etapa 3 (plano B)
  .\demo\preparar.ps1 -Agenda             # bloco 05: junta a agenda com a injeção

Se o PowerShell disser que "a execução de scripts está desativada", corre
uma vez, só para esta janela:
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#>
param(
    [string]$Destino = (Join-Path $HOME "fds-ao-vivo"),
    [int]$Etapa = 1,
    [switch]$Agenda
)

$ErrorActionPreference = "Stop"
$Raiz = Split-Path -Parent $PSScriptRoot
$Marca = ".fds-ao-vivo"
# Caminhos que funcionam no PowerShell 5.1 (Windows) e no 7 (qualquer sistema)
function C { [IO.Path]::Combine([string[]]$args) }

if ($Agenda) {
    if (-not (Test-Path (Join-Path $Destino $Marca))) {
        Write-Host "Primeiro cria a pasta: .\demo\preparar.ps1"; exit 1
    }
    Copy-Item (C $Raiz "demo" "injecao" "agenda-do-bairro.html") (C $Destino "dados")
    Write-Host "Agenda do bairro em $Destino\dados\agenda-do-bairro.html. Que comece o teatro."
    exit 0
}

# Só apagamos pastas que este script criou (têm a marca .fds-ao-vivo).
if (Test-Path $Destino) {
    if (-not (Test-Path (Join-Path $Destino $Marca))) {
        Write-Host "'$Destino' já existe e não foi criada por este script. Não lhe toco."
        Write-Host "Escolhe outra pasta, ou apaga-a tu se tiveres a certeza."
        exit 1
    }
    Remove-Item -Recurse -Force $Destino
}

foreach ($d in "ferramentas", "dados", "saida", ".claude") {
    New-Item -ItemType Directory -Force -Path (Join-Path $Destino $d) | Out-Null
}
New-Item -ItemType File -Force -Path (Join-Path $Destino $Marca) | Out-Null

Copy-Item (C $Raiz "agente" "ferramentas" "*.py") (C $Destino "ferramentas")
Copy-Item (C $Raiz "agente" "dados" "*") (C $Destino "dados")
Copy-Item (C $Raiz "agente" ".claude" "settings.json") (C $Destino ".claude")
Copy-Item -Recurse (C $Raiz "agente" ".claude" "hooks") (C $Destino ".claude" "hooks")
Copy-Item -Recurse (C $Raiz "agente" ".claude" "agents") (C $Destino ".claude" "agents")

if ($Etapa -ge 2) {
    Copy-Item (C $Raiz "demo" "etapas" "etapa-2-CLAUDE.md") (C $Destino "CLAUDE.md")
}
if ($Etapa -ge 3) {
    $skill = C $Destino ".claude" "skills" "fim-de-semana"
    New-Item -ItemType Directory -Force -Path $skill | Out-Null
    Copy-Item (C $Raiz "demo" "etapas" "etapa-3-SKILL.md") (C $skill "SKILL.md")
}
if ($Etapa -ge 5) {
    Get-Content -Raw -Encoding UTF8 (C $Raiz "demo" "etapas" "etapa-5-avisos.md") |
        Add-Content -Encoding UTF8 (C $Destino "CLAUDE.md")
}

Write-Host ""
Write-Host "Pasta pronta: $Destino  (etapa $Etapa)"
Write-Host ""
Write-Host "  cd `"$Destino`"; claude"
Write-Host ""
Write-Host "Na primeira vez o Claude Code pergunta se confias na pasta: diz que sim."
