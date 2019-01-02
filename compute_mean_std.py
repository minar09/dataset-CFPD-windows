import argparse
import json
import os
import numpy as np
from PIL import Image
from os import path as osp


def compute_mean_std():
    data_dir = 'E:/Dataset/CFPD/image/'
    image_list = os.listdir(data_dir)
    np.random.shuffle(image_list)
    pixels = []
    for image_path in image_list:
        image = Image.open(osp.join(data_dir, image_path), 'r')
        pixels.append(np.asarray(image).reshape(-1, 3))
    pixels = np.vstack(pixels)
    mean = np.mean(pixels, axis=0) / 255
    std = np.std(pixels, axis=0) / 255
    print(mean, std)
    info = {'mean': mean.tolist(), 'std': std.tolist()}
    with open('info.json', 'w') as fp:
        json.dump(info, fp)


def main():
    compute_mean_std()


if __name__ == '__main__':
    main()
