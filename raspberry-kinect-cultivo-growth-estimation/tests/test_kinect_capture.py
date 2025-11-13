# tests/test_kinect_capture.py
# Prueba simple para verificar que el Kinect responde y devuelve un mapa de profundidad
import freenect, numpy as np
depth,_ = freenect.sync_get_depth()
depth = np.array(depth, dtype=np.float32)
print('Profundidad mínima:', depth[depth>0].min(), 'máxima:', depth.max())
assert depth.max() > 0
print('Prueba Kinect: OK')
