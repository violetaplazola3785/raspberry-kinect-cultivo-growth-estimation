# data_agent.py
# Agente que recibe registros procesados y los almacena en CSV
from spade import agent, behaviour
import json, pandas as pd, os

class DataAgent(agent.Agent):
    class StoreBehaviour(behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                registro = json.loads(msg.body)
                carpeta = os.path.join(os.getcwd(), 'data')
                os.makedirs(carpeta, exist_ok=True)
                path = os.path.join(carpeta, 'resultados.csv')
                df = pd.DataFrame([registro])
                if not os.path.exists(path):
                    df.to_csv(path, index=False)
                else:
                    df.to_csv(path, mode='a', header=False, index=False)
                print(f"[DataAgent] Registro guardado: {registro['fecha_hora']}")

    async def setup(self):
        print('DataAgent iniciado')
        self.add_behaviour(self.StoreBehaviour())

if __name__ == '__main__':
    # Prueba simple
    registro = {'fecha_hora':'2025-01-01 10:00:00','altura_cm':30,'area_cm2':450,'volumen_cm3':13500,'estado':'Crecimiento'}
    import pandas as pd, os
    carpeta = os.path.join(os.getcwd(), 'data'); os.makedirs(carpeta, exist_ok=True)
    pd.DataFrame([registro]).to_csv(os.path.join(carpeta,'resultados.csv'), index=False)
    print('Archivo ejemplo creado en /data/resultados.csv')
