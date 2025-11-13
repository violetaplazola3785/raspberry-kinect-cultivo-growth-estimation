# control_agent.py
# Agente que recibe comandos de control y acciona un relé vía GPIO (Raspberry Pi)
from spade import agent, behaviour
import json, time

# Intentamos importar RPi.GPIO pero mantenemos simulación si no está presente
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    RELAY_PIN = 17
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    GPIO_AVAILABLE = True
except Exception as e:
    print('[ControlAgent] RPi.GPIO no disponible, funcionando en modo simulación. Error:', e)
    GPIO_AVAILABLE = False

class ControlAgent(agent.Agent):
    class ControlBehaviour(behaviour.CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                cmd = json.loads(msg.body)
                accion = cmd.get('accion','none')
                if accion == 'activar_riego':
                    if GPIO_AVAILABLE:
                        GPIO.output(RELAY_PIN, GPIO.HIGH)
                        time.sleep(2)  # activar por 2 segundos (ejemplo)
                        GPIO.output(RELAY_PIN, GPIO.LOW)
                        print('[ControlAgent] Riego activado (GPIO)')
                    else:
                        print('[ControlAgent] Simulación: Riego activado (no hay GPIO)')
                elif accion == 'apagar_riego':
                    if GPIO_AVAILABLE:
                        GPIO.output(RELAY_PIN, GPIO.LOW)
                        print('[ControlAgent] Riego apagado (GPIO)')
                    else:
                        print('[ControlAgent] Simulación: Riego apagado (no hay GPIO)')

    async def setup(self):
        print('ControlAgent iniciado')
        self.add_behaviour(self.ControlBehaviour())

if __name__ == '__main__':
    # Simula un comando
    cmd = {'accion':'activar_riego'}
    print('Simulación control -> activar_riego') 
