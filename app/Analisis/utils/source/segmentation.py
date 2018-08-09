#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import settings as config
from matplotlib.colors import LinearSegmentedColormap
from probability import Probability

class Segmentation(object):

    def __init__(self):
        prob = Probability()
        self.prob = prob

    def globalOtsu(self, detection, img):
        """
        :param detection: Detection class object
        :return: binary segmented image

        Computes Global Otsu method for the given grayscale image
        """
        from skimage import filters
        # img = numpy.array(detection.img_Grayscale.convert("L"))
        # img = detection.img_VARI
        val = filters.threshold_otsu(img)
        # grey_range = 25
        # TODO: this value needs to be configurable
        security_band = 0
        val = val - security_band
        mask = img < val
        # print('val', val)

        width = detection.img_width
        height = detection.img_height

        img_binary = np.array(mask).reshape(height, width)
        if not config.compute_VARI:
            # needs to be inverted to work with grayscale image
            img_binary = np.logical_not(img_binary)
        img_binary = img_binary.astype('uint8')

        # save binary image
        if config.getDebugMode() == 2:
            binary_fname = config.getBinaryGlobalOtsuPath(config.getImageFilename())
            mycmap = LinearSegmentedColormap.from_list('mycmap', ['white', 'black'])
            plt.imsave(binary_fname, img_binary, cmap=mycmap)

        # Normalisation
        min = np.min(img_binary)
        max = np.max(img_binary)
        new_max = 255
        new_min = 0
        # invert values of matrix (replace 1 with 0 and vice versa)
        img_binary = np.logical_not(img_binary)
        norm_img_binary = (img_binary - min) * (new_max-new_min /max-min) + new_min
        norm_img_binary = np.array(norm_img_binary).astype('uint8')

        return norm_img_binary


    def computeLocalOtsu(self, detection, img):
        """
        :param detection: Detection class object
        :return: binary segmented image

        Computes Local Otsu method for the given grayscale image
        """

        from skimage.morphology import disk
        from skimage.filters import rank

        radius = 150
        selem = disk(radius)

        local_otsu = rank.otsu(img, selem)
        # TODO: this value needs to be configurable
        security_band = 0
        local_otsu = local_otsu - security_band
        img = img < local_otsu

        width = detection.img_width
        height = detection.img_height

        img_binary = np.array(img).reshape(height, width)
        if not config.compute_VARI:
            # needs to be inverted to work with grayscale image
            img_binary = np.logical_not(img_binary)
        img_binary = img_binary.astype('uint8')

        # save binary image
        if config.getDebugMode() == 2:
            binary_fname = config.getBinaryLocalOtsuPath(config.getImageFilename())
            if config.compute_VARI:
                mycmap = LinearSegmentedColormap.from_list('mycmap', ['white', 'black'])
            else:
                mycmap = LinearSegmentedColormap.from_list('mycmap', ['black', 'white'])
            plt.imsave(binary_fname, img, cmap=mycmap)

        # Normalisation
        min = np.min(img_binary)
        max = np.max(img_binary)
        new_max = 255
        new_min = 0
        # invert values of matrix (replace 1 with 0 and vice versa)
        norm_img_binary = np.logical_not(img_binary)
        norm_img_binary = (norm_img_binary - min) * (new_max-new_min /max-min) + new_min
        norm_img_binary = np.array(norm_img_binary).astype('uint8')

        return norm_img_binary


    def initProbabilityConfig(self, detection):
        """
        :param detection: Detection class object

        Initializes the probability configuration from config file or GUI
        """
        try:
            # try to read configuration file
            # TODO: config file should be a parameter
            file = config.getConfigFilename()
            self.prob.readConfigFromFile(file)
            print('Parameters loaded from file:', file)

        except:
            # user GUI to take grey samples
            print('Patch size:', self.prob.patch_size, 'x', self.prob.patch_size)
            self.prob.readConfigFromGUI(detection)

        print('\nTrees: mean=', self.prob.trees_mean, 'std=', self.prob.trees_std)
        print('Background: mean=', self.prob.background_mean, 'std=', self.prob.background_std)
        print('Intersection=', self.prob.intersection)


    def generateHistogram(self):
        plt.close()
        prob = self.prob
        bins = np.linspace(0, 255, num=255)
        plt.hist(prob.trees_values, facecolor='green', label=prob.trees_label, bins=bins, normed=True)
        # plt.hist(mean_a, facecolor='red', bins=bins)
        plt.hist(prob.background_values, facecolor='blue', label=prob.background_label, bins=bins, normed=True)
        # plt.hist(mean_b, facecolor='red', bins=bins)
        plt.legend()

        # add Gaussian bells
        trees_gaussian = mlab.normpdf(bins, prob.trees_mean, prob.trees_std)
        plt.plot(bins, trees_gaussian, 'r--')
        bground_gaussian = mlab.normpdf(bins, prob.background_mean, prob.background_std)
        plt.plot(bins, bground_gaussian, 'r--')

        # add an arrow marking the point with same probability
        plt.annotate("", xy=(prob.intersection, 0.01), xycoords='data',
                    xytext=(prob.intersection, 0.03), textcoords='data',
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),)

        plt.title("Histogram")
        plt.ylabel("Pixels")
        plt.xlabel("Gray value")

        if config.getDebugMode() == 2:
            plt.savefig(config.getHistogramPath(config.getImageFilename()))
            # plt.show()

    def automaticGrayscaleSegmentation(self, detection):
        # define a 'grey range' where the values are considered as unknown
        grey_range = np.abs(self.prob.background_mean - self.prob.trees_mean) * 0.2
        lower_limit = self.prob.intersection - grey_range
        upper_limit = self.prob.intersection + grey_range

        # print(intersection)
        # print('t', computeProbability(intersection, trees_mean, trees_std))
        # print('bg', computeProbability(intersection, bground_mean, bground_std))
        # show the grey zone on the histogram
        # plt.hist([lower_limit, upper_limit], facecolor='red', bins=bins)

        # generation of binary image
        # on binary image:
        #   trees=0 (white)
        #   background=255 (white)
        #   unknown=255 (white) (to avoid false-positives)
        width = detection.img_width
        height = detection.img_height
        img_binary = []
        probs = {}
        tree = 255
        unknown = 128
        background = 0

        for y in range(height):
            for x in range(width):
                value = detection.img_Grayscale.getpixel((x, y))[0]
                if value in probs:
                    img_binary.append(probs[value])
                elif value >= lower_limit and value <= upper_limit:
                    # value is in the grey range
                    img_binary.append(unknown)
                    probs[value] = unknown
                else:
                    prob_t = self.prob.computeProbability(value, self.prob.trees_mean, self.prob.trees_std)
                    prob_b = self.prob.computeProbability(value, self.prob.background_mean, self.prob.background_std)
                    if prob_t > prob_b:
                        # if tree
                        img_binary.append(tree)
                        probs[value] = tree
                    else:
                        # if background
                        img_binary.append(background)
                        probs[value] = background

        img_binary = np.array(img_binary).reshape(height, width)
        img_binary = img_binary.astype('uint8')

        # return a matrix with 2 values only (replace 128 with 0)
        # for a in range(len(img_binary)):
        #     for b in range(len(img_binary[0])):
        #         if img_binary[a][b] == unknown:
        #             img_binary[a][b] = background
        img_binary[img_binary == 128] = 0

        # save binary image
        if config.getDebugMode() == 2:
            binary_fname = config.getBinaryPath(config.getImageFilename())
            mycmap = LinearSegmentedColormap.from_list('mycmap', ['black', 'red', 'white'])
            plt.imsave(binary_fname, img_binary, cmap=mycmap)


        return img_binary

    def computeVARI(self, detection):
        """
        :param detection: Detection class object
        :return: matrix of VARI values of the image

        Computes the VARI (Visible Atmospheric Resistant Index) of a RGB image

        """

        width = detection.img_width
        height = detection.img_height
        img_VARI = []

        for y in range(height):
            for x in range(width):
                R, G, B = detection.img_RGB.getpixel((x, y))
                divisor = G+R-B
                # TODO: this case must be improved
                if divisor == 0:
                    divisor = 1
                    # print('***', G-R)
                VARI_value = (G-R) / divisor

                img_VARI.append(VARI_value)

        # Normalisation
        min = np.min(img_VARI)
        max = np.max(img_VARI)
        new_max = 255
        new_min = 0
        norm_img_VARI = (img_VARI - min) * (new_max-new_min /max-min) + new_min
        norm_img_VARI = np.array(norm_img_VARI).astype('uint8')
        # change the shape of the matrix to display the image correctly
        img_VARI = np.array(norm_img_VARI).reshape(height, width)

        # save VARI image
        if config.getDebugMode() == 2:
            VARI_fname = config.getVARIPath()
            # mycmap = LinearSegmentedColormap.from_list('mycmap', ['black', 'red', 'white'])
            plt.imsave(VARI_fname, img_VARI, cmap='hot')

        return img_VARI

    def computeMultiprocessVARI(self, detection):
        """
        :param detection: Detection class object
        :return: matrix of VARI values of the image

        Computes the VARI (Visible Atmospheric Resistant Index) of a RGB image
        using multiprocessing

        """

        width = detection.img_width
        height = detection.img_height
        img_VARI = []

        self.img = np.asarray(detection.img_RGB)

        import multiprocessing

        num_cores = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(num_cores)
        img_VARI = pool.map(self.computeRowVARI, range(0, height))

        # Normalisation
        min = np.min(img_VARI)
        max = np.max(img_VARI)
        new_max = 255
        new_min = 0
        norm_img_VARI = (img_VARI - min) * (new_max-new_min /max-min) + new_min
        norm_img_VARI = np.array(norm_img_VARI).astype('uint8')
        # change the shape of the matrix to display the image correctly
        img_VARI = np.array(norm_img_VARI).reshape(height, width)

        # save VARI image
        if config.getDebugMode() == 2:
            VARI_fname = config.getVARIPath()
            # mycmap = LinearSegmentedColormap.from_list('mycmap', ['black', 'red', 'white'])
            plt.imsave(VARI_fname, img_VARI, cmap='hot')

        return img_VARI

    def computeRowVARI(self, i):
        """
        :param i: row of an RGB image
        :return: row with computed VARI values
        Computes the VARI descriptor for the given row
        """
        img_row = self.img[i]
        img_row_VARI = []
        for x in img_row:
            R = int(x[0])
            G = int(x[1])
            B = int(x[2])
            divisor = G + R - B
            # TODO: this case must be improved
            if divisor == 0:
                divisor = 1
                # print('***', G-R)
            VARI_value = (G - R) / divisor

            img_row_VARI.append(VARI_value)


        return img_row_VARI


    def writeProbabilityConfig(self, img_fname, dest_fname):
        self.prob.writeConfig(img_fname, dest_fname)