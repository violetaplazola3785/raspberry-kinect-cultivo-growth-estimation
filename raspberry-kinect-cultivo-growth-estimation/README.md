# 🌱 Estimación del Crecimiento de Cultivos con Raspberry Pi 4 y Kinect V1
Repositorio para la medición de crecimiento (altura, área proyectada y volumen estimado)
de pimiento morrón en invernadero usando Raspberry Pi 4 + Kinect V1.

## Estructura
- `src/` : Código fuente con agentes en español (SensorAgent, AnalysisAgent, DataAgent, ControlAgent)
- `data/`: Carpeta de ejemplo para datos y CSV generados
- `docs/`: Documentación y diagramas (arquitectura)
- `tests/`: Pruebas básicas

## Requisitos
Instala los paquetes listados en `requirements.txt` (recomendado usar entorno virtual).
Requiere Python 3.8+ y Raspberry Pi OS en la Pi.

## Uso rápido
1. Clona el repositorio en la Raspberry Pi.
2. Instala dependencias: `pip install -r requirements.txt`
3. Conecta Kinect y, si usas actuadores, conecta relé al GPIO (ver `src/control_agent.py`).
4. Ejecuta: `python3 src/main.py`

---
Licencia MIT.
