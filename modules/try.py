#kütüphane importları
import scipy.io as sio
import numpy as np
import cv2
import os

from skimage import feature
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
import matplotlib.pyplot as plt

def LBP(image):

    table = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 6: 5, 7: 6, 8: 7, 12: 8, 14: 9, 15: 10, 16: 11, 24: 12, 28: 13, 30: 14, 31: 15,
         32: 16, 48: 17, 56: 18, 60: 19, 62: 20, 63: 21, 64: 22, 96: 23, 112: 24, 120: 25, 124: 26, 126: 27, 127: 28,
         128: 29, 129: 30, 131: 31, 135: 32, 143: 33, 159: 34, 191: 35, 192: 36, 193: 37, 195: 38, 199: 39, 207: 40,
         223: 41, 224: 42, 225: 43, 227: 44, 231: 45, 239: 46, 240: 47, 241: 48, 243: 49, 247: 50, 248: 51, 249: 52,
         251: 53, 252: 54, 253: 55, 254: 56, 255: 57}

    histogram = [0 for i in range(59)]
    for i in range(1, len(image) - 1):
        for j in range(1, len(image[0]) - 1):
            lbp = 0
            lbp |= 1 * int(image[i - 1][j - 1] > image[i][j])
            lbp |= 2 * int(image[i - 1][j] > image[i][j])
            lbp |= 4 * int(image[i - 1][j + 1] > image[i][j])
            lbp |= 8 * int(image[i][j + 1] > image[i][j])
            lbp |= 16 * int(image[i + 1][j + 1] > image[i][j])
            lbp |= 32 * int(image[i + 1][j] > image[i][j])
            lbp |= 64 * int(image[i + 1][j - 1] > image[i][j])
            lbp |= 128 * int(image[i][j - 1] > image[i][j])
            if lbp in table:
                histogram[table[lbp]] += 1
            else:
                histogram[58] += 1

    return histogram


successPercentage = []
resultArray = []
parentDirectory = 'C:\\Users\\Sena Duman\\Desktop\\CRCHistoPhenotypes\\crchistophenotypes\\CRCHistoPhenotypes\\Classification'
list = os.listdir(parentDirectory)
imageFolders = len(list)
#print(imageFolders)

