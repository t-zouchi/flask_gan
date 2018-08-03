import chainer
from chainer import serializers
from network import Generator

import numpy as np
from PIL import Image
import os

class PgganGenerator():

    def __init__(self, depth):
        self.depth = depth
        self.gen = Generator(self.depth)
        serializers.load_npz('./pg_gen.npz', self.gen)

    def __call__(self,num):
        previewdir = "./results/"

        for i in range(num):
            z = self.gen.z(1)
            x = self.gen(z, alpha=1.0)
            x = chainer.cuda.to_cpu(x.data)
                
            img = x[0].copy()
            filename = os.path.join(previewdir, 'gen_%04d.png'%i)
            self.save_image(img, filename)

    def save_image(self, img, filename):
        img = np.transpose(img, (1, 2, 0))
        img = img * 256
        img = img.astype(np.int32)
        img[img < 0] = 0
        img[img >= 256] = 255
        img = np.uint8(img)
        img = Image.fromarray(img)
        img = img.resize((640,640), Image.LANCZOS)
        img.save(filename)