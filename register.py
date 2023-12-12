import pyaudio
import wave
import soundfile
import librosa
import numpy as np
import azure.storage.blob
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


# Set up audio parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Get user's name
name = input("Please enter your name: ")

# Start recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

print("Recording...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording finished.")

# Stop recording
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recording to a file with the user's name
filename = f"{name}.wav"
wf = wave.open(filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# print(f"Your voice has been registered as {filename}.")

# Load audio file
audio, sr = librosa.load(f'{filename}')

# # Apply noise reduction using spectral subtraction
# n_fft = 2048
# hop_length = 512
# noise = librosa.stft(audio[:n_fft], n_fft=n_fft, hop_length=hop_length)
# noise = np.mean(np.abs(noise)**2, axis=1)
# audio_stft = librosa.stft(audio, n_fft=n_fft, hop_length=hop_length)
# audio_power = np.abs(audio_stft)**2
# alpha = 2.0
# audio_power -= alpha * noise[:, np.newaxis]
# audio_power = np.maximum(audio_power, 0.0)
# audio_stft = np.sqrt(audio_power) * np.exp(1.0j * np.angle(audio_stft))
# audio = librosa.istft(audio_stft, hop_length=hop_length)

# # Save noise-reduced audio file
# soundfile.write(f'{filename}', audio, sr)

print(f"Your voice has been registered as {filename}.")


# Load the audio file
y, sr = librosa.load(filename)

# Extract features
chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc = 50)
spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

# Concatenate features into a single vector
features = np.concatenate([chroma_stft.mean(axis=1), mfcc.mean(axis=1), spectral_contrast.mean(axis=1)])

# Save features to file
features_file = f"{name}.npy"

np.save(features_file, features)

print(f"Features extracted from {filename} and saved to {features_file}.")

STORAGE_ACCOUNT_NAME = "voice1authentication"
STORAGE_ACCOUNT_KEY = "9KkQ7Y46EhbGtk3VpfDcRj8VMGN21uJz29zYElJCtFhqKM1PYfC62lJmhAM00KVAy7PKslTcjI8o+AStvBJYAw=="
CONTAINER_NAME = "speaker-storage"
BLOB_NAME =  [file for file in CONTAINER_NAME if file.endswith(".npy")]

# Upload MFCC features to Azure Blob Storage
# blob_name = f"{features_file}"
# block_blob_service = azure.storage.blob.BlobServiceClient(account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",account_name=STORAGE_ACCOUNT_NAME, account_key=STORAGE_ACCOUNT_KEY)
# block_blob_service.get_blob_client(CONTAINER_NAME, blob_name, str(features))
# print("MFCC features uploaded to Azure Blob Storage!")

# Set your connection string and container name
connection_string = 'DefaultEndpointsProtocol=https;AccountName=voice1authentication;AccountKey=9KkQ7Y46EhbGtk3VpfDcRj8VMGN21uJz29zYElJCtFhqKM1PYfC62lJmhAM00KVAy7PKslTcjI8o+AStvBJYAw==;EndpointSuffix=core.windows.net'
container_name = 'speaker-storage'

# Create BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Create a blob client and upload the file
blob_client = blob_service_client.get_blob_client(container=container_name, blob=f'{features_file}')
with open(f'{features_file}', "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print("MFCC features uploaded to Azure Blob Storage!")

# # Define the connection string for the Azure Storage account
# connect_str = "DefaultEndpointsProtocol=https;AccountName=voice1authentication;AccountKey=9KkQ7Y46EhbGtk3VpfDcRj8VMGN21uJz29zYElJCtFhqKM1PYfC62lJmhAM00KVAy7PKslTcjI8o+AStvBJYAw==;EndpointSuffix=core.windows.net"

# # Create a BlobServiceClient object to interact with the Azure Storage account
# blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# # Define the name of the container to upload the file to
# container_name = "speaker-storage"

# # Create a ContainerClient object to interact with the container
# container_client = blob_service_client.get_container_client(container_name)

# # Define the path to the file to upload
# file_path = "../Voice_Authentication/"

# # Define the name of the file in the container
# blob_name = "audioMNIST_meta.txt" # this file contains the list of users

# # Create a BlobClient object to interact with the file in the container
# blob_client = container_client.get_blob_client(blob_name)

# # Upload the file to the container
# with open(file_path, "rb") as data:
#     blob_client.upload_blob(data)

# # Print a message to confirm that the file has been uploaded
# print(f"File {blob_name} uploaded to container {container_name}")
