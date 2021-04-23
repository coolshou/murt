from murt import core, calculator
from murt.window import MurtWindow
from murt.utils import objreader

import numpy as np


class MurTracer():
    def __init__(self, scene_path=None):
        if scene_path is not None:
            vertices, triangles = objreader.read(scene_path)
            self.core = core.Tracer(vertices, triangles)
        else:
            self.core = None

    def loadTracer(self, vertices, triangles):
        if self.core is not None:
            del self.core
        self.core = core.Tracer(vertices, triangles)

    def isOutdoor(self, pos):
        pos = np.array(pos)
        assert pos.shape[0] == 3
        pos = np.array(pos).astype('float32')

        result = self.core.isOutdoor(pos)
        print(f'isoutdoor: {result}')
        return self.core.isOutdoor(pos) != 0

    def trace(self, txPos, rxPos):
        if self.core is None:
            return None
        txPos = np.array(txPos)
        rxPos = np.array(rxPos)
        assert rxPos.shape[0] == 3
        assert txPos.shape[0] == 3
        txPos = txPos.astype('float32')
        rxPos = rxPos.astype('float32')
        result = self.core.trace(txPos, rxPos)
        return result

    def ResultsToLines(self, results, txPos, rxPos):
        lines = []
        for result in results:
            line = None
            if result[0] == 1:
                line = {'points': [tuple(txPos), tuple(rxPos)],
                        'color': (0, 0.7, 0.3, 1)}
            if result[0] == 2:
                line = {'points': [tuple(txPos)], 'color': (0, 0, .9, 1)}
                for point in result[1]:
                    line['points'].append(tuple(point))
                line['points'].append(tuple(rxPos))
            if result[0] == 3:
                line = {'points': [tuple(txPos), tuple(result[1]), tuple(rxPos)],
                        'color': (0.7, 0.4, 0.7, 1)}
            # if result[0] == 4:
            #     dot = np.array(result[1]) + np.array([0, 0.2, 0])
            #     line = {'points': [tuple(result[1]), tuple(dot)],
            #             'color': (1, 0, 0, 1)}
            if line is not None:
                lines.append(line)
        return lines

    def TotalPathLoss(self, txPos, rxPos, results, txFreq=2.4e9, matPerm=5.31):
        losses = {'total_dB': None, 'signals': []}

        total_linear = 0
        loss_dB = None
        delay = 0
        if results is None:
            return None

        for result in results:
            if(result[0] == 1):
                loss_dB, delay = calculator.directLoss(txPos, rxPos, txFreq)

            elif(result[0] == 2):
                edges = list(map(list, result[1]))
                loss_dB, delay = calculator.diffractLoss(
                    txPos, rxPos, edges, txFreq)
            elif(result[0] == 3):
                refPos = list(result[1])
                loss_dB, delay = calculator.reflectLoss(txPos, rxPos,
                                                        refPos, txFreq,
                                                        matPerm)
            else:
                return None
            losses['signals'].append([loss_dB, delay])
            total_linear += np.power(10, -loss_dB/10)

        losses['total_dB'] = -10*np.log10(total_linear)
        return losses
