import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# based on the low-level example at
# https://rubikscode.net/2018/11/26/3-ways-to-implement-autoencoders-with-tensorflow-and-python/
class AutoEncoder:
    """A generalized autoencoder class
    Can be used in `with` statements
    """
    def __init__(self, layers,
                 regularization : int = 0,
                 activation = tf.nn.relu,
                 params : dict = {'learning_rate': 0.1, 'lambda': 1e-6}):
        """
        Parameters
        ----------
        layers : Iterable[int]
            Dimensions for each layer
            From input through encoded only; therefore len(layers) >= 2
        regularization : int [0,1,2]
            Regularization to use
            None if 0, L1 if 1, L2 if 2
            Default: 0
        activation : function
            The activation function to use for each layer
            Default: tf.nn.relu
        params : dict
            'learning_rate' : float
                The learning rate passed to the optimizer
            'lambda' : float
                The value multiplied by the regularization given in regularization
        """
        if not (hasattr(layers, '__len__') and all([type(i) is int for i in layers])):
            raise TypeError('layers must be an Iterable of ints')
        elif not regularization in [0, 1,2]:
            raise ValueError('regularization must be 0, 1, or 2')
        elif not str(type(activation)) == '<class \'function\'>':
            raise TypeError('activation must be a function')
        elif not (type(params) is dict and 'learning_rate' in params and 'lambda' in params):
            raise ValueError('params must define \'learning_rate\' and \'lambda\'')
        elif not type(params['learning_rate']) in [float, int]:
            raise TypeError('params[\'learning_rate\'] must be a float')
        elif not type(params['lambda']) in [float, int]:
            raise TypeError('params[\'lambda\'] must be a float')
        
        # inititalize network
        self._input = tf.placeholder('float', [None, layers[0]], 'input')
        
        if len(layers) == 2: # for only one hidden layer
            w_e = tf.Variable(tf.random.poisson(1, shape=list(layers)))
            b_e = tf.Variable(tf.random.normal(shape=[layers[1]]))
            w_d = tf.Variable(tf.random.poisson(1, shape=list(reversed(layers))))
            b_d = tf.Variable(tf.random.normal(shape=[layers[0]]))
            
            self._weights = [w_e, w_d]
            
            self._encoded = activation(self._input @ w_e + b_e, name='encoded')
            self._decoded = activation(self._encoded @ w_d + b_d, name='decoded')
            
        else: # for multiple hidden layers
            self._weights = []
            
            self._encoding_layers = []
            for i in range(0, len(layers)-1):
                w = tf.Variable(tf.random.poisson(1, shape=[layers[i], layers[i+1]]))
                b = tf.Variable(tf.random.normal(shape=[layers[i+1]]))
                self._weights.append(w)
                
                if i == 0:
                    self._encoding_layers.append(activation(self._input @ w + b, name='layer_encode' + str(i)))
                elif i+1 == len(layers) - 1:
                    self._encoded = activation(self._encoding_layers[-1] @ w + b, name='encoded')
                else:
                    self._encoding_layers.append(activation(self._encoding_layers[-1] @ w + b,
                                                 name = 'layer_encode' + str(i)))
            
            self._decoding_layers = []
            for i in range(1, len(layers)):
                print('decode',i)
                w = tf.Variable(tf.random.poisson(1, shape=[layers[-i], layers[-(i+1)]]))
                b = tf.Variable(tf.random.normal(shape=[layers[-(i+1)]]))
                self._weights.append(w)
                
                if i == 0:
                    self._decoding_layers.append(activation(self._encoded @ w + b, name='layer_decode' + str(i)))
                elif i+1 == len(layers) - 1:
                    self._decoded = activation(self._decoding_layers[-1] @ w + b, name='decoded')
                else:
                    self._decoding_layers.append(activation(self._decoding_layers[-1] @ w + b,
                                                           name = 'layer_decode' + str(i)))
        
        # setup
        self._l1 = tf.reduce_sum([tf.reduce_sum(i) for i in self._weights], name='l1')
        self._l2 = tf.reduce_sum([tf.reduce_sum(tf.square(i)) for i in self._weights], name='l2')
        self._loss = tf.reduce_mean(tf.square(self._input - self._decoded)) + \
                    params['lambda']*(0 if regularization == 0 else self._l2 if regularization == 2 else self._l1)
        self._optimizer = tf.train.GradientDescentOptimizer(params['learning_rate']).minimize(self._loss)
        self._training = tf.global_variables_initializer()
        self._session = tf.InteractiveSession()
        
        
    def train(self, x_train, x_val, batch_size, epochs, quiet=True):
        """Train the autoencoder
        
        Parameters
        ----------
        x_train : array
            A 2D array of values to train from
            Arranged as [repeats, values]
        x_val : array
            A 2D array of values to validate on
            Arranged as [repeats, values]
        batch_size : int
            The number of samples to train on at a time
        epochs : int
            The number of times to go through the training set
            
        Returns
        -------
        self : AutoEncoder
            for use in `auto = AutoEncode(...).train(...)`
        """
        self._session.run(self._training)
        self._losses = []
        
        if not quiet: print('Begin training...')
        
        for epoch in range(epochs):
            for i in range(x_train.shape[0] // batch_size):
                batch_x = x_train[i * batch_size : (i+1) * batch_size, :]
                self._session.run(self._optimizer, feed_dict = {self._input: batch_x})

            loss = self._session.run(self._loss, feed_dict={self._input: x_val})
            if np.isnan(loss):
                raise RuntimeError('Got nan for loss')
            self._losses.append(loss)
            if not quiet or (quiet and epoch+1 == epochs):
                print('Epoch', epoch+1, '/', epochs, 'loss:', loss)
                
        return self
    
    def loss_report(self):
        fig, ax = plt.subplots()
        ax.set_xlabel = 'epochs'
        ax.set_ylabel = 'loss'
        if hasattr(self, '_losses'):
            ax.plot(self._losses)
        return fig, ax
            
    def encode(self, x):
        x_en = self._session.run(self._encoded, feed_dict={self._input: x})
        return x_en
    
    def decode(self, x_en):
        x_de = self._session.run(self._decoded, feed_dict={self._encoded: x_en})
        return x_de
    
    def denoise(self, x):
        x_de = self._session.run(self._decoded, feed_dict={self._input: x})
        return x_de
    
    def close(self):
        self._session.close()
    
    
    # for context management
    def __enter__(self):
        return self
    def __exit__(self, type, value, tb):
        self.close()
        return False
        
        
a, b = np.array([[10]*10]*10000), np.array([[10]*10]*100)
a, b = a + np.random.normal(size=(10000,10)), b + np.random.normal(size=(100,10))
auto = AutoEncoder((10,2)).train(a, b, 100, 200)
# [Out]: Epoch 200 / 200 loss: 81.27038

auto.loss_report()

print(np.mean(auto.denoise(a), axis=0))
# [Out]: [ 0.      ,  0.      ,  0.      , 10.00781 ,  0.      ,  0.      ,  0.      ,  0.      ,  0.      , 10.000637]

auto.close()
plt.show()
