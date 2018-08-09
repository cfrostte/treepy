import logging
import time, datetime

# initializes the configuration settings
def initConfig():
    # debug mode:
    #   0 = do nothing, just process
    #   1 = show results
    #   2 = save results
    global DEBUG_MODE
    DEBUG_MODE = 0

    # folder to read images from
    global images_folder
    images_folder = "fotos_dron"

    # exclusion margin (in percentage) from the border of the image
    global exclusion_margin
    exclusion_margin = 3

    # minimal area to consider detected regions (in pixels)
    global min_area_size
    min_area_size = 400

    # image formats supported
    global supp_formats
    supp_formats = ('jpg', 'png')

    # file extension to save results as
    global results_format
    results_format = '.png'

    # name of the results folder
    global results_folder
    results_folder = 'results'

    # suffix to save binary results
    global binary_suffix
    binary_suffix = '_binary'

    # suffix to save Global Otsu's method results
    global global_otsu_suffix
    global_otsu_suffix = '_global_otsu'

    # suffix to save Local Otsu's method results
    global local_otsu_suffix
    local_otsu_suffix = '_local_otsu'

    # suffix to save VARI segmentation results
    global vari_suffix
    vari_suffix = '_vari'

    # suffix to save labeling results
    global labeling_suffix
    labeling_suffix = '_labeling'

    # suffix to save closing results
    global closing_suffix
    closing_suffix = '_closing'

    # suffix to save histogram
    global histogram_suffix
    histogram_suffix = '_histogram'

    # threshold (RGB)
    global RGB_threshold
    RGB_threshold = [(0, 51), (0, 255), (80, 255)]

    # threshold for distance between nodes
    global distance_threshold
    distance_threshold = 50

    # resize image (0 to 1.0, means 0% to 100% of original size)
    global resize
    resize = 1.0

    global report_filename
    report_filename = 'info_subgraph'

    global report_extension
    report_extension = '.txt'

    global image_filename

    global subplot_size
    subplot_size = ()

    global arr_overlay

    global config_filename
    config_filename = 'probability_data.json'

    global use_autocontrast
    use_autocontrast = True

    global use_automatic_segm_threshold
    use_automatic_segm_threshold = False

    global use_polynomial_regression
    use_polynomial_regression = False

    # segmentation algorithm
    global algorithm
    algorithm = 1

    # VARI descriptor for segmentation
    global compute_VARI
    compute_VARI = False

    # enable multiprocessing to compute VARI
    global multiprocess_VARI
    multiprocess_VARI = True

# initializes log file and prints header
def initLog(log_name):
    global st_time
    st_time = datetime.datetime.now()
    logging.basicConfig(filename=log_name + '.log', filemode='w', level=logging.DEBUG)
    logging.info("CURRENT SETTINGS")
    logging.info("Current folder: " + images_folder)
    logging.info("Results folder: %s", results_folder)
    logging.info("Debug mode: %d", DEBUG_MODE)
    logging.info("Supported formats: " + str(supp_formats))
    logging.info("Resize (%): " + str(resize*100))
    logging.info("Exclusion margin (%): " + str(exclusion_margin))
    logging.info("Minimal area size (px): %d", min_area_size)
    logging.info("Binary results path: " + getBinaryPath('*'))
    logging.info("Labeling results path: " + getLabelingPath('*'))
    logging.info("---------------------------------")
    logging.info("Started at: " + str(st_time))
    logging.info("---------------------------------")

# prints info and results for each processed object
def printObjInfoToLog(obj):
    logging.info(" File name: " + obj.getFileName() )
    logging.info("    Width (px): " + str(obj.getImageWidth()) )
    logging.info("    Height (px): " + str(obj.getImageHeight()) )
    logging.info("    Regions detected: " + str(obj.getRegionsN()) )
    logging.info("    Regions areas (px): " + str(obj.getRegionsArea()) )
    logging.info("    SCORE (0 to 1.0): " + str(obj.getScore()) )
    logging.info("---------------------------------")

# prints results for a list of objects
def printListInfoToLog(obj_list):
    logging.info("Images processed: " + str(len(obj_list)))

# closes the log file and prints footer
def closeLog():
    fn_time = datetime.datetime.now()
    logging.info("Finished at: " + str(fn_time))
    tot_time = fn_time - st_time
    logging.info("Total time: " + str(tot_time))


# BASIC SETs/GETs METHODS
def setDebugMode(var):
    global DEBUG_MODE
    DEBUG_MODE = var

def getDebugMode():
    return DEBUG_MODE
# -------------------------------------------------
def setSourceFolderName(var):
    global images_folder
    images_folder = var

def getSourceFolderName():
    return images_folder
# -------------------------------------------------
def setExclusionMargin(var):
    global exclusion_margin
    exclusion_margin = var

def getExclusionMargin():
    return exclusion_margin
