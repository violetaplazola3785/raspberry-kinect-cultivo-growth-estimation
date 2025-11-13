# main.py
# Lanzador de agentes: SensorAgent, AnalysisAgent, DataAgent y ControlAgent
# Atención: requiere un servidor XMPP (puedes usar Prosody en la misma Raspberry Pi)
from spade import agent
import asyncio, time, os

# Importar clases desde archivos locales
from sensor_agent import SensorAgent
from analysis_agent import AnalysisAgent
from data_agent import DataAgent
from control_agent import ControlAgent

async def main():
    # Usuario@dominio — requiere servidor XMPP configurado o usar localhost con prosody
    sensor = SensorAgent('sensor@localhost', 'password')
    analysis = AnalysisAgent('analysis@localhost', 'password')
    data = DataAgent('data@localhost', 'password')
    control = ControlAgent('control@localhost', 'password')

    await sensor.start(auto_register=True)
    await analysis.start(auto_register=True)
    await data.start(auto_register=True)
    await control.start(auto_register=True)

    print('Todos los agentes iniciados. Presiona Ctrl+C para detener.')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Deteniendo agentes...')
        await sensor.stop()
        await analysis.stop()
        await data.stop()
        await control.stop()

if __name__ == '__main__':
    asyncio.run(main())
