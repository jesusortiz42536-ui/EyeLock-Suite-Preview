import psutil
import time
import os

# --- CONFIGURACIÓN DE SEGURIDAD KIMAD ---
# Agrega aquí IPs que te parezcan sospechosas para que Sentinel las resalte
IP_BANEADAS = ["192.168.1.100", "45.33.22.11"] 
LOG_FILE = "sentinel_alerts.log"

def banner():
    print(r"""
    ######################################################
    #          🛡️  KIMAD SENTINEL - ACTIVE DEFENSE        #
    #            Monitoring Network Connections          #
    ######################################################
    """)

def monitorear_red():
    banner()
    print(f"[*] Iniciando monitoreo en PC Master...")
    print(f"[*] Guardando logs en: {LOG_FILE}\n")
    print(f"{'PROTO':<7} {'LOCAL ADDR':<25} {'REMOTE ADDR':<25} {'STATUS'}")
    print("-" * 75)
    
    try:
        while True:
            conexiones = psutil.net_connections()
            for conn in conexiones:
                # Solo queremos ver conexiones activas (ESTABLISHED)
                if conn.status == 'ESTABLISHED':
                    l_addr = f"{conn.laddr.ip}:{conn.laddr.port}"
                    r_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    
                    # Verificamos si la IP remota está en la lista negra
                    remote_ip = conn.raddr.ip if conn.raddr else ""
                    if remote_ip in IP_BANEADAS:
                        print(f"[⚠️ PELIGRO] IP Bloqueada detectada: {r_addr}")
                        with open(LOG_FILE, "a") as f:
                            f.write(f"{time.ctime()} - ALERTA: {r_addr} intentó conectar.\n")
                    else:
                        print(f"{'TCP':<7} {l_addr:<25} {r_addr:<25} {conn.status}")
            
            time.sleep(5) # Escaneo cada 5 segundos para no saturar el CPU
            
    except KeyboardInterrupt:
        print("\n[!] Sentinel desactivado por el usuario. Cerrando búnker.")

if __name__ == "__main__":
    monitorear_red()