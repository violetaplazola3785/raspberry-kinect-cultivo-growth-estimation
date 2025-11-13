# sensor_agent.py
# Agente que captura imágenes RGB y profundidad desde Kinect v1 usando freenect
# Calcula medidas básicas: altura promedio (cm), área proyectada (cm2) y volumen estimado (cm3)
from spade import agent, behaviour, message
import freenect
import numpy as np
import json

class SensorAgent(agent.Agent):
    class CaptureBehaviour(behaviour.PeriodicBehaviour):
        async def run(self):
            # Capturar mapa de profundidad desde Kinect
            depth, _ = freenect.sync_get_depth()
            depth = np.array(depth, dtype=np.float32)
            # Filtrar valores inválidos (0) y fuera de rango
            valid = depth[(depth > 0) & (depth < 2000)]
            if valid.size == 0:
                print("[SensorAgent] No se obtuvo profundidad válida")
                return

            # Altura aproximada en mm: diferencia entre fondo y partes cercanas
            fondo = np.percentile(depth, 98)   # valor de fondo (suelo / más lejano)
            planta = np.percentile(depth, 10)  # valor cercano (hojas)
            altura_mm = fondo - planta
            altura_cm = float(altura_mm) / 10.0

            # Area proyectada: píxeles más cercanos que el fondo-umbral
            mask = (depth < (fondo - 50)) & (depth > 0)
            area_px = int(np.count_nonzero(mask))
            # Factor de calibración por defecto (ajustar con regla en escena)
            cm_por_pixel = 0.25
            area_cm2 = area_px * (cm_por_pixel ** 2)

            volumen_cm3 = area_cm2 * altura_cm

            data = {"altura_cm": round(altura_cm,2),
                    "area_cm2": round(area_cm2,2),
                    "volumen_cm3": round(volumen_cm3,2),
                    "area_px": int(area_px)}
            # Enviar al AnalysisAgent
            msg = message.Message(to="analysis@localhost", body=json.dumps(data))
            await self.send(msg)
            print(f"[SensorAgent] Datos enviados: {data}")

    async def setup(self):
        print("SensorAgent iniciado")
        # Ejecutar cada 60 segundos (ajusta periodo según necesidad)
        self.add_behaviour(self.CaptureBehaviour(period=60))

if __name__ == '__main__':
    # Código de prueba local (sin XMPP) — captura una vez y muestra resultados
    depth, _ = freenect.sync_get_depth()
    import cv2
    import numpy as np
    depth = np.array(depth, dtype=np.float32)
    fondo = np.percentile(depth, 98)
    planta = np.percentile(depth, 10)
    altura_cm = (fondo - planta)/10.0
    mask = (depth < (fondo - 50)) & (depth > 0)
    area_px = int(np.count_nonzero(mask))
    cm_por_pixel = 0.25
    area_cm2 = area_px * (cm_por_pixel ** 2)
    volumen_cm3 = area_cm2 * altura_cm
    print({"altura_cm": altura_cm, "area_cm2": area_cm2, "volumen_cm3": volumen_cm3, "area_px": area_px})
