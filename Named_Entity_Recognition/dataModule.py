from torch.utils.data import Dataset
import numpy as np
from sklearn.model_selection import train_test_split

class char2vecDataLoader(Dataset):
    def __init__(self, X, Y, max_length, train=True):
        self.vocabulary = list("""ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{}""")
        self.vocab_length = len(self.vocabulary)

        self.identity_mat = np.identity(self.vocab_length)
        self.max_length = max_length
        self.texts = []
        self.labels = []

        X_train, X_val, y_train, y_val = train_test_split(X, Y, test_size=0.15, random_state=2020, stratify=Y)

        if train:
            self.texts = X_train
            self.labels = y_train
        else:
            self.texts = X_val
            self.labels = y_val

        self.length = len(self.labels)

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        raw_text = self.texts[index]
        data = np.array([self.identity_mat[self.vocabulary.index(i)] for i in list(str(raw_text)) if i in self.vocabulary], dtype=np.float32)

        if len(data) > self.max_length:
            data = data[:self.max_length]
        elif 0 < len(data) < self.max_length:
            data = np.concatenate((data, np.zeros((self.max_length - len(data), self.vocab_length), dtype=np.float32)))
        elif len(data) == 0:
            data = np.zeros((self.max_length, self.vocab_length), dtype=np.float32)

        label = self.labels[index]
        return data, label