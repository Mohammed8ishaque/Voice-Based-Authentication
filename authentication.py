import os
import librosa
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist

# Define the path to the dataset

# Define the number of Gaussian mixtures to use in GMM
n_components = 16

# Define the number of MFCC coefficients to use
n_mfcc = 12

# Define the size of the window for MFCC computation
frame_size = 0.025

# Define the stride between consecutive frames for MFCC computation
frame_stride = 0.01

# Define the threshold for accepting/rejecting a speaker
threshold = 5

# Define a function to compute the MFCC coefficients for a given audio file
def compute_mfcc(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    mfcc = librosa.feature.mfcc(y, sr, n_mfcc=n_mfcc, n_fft=int(frame_size*sr),
                                hop_length=int(frame_stride*sr))
    return mfcc.T

# Define a function to train a GMM model on the given set of audio files
def train_gmm(audio_files):
    mfccs = np.vstack([compute_mfcc(f) for f in audio_files])
    scaler = StandardScaler()
    mfccs_scaled = scaler.fit_transform(mfccs)
    gmm = GaussianMixture(n_components=n_components, covariance_type='diag')
    gmm.fit(mfccs_scaled)
    return gmm, scaler

# Train a GMM model on the set of enrollment audio files
# Define the path to the folder containing the .npy files
folder_path = "../Voice_Authentication/"

# Get a list of all files in the folder
file_list = os.listdir(folder_path)

# Filter the list to only include .npy files
npy_files = [file for file in file_list if file.endswith(".npy")]

# Select any .npy file from the list
selected_file1 = npy_files[0]

enrollment_files = [selected_file1]

# enrollment_files = enrollment_files.reshape(1,-1)
gmm, scaler = train_gmm(enrollment_files)

# enrollment_files = [os.path.join(dataset_path, "enrollment", f) for f in os.listdir(os.path.join(dataset_path, "enrollment")) if f.endswith(".wav",".mp3")]
# gmm, scaler = train_gmm(enrollment_files)

# Define a function to perform speaker verification on a given audio file
def verify_speaker(audio_file):
    mfcc = compute_mfcc(audio_file)
    mfcc_scaled = scaler.transform(mfcc)
    score = gmm.score(mfcc_scaled)
    return score

# Define a function to perform speaker identification on a given audio file
def identify_speaker(audio_file):
    mfcc = compute_mfcc(audio_file)
    mfcc_scaled = scaler.transform(mfcc)
    scores = cdist([mfcc_scaled], gmm.means_, 'mahalanobis', VI=gmm.covariances_)
    min_score_idx = np.argmin(scores)
    min_score = scores[0, min_score_idx]
    speaker = os.listdir(os.path.join(folder_path))[min_score_idx]
    return speaker, min_score

# Test files path
# Define the path to the folder containing the .npy files
folder_path0 = "../Voice_Authentication/"

# Get a list of all files in the folder
file_list = os.listdir(folder_path0)

# Filter the list to only include .npy files
npy_files = [file for file in file_list if file.endswith(".npy",".wav")]

# Select any .npy file from the list
selected_file = npy_files[0]  

# Perform speaker verification on a test audio file
test_file = f"{selected_file}"
score = verify_speaker(test_file)
if score >= threshold:
    print("Speaker accepted")
else:
    print("Speaker rejected")

# Perform speaker identification on a test audio file
test_file = f"{selected_file}"
speaker, score = identify_speaker(test_file)
if score >= threshold:
    print("Identified speaker:", speaker)
else:
    print("Speaker not recognized")

# This code assumes that you have a dataset of audio files for enrollment and testing, 
# with the enrollment files stored in a folder called "enrollment" and the test files 
# stored in a folder called "test". It also assumes that the audio files are in WAV 
# format and that they have already been preprocessed to remove any background noise 
# or other artifacts.
# The code first trains a GMM model on the set of enrollment audio files using