from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense , Activation , Dropout ,Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.metrics import categorical_accuracy
from keras.models import model_from_json
from keras.optimizers import *
from keras.layers.normalization import BatchNormalization
from sklearn.model_selection import train_test_split
import numpy as np

# get the data
filename = 'test_data.csv'
label_map = ['Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


def getData(filename):
    # images are 48x48
    # N = 35887
    Y = []
    X = []
    first = True
    for line in open(filename):
        if first:
            first = False
        else:
            row = line.split(',')
            Y.append(int(row[0]))
            X.append([int(p) for p in row[1].split()])
    X, Y = np.array(X) / 255.0, np.array(Y)
    return X, Y


X, Y = getData(filename)
num_class = len(set(Y))


# To see number of training data point available for each label
def balance_class(Y):
    num_class = set(Y)
    count_class = {}
    for i in range(len(num_class)):
        count_class[i] = sum([1 for y in Y if y == i])
    return count_class


balance = balance_class(Y)

# Keras with Tensorflow backend
N, D = X.shape
X = X.reshape(N, 48, 48, 1)

# Split in  training set : validation set :  testing set in 80:10:10
# X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=1.0, random_state=0)
# y_train = (np.arange(num_class) == y_train[:, None]).astype(np.float32)
# y_test = (np.arange(num_class) == y_test[:, None]).astype(np.float32)

X_test = list(X)
y_test = list(Y)

batch_size = 128
epochs = 15


def baseline_model_saved():
    # load json and create model
    json_file = open('model_4layer_2_2_pool.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights from h5 file
    model.load_weights("model_4layer_2_2_pool.h5")
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[categorical_accuracy])
    return model


print("Load model from disk")
model = baseline_model_saved()

# Model will predict the probability values for 7 labels for a test image
score = model.predict(X_test)
print(model.summary())

new_X = [np.argmax(item) for item in score]
y_test2 = [np.argmax(item) for item in y_test]

# Calculating categorical accuracy taking label having highest probability
accuracy = [(x == y) for x, y in zip(new_X, y_test2)]
print("Accuracy on Test set : ", np.mean(accuracy))