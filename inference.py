from pathlib import Path

import soundfile
import tensorflow.keras as keras
import numpy as np
import librosa

from create_dataset import process_audio_np, denoise_audio_np


class Inference:
    def __init__(self, model_path, sample_rate):
        self.model = keras.models.load_model(model_path)
        self.sample_rate = sample_rate

        self.model.summary()

    def predict(self, byte_list, threshold=0.01):
        # TODO figure out why x shape first dim is double what it should be
        #  (ex: 35 sec clip divided into 5 sec clips produces 14 in first dim)
        x = self.preprocess(byte_list)
        print("x shape", x.shape)

        pred = self.model.predict_on_batch(x)
        print("pred shape", pred.shape)
        avg_pred = np.mean(pred)
        print("avg_pred", avg_pred)

        if 0.5 - threshold <= avg_pred <= 0.5 + threshold:
            return "unsure"
        if avg_pred > 0.5:
            return "abnormal"
        return "normal"

    def preprocess(self, byte_list):
        audio = np.array(byte_list)
        audio = librosa.resample(audio, self.sample_rate, 1000)
        mfccs = process_audio_np(audio, 5)  # 5 second samples
        return np.array(mfccs)

    def get_wav(self, byte_list):
        audio = np.array(byte_list)
        audio = librosa.resample(audio, self.sample_rate, 1000)
        audio = denoise_audio_np(audio)
        soundfile.write("./outputs/temp_recording.wav", audio, 1000)


if __name__ == "__main__":
    model_full_save = Path(
        "./model_saves/3515192_epochs_15-batch_size_2-lr_1e-06/full_save"
    )
    test_audio_path = Path(
        "./datasets/classification-heart-sounds-physionet/training-a/a0001.wav"
    )

    inference = Inference(model_full_save, 1000)

    audio_np, sr = librosa.load(test_audio_path, sr=None)
    print(inference.predict(audio_np))
