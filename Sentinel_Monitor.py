import psutil
import time
import os
import subprocess
import msvcrt

# --- CONFIGURACIÓN DE PODER KIMAD TECH ---
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
    print(f"{CYAN}    [ SENTINEL v3.2 - FORCE ADMIN & DEBUG / BY DR. ENCRYPT ]{RESET}\n")

def bloquear_ip(ip):
    """Ejecuta el comando de Firewall con reporte de error detallado."""
    tag = ip.replace('.', '_')
    nombre_rule = f"KIMAD_SENTINEL_{tag}"
    comando = f'netsh advfirewall firewall add rule name="{nombre_rule}" dir=in action=block remoteip={ip}'
    
    print(f"\n{AMARILLO}[*] Intentando levantar muro en Firewall...{RESET}")
    
    try:
        # Ejecutamos y capturamos la respuesta de Windows
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            print(f"{ROJO}[🔒 ÉXITO] IP {ip} desterrada permanentemente.{RESET}")
            with open(LOG_FILE, "a") as f:
                f.write(f"{time.ctime()} - BLOQUEO EXITOSO: {ip}\n")
        else:
            # Si Windows dice que no, mostramos el por qué exacto
            print(f"{ROJO}[!] ERROR DE WINDOWS: {resultado.stdout.strip()}{RESET}")
            
    except Exception as e:
        print(f"{ROJO}[!] ERROR CRÍTICO DEL SCRIPT: {e}{RESET}")

def monitorear_red():
    banner()
    print(f"{AMARILLO}[*] Escaneo táctico iniciado. Presiona 'B' para abrir el Gatillo de Bloqueo.{RESET}")
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

                        print(f"{VERDE}{pid:<8} {prog[:18]:<20} {ip_remota:<18} {conn.status}{RESET}")
                        ips_vistas.add(ip_remota)

            # Detector de teclado para el bloqueo
            if msvcrt.kbhit():
                tecla = msvcrt.getch().decode('utf-8').upper()
                if tecla == 'B':
                    target = input(f"\n{AMARILLO}[❓] IP OBJETIVO PARA BLOQUEO: {RESET}")
                    if target:
                        bloquear_ip(target)
                        print(f"{VERDE}[+] Monitor reanudado...{RESET}\n")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n{ROJO}[!] Sentinel desactivado. Regresando al búnker.{RESET}")

if __name__ == "__main__":
    monitorear_red()