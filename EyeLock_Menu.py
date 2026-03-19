import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def mostrar_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Banner de Jefe con Estilo KIMAD
    console.print(Panel(
        "[bold green]EYELOCK SUITE v2.0[/bold green]\n[bold white]KIMAD TECH - ACTIVE DEFENSE SYSTEM[/bold white]",
        border_style="cyan",
        subtitle="[bold magenta]Dr. Encrypt Console[/bold magenta]",
        padding=(1, 2)
    ))

    # Tabla de Módulos Tácticos
    table = Table(show_header=True, header_style="bold yellow", expand=True)
    table.add_column("ID", style="dim", width=6, justify="center")
    table.add_column("MÓDULO TÁCTICO", style="bold white")
    table.add_column("ESTADO", style="green", justify="center")
    table.add_column("DESCRIPCIÓN", style="cyan")

    table.add_row("01", "SENTINEL NETWORK", "ONLINE", "Radar de red y bloqueo de IPs (Firewall)")
    table.add_row("02", "FIX-SCAN DNS", "ONLINE", "Optimización Nala Style (FlushDNS/Renew)")
    table.add_row("03", "PHARMA-SCAN", "ONLINE", "IA de reconocimiento de medicinas (OCR)")
    table.add_row("04", "SAT-VAULT", "LOCKED", "Bóveda cifrada para llaves .key y .cer")
    table.add_row("Q", "EXIT", "-", "Cerrar el búnker y salir")

    console.print(table)
    return input("\n[>] SELECCIONE MÓDULO PARA INICIAR: ").upper()

def ejecutar():
    while True:
        opcion = mostrar_menu()
        
        if opcion == "01":
            console.print("[yellow][*] Lanzando Sentinel Network...[/yellow]")
            os.system("python Sentinel_Monitor.py")
        elif opcion == "02":
            console.print("[yellow][*] Lanzando Fix-Scan...[/yellow]")
            os.system("python Fix_Scan.py")
            input("\nPresiona Enter para volver al Menú Maestro...")
        elif opcion == "03":
            console.print("[yellow][*] Lanzando Pharma-Scan...[/yellow]")
            os.system("python Pharma_Scan.py")
            input("\nPresiona Enter para volver al Menú Maestro...")
        elif opcion == "Q":
            console.print("[bold red][!] Desconectando... Búnker fuera de línea.[/bold red]")
            break
        else:
            console.print("[red][!] Error: Módulo no reconocido por KIMAD TECH.[/red]")
            time.sleep(1)

if __name__ == "__main__":
    ejecutar()