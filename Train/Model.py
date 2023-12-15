import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from Utils import config
from keras.models import load_model, Model
from keras.layers import Dense, Flatten, Conv2D, BatchNormalization, LeakyReLU, add, Input
from keras.optimizers import Adam
from keras import regularizers
from loss import softmax_cross_entropy_with_logits
matplotlib.use('Agg')


class ResidualCNN:
    def __init__(self, reg_const, learning_rate, input_dim, output_dim, hidden_layers):
        self.reg_const = reg_const
        self.learning_rate = learning_rate
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_layers = hidden_layers
        self.num_layers = len(hidden_layers)
        self.model = self._build_model()

    def pred(self, x):
        return self.model.predict(x)

    def fit(self, state, target, epochs, verbose=0, validation_split=0.1, batch_size=32):
        self.model.fit(
            state, target,
            epochs=epochs,
            verbose=verbose,
            validation_split=validation_split,
            batch_size=batch_size
        )

    def save(self, version):
        self.model.save(config.MODEL_PATH.format(version))

    def load(self, version):
        self.model = load_model(config.MODEL_PATH.format(version))

    def conv_layer(self, x, filters, kernel_size):
        x = Conv2D(
            filters=filters,
            kernel_size=kernel_size,
            data_format="channels_first",
            padding='same',
            use_bias=False,
            activation='linear',
            kernel_regularizer=regularizers.l2(self.reg_const)
        )(x)

        x = BatchNormalization(axis=1)(x)
        x = LeakyReLU()(x)

        return x

    def residual_layer(self, input_block, filters, kernel_size):
        x = self.conv_layer(input_block, filters, kernel_size)
        x = Conv2D(
            filters=filters,
            kernel_size=kernel_size,
            data_format="channels_first",
            padding='same',
            use_bias=False,
            activation='linear',
            kernel_regularizer=regularizers.l2(self.reg_const)
        )(x)

        x = BatchNormalization(axis=1)(x)
        x = add([input_block, x])
        x = LeakyReLU()(x)

        return x

    def value_head(self, x):
        x = self.conv_layer(x, 1, (1, 1))
        x = Flatten()(x)
        x = Dense(
            20,
            use_bias=False,
            activation='linear',
            kernel_regularizer=regularizers.l2(self.reg_const)
        )(x)
        x = LeakyReLU()(x)
        x = Dense(
            1,
            use_bias=False,
            activation='tanh',
            kernel_regularizer=regularizers.l2(self.reg_const),
            name='value_head'
        )(x)

        return x

    def policy_head(self, x):
        x = self.conv_layer(x, 2, (1, 1))
        x = Flatten()(x)
        x = Dense(
            self.output_dim,
            use_bias=False,
            activation='linear',
            kernel_regularizer=regularizers.l2(self.reg_const),
            name='policy_head'
        )(x)

        return x

    def _build_model(self):

        main_input = Input(shape=self.input_dim, name='main_input')

        x = self.conv_layer(main_input, self.hidden_layers[0]['filters'], self.hidden_layers[0]['kernel_size'])

        if len(self.hidden_layers) > 1:
            for h in self.hidden_layers[1:]:
                x = self.residual_layer(x, h['filters'], h['kernel_size'])

        vh = self.value_head(x)
        ph = self.policy_head(x)

        model = Model(inputs=[main_input], outputs=[vh, ph])
        model.compile(loss={'value_head': 'mean_squared_error', 'policy_head': softmax_cross_entropy_with_logits},
                      optimizer=Adam(lr=self.learning_rate, momentum=config.MOMENTUM),
                      loss_weights={'value_head': 0.5, 'policy_head': 0.5}
                      )

        return model

    def viewLayers(self):
        layers = self.model.layers
        for i, l in enumerate(layers):
            x = l.get_weights()
            print('LAYER ' + str(i))

            try:
                weights = x[0]
                s = weights.shape

                fig = plt.figure(figsize=(s[2], s[3]))  # width, height in inches
                channel = 0
                filter = 0
                for i in range(s[2] * s[3]):
                    sub = fig.add_subplot(s[3], s[2], i + 1)
                    sub.imshow(weights[:, :, channel, filter], cmap='coolwarm', clim=(-1, 1), aspect="auto")
                    channel = (channel + 1) % s[2]
                    filter = (filter + 1) % s[3]

            except:
                try:
                    fig = plt.figure(figsize=(3, len(x)))  # width, height in inches
                    for j in range(len(x)):
                        sub = fig.add_subplot(len(x), 1, j + 1)
                        if j == 0:
                            clim = (0, 2)
                        else:
                            clim = (0, 2)
                        sub.imshow([x[j]], cmap='coolwarm', clim=clim, aspect="auto")

                    plt.show()
                except:
                    try:
                        fig = plt.figure(figsize=(3, 3))  # width, height in inches
                        sub = fig.add_subplot(1, 1, 1)
                        sub.imshow(x[0], cmap='coolwarm', clim=(-1, 1), aspect="auto")

                        plt.show()

                    except:
                        pass

            plt.show()
