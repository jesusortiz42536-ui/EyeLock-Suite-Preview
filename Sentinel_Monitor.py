import psutil
import time
import os
import subprocess

# --- CONFIGURACIÓN DE PODER ---
LOG_FILE = "sentinel_firewall.log"
VERDE = "\033[92m"
ROJO = "\033[91m"
CYAN = "\033[96m"
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
    print(f"{CYAN}    [ SENTINEL v3.0 - FIREWALL ACTIVE DEFENSE / BY DR. ENCRYPT ]{RESET}\n")

def bloquear_ip(ip):
    """Ejecuta el comando de Windows Firewall para banear la IP"""
    nombre_regla = f"KIMAD_BLOCK_{ip}"
    comando = f'netsh advfirewall firewall add rule name="{nombre_regla}" dir=in action=block remoteip={ip}'
    
    try:
        subprocess.run(comando, shell=True, check=True, stdout=subprocess.DEVNULL)
        alerta = f"[🔒 BLOQUEADO] IP {ip} ha sido expulsada por KIMAD Sentinel."
        print(f"{ROJO}{alerta}{RESET}")
        with open(LOG_FILE, "a") as f:
            f.write(f"{time.ctime()} - {alerta}\n")
    except Exception as e:
        print(f"{ROJO}[!] Error al bloquear (¿Eres Administrador?): {e}{RESET}")

def monitorear_red():
    banner()
    print(f"{CYAN}{'PID':<8} {'PROGRAMA':<20} {'REMOTE IP':<18} {'ACCION'}{RESET}")
    print("-" * 75)
    
    ips_vistas = set()

    try:
        while True:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    ip_remota = conn.raddr.ip
                    pid = conn.pid
                    
                    try:
                        prog = psutil.Process(pid).name()
                    except:
                        prog = "Unknown"

                    # Si es una IP nueva, preguntamos si queremos bloquearla
                    if ip_remota not in ips_vistas and ip_remota != "127.0.0.1":
                        print(f"{VERDE}{pid:<8} {prog[:18]:<20} {ip_remota:<18} [Enter p/ Ignorar | B p/ Bloquear]{RESET}")
                        
                        # Pequeño truco para decidir rápido (puedes mejorar esto con inputs)
                        ips_vistas.add(ip_remota)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print(f"\n{ROJO}[!] Sentinel Offline.{RESET}")

if __name__ == "__main__":
    monitorear_red()