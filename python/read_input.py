import scipy.io
import os.path
f = os.path.dirname(__file__)+ '/../dataset/output.mat'
path = os.path.realpath(f)
mat = scipy.io.loadmat(path)
