import chainer
from chainer import serializers
from net import Discriminator
from net import Generator

from chainer import Variable

import numpy as np
from PIL import Image

import os

class ImageGenerator():

    def __init__(self, n_hidden):
        self.n_hidden = n_hidden
        self.gen = Generator(self.n_hidden)
        chainer.serializers.load_npz('./gen_iter_41200.npz', self.gen)


    def __call__(self):
        rows = 10
        cols = 10
        previewdir = "./results/"

        z = Variable(np.asarray(self.gen.make_hidden(rows * cols)))

        x = self.gen(z)

        x = chainer.cuda.to_cpu(x.data)

        x = np.asarray(np.clip(x * 255, 0.0, 255.0), dtype=np.uint8)
        _, _, H, W = x.shape
        x = x.reshape((rows, cols, 3, H, W))
        x = x.transpose(0, 1, 3, 4, 2)

        for i in range(rows):
            for j in range(cols):
                pilimg = Image.fromarray(x[i][j])
                resize_img = pilimg.resize((640,640), Image.LANCZOS)
                previewpath = previewdir + "{0}{1}instabae.png".format(i,j)
                resize_img.save(previewpath)
                j = j + 1
            i = i + 1