for j in range(1, imageFolders + 1):
    fileAddsImg = '\\img' + str(j) + '\\img' + str(j) + '.bmp'
    fileAddsE = '\\img' + str(j) + '\\img' + str(j) + '_epithelial.mat'
    fileAddsF = '\\img' + str(j) + '\\img' + str(j) + '_fibroblast.mat'
    fileAddsI = '\\img' + str(j) + '\\img' + str(j) + '_inflammatory.mat'
    fileAddsO = '\\img' + str(j) + '\\img' + str(j) + '_others.mat'

    fileE = parentDirectory + fileAddsE
    fileF = parentDirectory + fileAddsF
    fileI = parentDirectory + fileAddsI
    fileO = parentDirectory + fileAddsO
    img = parentDirectory + fileAddsImg

    #etiketli veri klasöründen resim ve hücre tiplerinin dosyaları
    '''
    fileE = 'C:\\Users\\Sena Duman\\Desktop\\CRCHistoPhenotypes\\crchistophenotypes\\CRCHistoPhenotypes\\Classification\\img15\\img15_epithelial.mat'
    fileF = 'C:\\Users\\Sena Duman\\Desktop\\CRCHistoPhenotypes\\crchistophenotypes\\CRCHistoPhenotypes\\Classification\\img15\\img15_fibroblast.mat'
    fileI = 'C:\\Users\\Sena Duman\\Desktop\\CRCHistoPhenotypes\\crchistophenotypes\\CRCHistoPhenotypes\\Classification\\img15\\img15_inflammatory.mat'
    fileO = 'C:\\Users\\Sena Duman\\Desktop\\CRCHistoPhenotypes\\crchistophenotypes\\CRCHistoPhenotypes\\Classification\\img15\\img15_others.mat'
    img = 'C:\\Users\\Sena Duman\\Desktop\\CRCHistoPhenotypes\\crchistophenotypes\\CRCHistoPhenotypes\\Classification\\img15\\img15.bmp'
    '''
    #mat dosyalarının içeriğinin alınması, x ve y koordinatları ayrı ayrı alınıyor
    matE = sio.loadmat(fileE)
    contentsE = matE['detection']
    contentsE = np.array(contentsE)
    contentsE = contentsE.astype(int)
    classesE = np.zeros(np.size(contentsE, axis=0))
    classesE[classesE == 0] = 0
    xE = contentsE[:,0]
    yE = contentsE[:,1]
    matF = sio.loadmat(fileF)
    contentsF = matF['detection']
    contentsF = np.array(contentsF)
    contentsF = contentsF.astype(int)
    classesF = np.zeros(np.size(contentsF, axis=0))
    classesF[classesF == 0] = 1
    xF = contentsF[:,0]
    yF = contentsF[:,1]
    matI = sio.loadmat(fileI)
    contentsI = matI['detection']
    contentsI = np.array(contentsI)
    contentsI = contentsI.astype(int)
    classesI = np.zeros(np.size(contentsI, axis=0))
    classesI[classesI == 0] = 2
    xI = contentsI[:,0]
    yI = contentsI[:,1]
    matO = sio.loadmat(fileO)
    contentsO = matO['detection']
    contentsO = np.array(contentsO)
    contentsO = contentsO.astype(int)
    classesO = np.zeros(np.size(contentsO, axis=0))
    classesO[classesO == 0] = 3
    xO = contentsO[:,0]
    yO = contentsO[:,1]

    #resim üstüne okunan mat dosyasındaki noktalar basılıyor, renklere göre hücre tipleri fark ediyor
    im = plt.imread(img)
    '''
    implot = plt.imshow(im)
    implot = plt.scatter(xE, yE, c='cyan', s=5)
    implot = plt.scatter(xF, yF, c='r', s=5)
    implot = plt.scatter(xI, yI, c='g', s=5)
    implot = plt.scatter(xO, yO, c='b', s=5)
    plt.show()
    '''
    #resmin grayscaled okunduğu yer
    im_ = cv2.imread(img, cv2.IMREAD_GRAYSCALE)


    #süperpiksel uygulanması, süperpikselli resim üzerine hücre noktalarının basılmış hali
    segments = slic(im_, n_segments=1350, compactness=0.1, enforce_connectivity=True, sigma=3)
    '''
    fig = plt.figure("Superpixels -- 500 segments")
    ax = fig.add_subplot(1, 1, 1)
    figs = ax.imshow(mark_boundaries(im_, segments, mode='inner', color=(1, 0, 0)))
    figs = plt.scatter(xE, yE, c='g', s=2)
    figs = plt.scatter(xF, yF, c='g', s=2)
    figs = plt.scatter(xI, yI, c='g', s=2)
    figs = plt.scatter(xO, yO, c='g', s=2)
    plt.axis("off")
    plt.show()

    #rapora şekil şukul olsun diye 3 figürü yan yana bastırmışım bu dursun işimize yarar
    plt.subplot(1, 3, 1)
    plt.imshow(im)
    plt.subplot(1, 3, 2)
    plt.imshow(im_, cmap='gray')
    plt.subplot(1, 3, 3)

    plt.scatter(xE, yE, c='r', s=2)
    plt.scatter(xF, yF, c='r', s=2)
    plt.scatter(xI, yI, c='r', s=2)
    plt.scatter(xO, yO, c='r', s=2)
    plt.imshow(im_, cmap='gray')
    plt.figure()
    plt.show()
    '''
    #segmentasyon için hücre merkezi ve etiket verisi verilerinin hazırlanması
    xS = np.concatenate((xE, xF, xI, xO), axis=0)
    yS = np.concatenate((yE, yF, yI, yO), axis=0)
    classes = np.concatenate((classesE, classesF, classesI, classesO), axis=0)
    #print("total cell count: %d" % len(classes))

    # acayip logiclerle segmentasyon

    maxIndex = np.max(segments)
    markedSuperpixels = np.zeros(maxIndex)
    index = 0
    segmentedCount = 0
    segmentedImage = np.zeros((500, 500), dtype=np.uint8)
    segmentsOfImage = np.zeros((500, 500), dtype=np.uint8)
    lbpResult = []
    while index <= maxIndex:
        arr = np.where(segments == index)
        arr = np.array(arr)

        miny = np.min(arr[0][0:])
        maxy = np.max(arr[0][0:])
        minx = np.min(arr[1][0:])
        maxx = np.max(arr[1][0:])
        width = maxx - minx + 1
        height = maxy - miny + 1
        tempArr = np.zeros((height, width), dtype=np.uint8)
        lbpVector = np.zeros(59, dtype=np.uint8)

        segLen = np.size(arr, axis=1)
        dotLen = np.size(xS)
        dotIndex = 0
        segIndex = 0
        skip = 0

        while dotIndex < dotLen:
            while segIndex < segLen and skip == 0:
                if arr[1][segIndex] == xS[dotIndex] and arr[0][segIndex] == yS[dotIndex]:
                    i = 0
                    pixelCount = 0
                    averageColour = 0
                    segmentedCount += 1
                    for i in range(0, segLen):
                        segmentedImage[arr[0][i]][arr[1][i]] = im_[arr[0][i]][arr[1][i]]
                        segmentsOfImage[arr[0][i]][arr[1][i]] = index
                        pixelCount += segmentedImage[arr[0][i]][arr[1][i]]
                        averageColour = int(pixelCount / segLen)
                        tempArr[int((height - 1) / (maxy - miny) * (arr[0][i] - maxy) + (height - 1))][
                            int((width - 1) / (maxx - minx) * (arr[1][i] - maxx) + (width - 1))] = im_[arr[0][i]][
                            arr[1][i]]


                    skip = 1
                else:
                    segIndex += 1
                    skip = 0
            dotIndex += 1
            segIndex = 0
        index += 1


    '''
    plt.imshow(segmentedImage, cmap='gray')
    segmentedImage = mark_boundaries(segmentedImage, segmentsOfImage, mode='inner', color=(1, 0, 0))
    plt.imshow(segmentedImage, cmap='gray')
    plt.show()
    '''

    successPercentage.append(float("{0:.2f}".format(segmentedCount/len(classes)*100)))
    #segmentasyon, lbp uygulanması ve csv dosya kaydı
    #print("segmented cell count: %d" % segmentedCount)

    print("image %d is processed." % j)

print("Overall success rate: %f" % (sum(successPercentage)/len(successPercentage)))





#parentLbpCsvVector = np.concatenate((parentLbpCsvVector,resultArray), axis=1)

#parentLbpCsvVector = np.array(parentLbpCsvVector)
#np.savetxt("dataset-lbp.csv", parentLbpCsvVector, delimiter=",", fmt="%s")








