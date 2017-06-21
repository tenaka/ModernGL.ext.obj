'''
    ModernGL extension for loading obj files
'''

import logging
import re
import struct

log = logging.getLogger('ModernGL.ext.obj')

RE_COMMENT = re.compile(r'#[^\n]*\n', flags=re.M)
RE_VERT = re.compile(r'^v\s+(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)$')
RE_TEXT = re.compile(r'^vt\s+(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)(\s+(-?\d+(\.\d+)?))?$')
RE_NORM = re.compile(r'^vn\s+(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)\s+(-?\d+(\.\d+)?)$')
RE_FACE = re.compile(r'^f\s+(\d+)(/(\d+)?(/(\d+))?)?\s+(\d+)(/(\d+)?(/(\d+))?)?\s+(\d+)(/(\d+)?(/(\d+))?)?$')

PACKER = 'lambda i, face, vx, vy, vz, tx, ty, tz, nx, ny, nz: struct.pack("%df", %s)'

INT_OR_NONE = lambda x: None if x is None else int(x)
SAFE_FLOAT = lambda x: 0.0 if x is None else float(x)

class Obj:
    '''
        Obj class
    '''

    @staticmethod
    def open(filename):
        return Obj.fromstring(open(filename).read())

    @staticmethod
    def frombytes(data):
        return Obj.fromstring(data.decode())

    @staticmethod
    def fromstring(data):

        vert = []
        text = []
        norm = []
        face = []

        data = RE_COMMENT.sub('\n', data)

        for line in data.splitlines():
            if not line:
                continue

            match = RE_VERT.match(line)

            if match:
                vert.append(tuple(map(SAFE_FLOAT, match.group(1, 3, 5))))
                continue

            match = RE_TEXT.match(line)

            if match:
                text.append(tuple(map(SAFE_FLOAT, match.group(1, 3, 6))))
                continue

            match = RE_NORM.match(line)

            if match:
                norm.append(tuple(map(SAFE_FLOAT, match.group(1, 3, 5))))
                continue

            match = RE_FACE.match(line)

            if match:
                v, t, n = match.group(1, 3, 5)
                face.append((int(v), INT_OR_NONE(t), INT_OR_NONE(n)))
                v, t, n = match.group(6, 8, 10)
                face.append((int(v), INT_OR_NONE(t), INT_OR_NONE(n)))
                v, t, n = match.group(11, 13, 15)
                face.append((int(v), INT_OR_NONE(t), INT_OR_NONE(n)))
                continue

            log.debug('unknown line "%s"', line)

        if not face:
            raise Exception('empty')

        v0, t0, n0 = face[0]

        for v, t, n in face:
            if (t0 is None) ^ (t is None):
                raise Exception('inconsinstent')

            if (n0 is None) ^ (n is None):
                raise Exception('inconsinstent')

        return Obj(vert, text, norm, face)

    def __init__(self, vert, text, norm, face):
        self.vert = vert
        self.text = text
        self.norm = norm
        self.face = face

    def pack(self, mode):
        mode = mode.split()

        zero = 0.0
        one = 1.0

        result = bytearray()
        packer = eval(PACKER % (len(mode), ', '.join(mode)))

        for i, (v, t, n) in enumerate(self.face):
            face = i // 3

            vx, vy, vz = self.vert[v - 1]
            tx, ty, tz = self.text[t - 1] if t is not None else (0.0, 0.0, 0.0)
            nx, ny, nz = self.norm[n - 1] if n is not None else (0.0, 0.0, 0.0)

            result += packer(i, face, vx, vy, vz, tx, ty, tz, nx, ny, nz)

        return bytes(result)

