from lasagne import layers
from lasagne.updates import nesterov_momentum
from nolearn.lasagne import NeuralNet
import utils
from sklearn.metrics import mean_squared_error

try:
	from lasagne.layers.cuda_convnet import Conv2DCCLayer as Conv2DLayer
	from lasagne.layers.cuda_convnet import MaxPool2DCCLayer as MaxPool2DLayer
except ImportError:
	Conv2DLayer = layers.Conv2DLayer
	MaxPool2DLayer = layers.MaxPool2DLayer

if __name__ == "__main__":

    net1 = NeuralNet(
        layers=[   #three layers: one hidden layer
            ('input', layers.InputLayer),
            ('hidden', layers.DenseLayer),
            ('output', layers.DenseLayer),
            ],
         #layer parameters:
        input_shape=(128, 9216),  # 128 images per batch times 96x96 input pixels
        hidden_num_units=100,  # number of units in hidden layer
        output_nonlinearity=None,  # output layer uses identity function
        output_num_units=30,  # 30 target values

        ## optimization method:
        update=nesterov_momentum,
        update_learning_rate=0.01,
        update_momentum=0.9,

        regression=True,  # flag to indicate we're dealing with regression problem
        max_epochs=400,  # we want to train this many epochs
        verbose=1,
        )
    X, y = utils.load()

    print("X.shape == {}; X.min == {:.3f}; X.max == {:.3f}".format(
        X.shape, X.min(), X.max()))
    print("y.shape == {}; y.min == {:.3f}; y.max == {:.3f}".format(
        y.shape, y.min(), y.max()))#with codecs.open(CORPUS_FILE, mode='w', encoding='utf-8') as news_file:
    net1.fit(X, y)

    utils.save_net(net1, "net1")
    utils.plot_result(net1)

    print mean_squared_error(net1.predict(X), y)
