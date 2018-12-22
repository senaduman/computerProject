import scipy.io as sio
import numpy as np
import cv2
img = 'C:\\Users\\Sena Duman\\Desktop\\CRCHistoPhenotypes\\crchistophenotypes\\' \
      'CRCHistoPhenotypes\\Classification\\img5\\img5.bmp'
im_ = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
fileE = 'C:\\Users\\Sena Duman\\Desktop\\CRCHistoPhenotypes\\crchistophenotypes\\' \
        'CRCHistoPhenotypes\\Classification\\img5\\img5_epithelial.mat'
matE = sio.loadmat(fileE)
contentsE = matE['detection']
contentsE = np.array(contentsE)
contentsE = contentsE.astype(int)
xE = contentsE[:,0]
yE = contentsE[:,1]


