import os
import keras
import librosa
import numpy as np
import matplotlib.pyplot as plt
from keras import Sequential
from keras.utils import to_categorical
from keras.layers import Dense
from sklearn.model_selection import train_test_split

DATA = 'data.npy'
TARGET = 'target.npy'


# 加载标签
def load_label(label_path):
    label = os.listdir(label_path)
    return label


# 提取 mfcc 参数
def wav2mfcc(path, max_pad_size=11):
    y, sr = librosa.load(path=path, sr=None, mono=False)
    y = y[::3]
    audio_mac = librosa.feature.mfcc(y=y, sr=16000)
    y_shape = audio_mac.shape[1]
    if y_shape < max_pad_size:
        pad_size = max_pad_size - y_shape
        audio_mac = np.pad(audio_mac, ((0, 0), (0, pad_size)), mode='constant')
    else:
        audio_mac = audio_mac[:, :max_pad_size]
    return audio_mac


# 存储处理过的数据，方便下一次的使用
def save_data_to_array(label_path, max_pad_size=11):
    mfcc_vectors = []
    target = []
    labels = load_label(label_path=label_path)
    for i, label in enumerate(labels):
        path = label_path + '/' + label
        wavfiles = [path + '/' + file for file in os.listdir(path)]
        for wavfile in wavfiles:
            wav = wav2mfcc(wavfile, max_pad_size=max_pad_size)
            mfcc_vectors.append(wav)
            target.append(i)
    np.save(DATA, mfcc_vectors)
    np.save(TARGET, target)
    # return mfcc_vectors, target


# 获取训练集与测试集
def get_train_test(split_ratio=.6, random_state=42):
    X = np.load(DATA)
    y = np.load(TARGET)
    assert X.shape[0] == y.shape[0]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(1 - split_ratio), random_state=random_state,
                                                        shuffle=True)
    return X_train, X_test, y_train, y_test


def main():
    x_train, x_test, y_train, y_test = get_train_test()
    x_train = x_train.reshape(-1, 220)
    x_test = x_test.reshape(-1, 220)
    y_train_hot = to_categorical(y_train)
    y_test_hot = to_categorical(y_test)
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(220,)))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(6, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.RMSprop(),
                  metrics=['accuracy'])
    history = model.fit(x_train, y_train_hot, batch_size=100, epochs=20, verbose=1,
                        validation_data=(x_test, y_test_hot))
    plot_history(history)


def save():
    label_path = 'audio'
    save_data_to_array(label_path, max_pad_size=11)


def plot_history(history):
    plt.plot(history.history['acc'],label='train')
    plt.plot(history.history['val_acc'],label='validation')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
