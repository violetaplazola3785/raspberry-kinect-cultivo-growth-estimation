# analysis_agent.py
# Agente que recibe medidas del SensorAgent y calcula indicadores de crecimiento y alertas simples
from spade import agent, behaviour
import json, pandas as pd, datetime

class AnalysisAgent(agent.Agent):
    class AnalyzeBehaviour(behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)  # espera hasta 10s por mensaje
            if msg:
                data = json.loads(msg.body)
                altura = data.get('altura_cm', 0)
                volumen = data.get('volumen_cm3', 0)
                estado = 'Desconocido'
                # Reglas simples — adapta según datos reales
                if altura < 20:
                    estado = 'Planta joven'
                elif altura < 40:
                    estado = 'Crecimiento'
                else:
                    estado = 'Madurez'
                # Preparar registro
                registro = {
                    'fecha_hora': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'altura_cm': altura,
                    'area_cm2': data.get('area_cm2',0),
                    'volumen_cm3': volumen,
                    'estado': estado
                }
                # Enviar al DataAgent
                msg2 = self.message_to('data@localhost', body=json.dumps(registro))
                await self.send(msg2)
                print(f"[AnalysisAgent] Analizado: {registro}")

    async def setup(self):
        print('AnalysisAgent iniciado')
        self.add_behaviour(self.AnalyzeBehaviour())

    def message_to(self, to, body=''):
        from spade.message import Message
        return Message(to=to, body=body)

if __name__ == '__main__':
    # Prueba local
    sample = {'altura_cm': 25, 'area_cm2': 500, 'volumen_cm3': 12500}
    print('Simulación AnalysisAgent => Estado:', 'Crecimiento' if sample['altura_cm']>20 else 'Planta joven')