# -------------------------------------------------
def setMinAreaSize(var):
    global min_area_size
    min_area_size = var

def getMinAreaSize():
    return min_area_size
# -------------------------------------------------
def setSupportedFormats(var):
    global supp_formats
    supp_formats = var

def getSupportedFormats():
    return supp_formats
# -------------------------------------------------
def setResultsFormats(var):
    global results_format
    results_format = "." + var

def getResultsExtension():
    return results_format
# -------------------------------------------------
def setResultsFolderName(var):
    global results_folder
    results_folder = var

def getResultsFolderName():
    return results_folder
# -------------------------------------------------
def setBinarySuffix(var):
    global binary_suffix
    binary_suffix = var

def getBinarySuffix():
    return binary_suffix
# -------------------------------------------------
def setGlobalOtsuSuffix(var):
    global global_otsu_suffix
    global_otsu_suffix = var

def getGlobalOtsuSuffix():
    return global_otsu_suffix
# -------------------------------------------------
def setLocalOtsuSuffix(var):
    global local_otsu_suffix
    local_otsu_suffix = var

def getLocalOtsuSuffix():
    return local_otsu_suffix
# -------------------------------------------------
def setVARISuffix(var):
    global vari_suffix
    vari_suffix = var

def getVARISuffix():
    return vari_suffix
# -------------------------------------------------
def setHistogramSuffix(var):
    global histogram_suffix
    histogram_suffix = var

def getHistogramSuffix():
    return histogram_suffix
# -------------------------------------------------
def setLabelingSuffix(var):
    global labeling_suffix
    labeling_suffix = var

def getLabelingSuffix():
    return labeling_suffix
# -------------------------------------------------
def setClosingSuffix(var):
    global binary_suffix
    closing_suffix = var

def getClosingSuffix():
    return closing_suffix
# -------------------------------------------------
def setRGBThreshold(var):
    global RGB_threshold
    RGB_threshold = var

def getRGBThreshold():
    return RGB_threshold
# -------------------------------------------------
def setDistanceThreshold(var):
    global distance_threshold
    distance_threshold = var

def getDistanceThreshold():
    return distance_threshold

def setDistanceInNodes(var):
    global distance_node
    distance_node = var
    
def getDistanceInNodes():
    return distance_node
# -------------------------------------------------
def setResize(var):
    global resize
    resize = var

def getResize():
    return resize
# -------------------------------------------------
def getReportFilename():
    return report_filename
# -------------------------------------------------
def getReportExtension():
    return report_extension
# -------------------------------------------------
def setImageFilename(file):
    global image_filename
    image_filename = file

def getImageFilename():
    return image_filename
# -------------------------------------------------
def setConfigFilename(file):
    global config_filename
    config_filename = file

def getConfigFilename():
    return config_filename
# -------------------------------------------------

# OTHER METHODS
# returns relative path to an original image
def getImagePath(image_name):
    image_path = images_folder + '/' + image_name
    return image_path

# returns relative path of folder to save binary images
def getBinaryFolderPath():
    return getResultsPath()

# returns relative path to save binary images
def getBinaryPath(image_name):
    binary_path = getResultsPath() + '/' + image_name + getBinarySuffix() + getResultsExtension()
    return binary_path

# returns relative path to save Global Otsu's binary images
def getBinaryGlobalOtsuPath(image_name):
    binary_path = getResultsPath() + '/' + image_name + getBinarySuffix() + getGlobalOtsuSuffix() + getResultsExtension()
    return binary_path

# returns relative path to save Local Otsu's binary images
def getBinaryLocalOtsuPath(image_name):
    binary_path = getResultsPath() + '/' + image_name + getBinarySuffix() + getLocalOtsuSuffix() + getResultsExtension()
    return binary_path

# returns relative path to save VARI's binary images
def getVARIPath():
    vari_path = getResultsPath() + '/' + getImageFilename() + getVARISuffix() + getResultsExtension()
    return vari_path

# returns relative path to save labeled images
def getLabelingPath(image_name):
    labeling_path = getResultsPath() + '/' + image_name + getLabelingSuffix() + getResultsExtension()
    return labeling_path

# returns relative path to save closing images
def getClosingPath(image_name):
    labeling_path = getResultsPath() + '/' + image_name + getBinarySuffix() + getClosingSuffix() + getResultsExtension()
    return labeling_path

# returns relative path to save histogram
def getHistogramPath(image_name):
    histogram_path = getResultsPath() + '/' + image_name + getHistogramSuffix() + getResultsExtension()
    return histogram_path

# returns relative path to save report of detection
def getReportPath():
    report_path = getResultsPath() + '/' + 'info_subgraph' + '_' + getImageFilename() + getReportExtension()
    return report_path

def getResultsPath():
    return getSourceFolderName() + '/' + getResultsFolderName()