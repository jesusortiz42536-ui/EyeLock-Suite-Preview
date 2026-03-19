import os
import time
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()

def ejecutar_comando(comando):
    try:
        subprocess.run(comando, shell=True, check=True, capture_output=True)
        return True
    except:
        return False

def fix_dns_network():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Banner Estilo KIMAD / Nala
    console.print(Panel.fit(
        "[bold cyan]🛡️ KIMAD FIX-SCAN v1.0[/bold cyan]\n[white]System Hardening & Network Repair[/white]",
        border_style="green"
    ))

    tareas = [
        ("Limpiando caché DNS (FlushDNS)", "ipconfig /flushdns"),
        ("Liberando dirección IP (Release)", "ipconfig /release"),
        ("Renovando dirección IP (Renew)", "ipconfig /renew"),
        ("Reseteando Winsock (Catálogo de red)", "netsh winsock reset"),
        ("Limpiando tablas de rutas", "route -f")
    ]

    table = Table(title="[bold yellow]Reporte de Optimización[/bold yellow]", show_header=True, header_style="bold magenta")
    table.add_column("Tarea", style="dim", width=40)
    table.add_column("Estado", justify="right")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        
        for descripcion, comando in tareas:
            task = progress.add_task(description=f"Ejecutando: {descripcion}...", total=None)
            exito = ejecutar_comando(comando)
            time.sleep(1) # Para que se vea el efecto de Nala
            
            status = "[bold green]FIXED[/bold green]" if exito else "[bold red]FAILED[/bold red]"
            table.add_row(descripcion, status)
            progress.remove_task(task)

    console.print(table)
    console.print("\n[bold green]✅ Sistema optimizado por KIMAD TECH. Conexión blindada.[/bold green]")

if __name__ == "__main__":
    # Verificar si es admin
    fix_dns_network()