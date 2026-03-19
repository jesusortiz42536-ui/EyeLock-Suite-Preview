import psutil
import time
import os
import subprocess
import msvcrt # Librería para detectar teclas sin detener el programa (Solo Windows)

# --- CONFIGURACIÓN DE PODER ---
LOG_FILE = "sentinel_firewall.log"
VERDE = "\033[92m"
ROJO = "\033[91m"
CYAN = "\033[96m"
AMARILLO = "\033[93m"
RESET = "\033[0m"

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{VERDE}")
    print(r"""
    ██╗  ██╗██╗███╗   ███╗ █████╗ ██████╗     ████████╗██╗  ██╗███████╗    ██╗    ██╗ █████╗ ██╗     ██╗     
    ██║ ██╔╝██║████╗ ████║██╔══██╗██╔══██╗    ╚══██╔══╝██║  ██║██╔════╝    ██║    ██║██╔══██╗██║     ██║     
    █████╔╝ ██║██╔████╔██║███████║██║  ██║       ██║   ███████║█████╗      ██║ █╗ ██║███████║██║     ██║     
    ██╔═██╗ ██║██║╚██╔╝██║██╔══██║██║  ██║       ██║   ██╔══██║██╔══╝      ██║███╗██║██╔══██║██║     ██║     
    ██║  ██╗██║██║ ╚═╝ ██║██║  ██║██████╔╝       ██║   ██║  ██║███████╗    ╚███╔███╔╝██║  ██║███████╗███████╗
    ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝        ╚═╝   ╚═╝  ╚═╝╚══════╝     ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝
    """)
    print(f"{CYAN}    [ SENTINEL v3.1 - TACTICAL FIREWALL TRIGGER / BY DR. ENCRYPT ]{RESET}\n")

def bloquear_ip(ip):
    """Ejecuta el comando de Windows Firewall para banear la IP de forma permanente."""
    nombre_regla = f"KIMAD_BLOCK_{ip.replace('.', '_')}"
    # Comando netsh para crear la regla de bloqueo
    comando = f'netsh advfirewall firewall add rule name="{nombre_regla}" dir=in action=block remoteip={ip}'
    
    try:
        subprocess.run(comando, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        alerta = f"\n{ROJO}[🔒 BLOQUEADO] IP {ip} ha sido desterrada del sistema.{RESET}"
        print(alerta)
        with open(LOG_FILE, "a") as f:
            f.write(f"{time.ctime()} - {alerta}\n")
    except Exception as e:
        print(f"\n{ROJO}[!] ERROR: Asegúrate de ejecutar como ADMINISTRADOR.{RESET}")

def monitorear_red():
    banner()
    print(f"{AMARILLO}[*] Escaneo profundo activo. Presiona 'B' cuando veas una IP para bloquearla.{RESET}")
    print(f"{CYAN}{'PID':<8} {'PROGRAMA':<20} {'REMOTE IP':<18} {'ESTADO'}{RESET}")
    print("-" * 80)
    
    ips_vistas = set()

    try:
        while True:
            conexiones = psutil.net_connections(kind='inet')
            for conn in conexiones:
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    ip_remota = conn.raddr.ip
                    pid = conn.pid
                    
                    if ip_remota not in ips_vistas and ip_remota != "127.0.0.1":
                        try:
                            prog = psutil.Process(pid).name()
                        except:
                            prog = "Unknown"

                        # Imprime la línea de conexión encontrada
                        print(f"{VERDE}{pid:<8} {prog[:18]:<20} {ip_remota:<18} {conn.status}{RESET}")
                        
                        # Guardamos en vistas para no repetir en el scroll
                        ips_vistas.add(ip_remota)

            # Lógica de detección de teclado (Gatillo)
            if msvcrt.kbhit():
                tecla = msvcrt.getch().decode('utf-8').upper()
                if tecla == 'B':
                    target = input(f"\n{AMARILLO}[?] IP A BLOQUEAR: {RESET}")
                    if target:
                        bloquear_ip(target)
                        print(f"{VERDE}[+] Monitor reanudado...{RESET}\n")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n{ROJO}[!] Sentinel desactivado. Regresando al búnker.{RESET}")

if __name__ == "__main__":
    # Verificación de privilegios simple
    monitorear_red()