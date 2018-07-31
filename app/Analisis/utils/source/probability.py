#!/usr/bin/env python

import time
import json
import matplotlib.pyplot as plt
import numpy as np

class Probability(object):

    def __init__(self):
        self.patch_size = 9
        self.intersection = -1
        self.samples_n = -1

        self.trees_label = 'Trees'
        self.trees_mean = -1
        self.trees_std = -1
        self.trees_values = [] # grey values of sampled trees pixels
        self.trees_coords = [] # coords (x,y) of sampled trees pixels

        self.background_label = 'Background'
        self.background_mean = -1
        self.background_std = -1
        self.background_values = [] # grey values of sampled background pixels
        self.background_coords = []  # coords (x,y) of sampled background pixels

        self.loaded_config = False

    def readConfigFromFile(self, src_fname):
        with open(src_fname, 'r') as handle:
            parsed = json.load(handle)

        self.patch_size = parsed['general']['patch_size']
        self.intersection = parsed['general']['intersection']

        self.trees_values = parsed['trees']['values']
        self.trees_mean = parsed['trees']['mean']
        self.trees_std = parsed['trees']['std']

        self.background_values = parsed['background']['values']
        self.background_mean = parsed['background']['mean']
        self.background_std = parsed['background']['std']

        self.loaded_config = True

    def readConfigFromGUI(self, detection):
        # user GUI to take grey samples
        self.trees_coords, self.trees_values = self.getGrayscaleSamples(detection, self.trees_label)
        self.background_coords, self.background_values = self.getGrayscaleSamples(detection, self.background_label)

        # calculate mean/std
        self.trees_mean = np.mean(list(self.trees_values))
        self.trees_std = np.std(list(self.trees_values))
        self.background_mean = np.mean(list(self.background_values))
        self.background_std = np.std(list(self.background_values))

        # find grey value with same probability
        self.intersection = self.binarySearchOfGrayThreshold()

    def writeConfig(self, img_fname, dest_fname):
        # write probability information to a file
        if not self.loaded_config:
            data = {
                'general': {
                    'datetime': time.ctime(),
                    'image': img_fname,
                    'patch_size': self.patch_size,
                    'intersection': self.intersection
                },
                'trees': {
                    'mean': self.trees_mean, 'std': self.trees_std,
                    'samples_n': len(self.trees_values),
                    'coords': self.trees_coords,
                    'values': self.trees_values
                },
                'background': {
                    'mean': self.background_mean, 'std': self.background_std,
                    'samples_n': len(self.background_values),
                    'coords': self.background_coords,
                    'values': self.background_values
                }
            }
            with open(dest_fname, 'w') as file:
                json.dump(data, file, sort_keys = False, indent=4, ensure_ascii=False)

    def getGrayscaleSamples(self, detection, name):
        samples_n = self.samples_n
        patch_size = int(self.patch_size/2)
        # gray_sum = 0
        samples_coords = []
        gray_values = []
        plt.close()
        plt.axis('off')
        plt.subplots_adjust(bottom=0.01, top=0.9, left=0.01, right=1)
        plt.imshow(detection.img_Grayscale)
        msg = ('Please, select ' + str(samples_n) + ' samples of ' + name)
        plt.title(msg, fontsize=12)
        plt.draw()
        p = plt.ginput(samples_n, timeout=-1)

        for i in range(len(p)):
            min_x = int(p[i][0]) - patch_size
            max_x = int(p[i][0]) + patch_size + 1
            min_y = int(p[i][1]) - patch_size
            max_y = int(p[i][1]) + patch_size + 1
            for x in range(min_x, max_x):
                for y in range(min_y, max_y):
                    # store coordinates of sampled pixels
                    samples_coords.append((x, y))
                    # get the gray value of each sampled pixel
                    gray = detection.img_Grayscale.getpixel((x,y))[0]
                    gray_values.append(gray)
                    # gray_sum = gray_sum + gray

        return samples_coords, gray_values

    def binarySearchOfGrayThreshold(self):
        """
        Return the value of the range (mean_a, mean_b) with same
        probability P(A)=P(B).

        :return: value with the same probability for both categories (A and B)
        """
        mean_a = self.trees_mean
        std_a = self.trees_std
        mean_b = self.background_mean
        std_b = self.background_std

        left = mean_a
        right = mean_b
        stop = False

        while stop == False:
            middle = (left + right) / 2
            digits = 28
            # must be rounded to avoid an infinite loop
            p_a = round(self.computeProbability(middle, mean_a, std_a), digits)
            p_b = round(self.computeProbability(middle, mean_b, std_b), digits)

            if (p_a > p_b):
                # move to the right half
                left = middle
            elif (p_a < p_b):
                # move to the left half
                right = middle

            if p_a == p_b or left == right:
                stop = True
                return middle

    def computeProbability(self, x, mean, std):
        a = ((np.sqrt(2*np.pi))*std)
        b = (((x - mean)**2)/(2*std))
        prob = (1/a) * (np.exp(-1 * b))

        return prob
