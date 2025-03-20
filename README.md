# Voice-Based Authentication System

## Overview

The **Voice-Based Authentication System** is a biometric security solution that authenticates users based on their voice patterns. This system leverages machine learning techniques to analyze and verify a user's voiceprint, providing a secure and user-friendly authentication method. It also integrates **Azure Blob Storage** for securely storing and retrieving voice data.

## Features

- **Biometric Security**: Uses voice patterns for authentication.
- **Machine Learning**: Implements AI models to distinguish between users.
- **Speaker Recognition**: Identifies and verifies users based on their unique voiceprints.
- **Real-Time Authentication**: Provides quick and accurate verification.
- **Secure and Efficient**: Minimizes the risk of unauthorized access.
- **Cloud Storage**: Uses Azure Blob Storage for storing voice data securely.

## Technologies Used

- **Python**: Core programming language.
- **PyAudio**: Capturing and processing voice input.
- **Librosa**: For audio processing and feature extraction.
- **NumPy & SciPy**: Data handling and signal processing.
- **scikit-learn**: Used for machine learning model implementation.
- **Azure Storage Blob**: Cloud storage for voice data.

## Installation

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.x
- Pip (Python package manager)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Mohammed8ishaque/Voice-Based-Authentication.git
   cd Voice-Based-Authentication
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up Azure Storage:
   - Update `AZURE_STORAGE_CONNECTION_STRING` in `authentication.py` and `register.py`.

4. Run the system:
   ```bash
   python authentication.py
   ```

## Usage

1. **Registration**: Users must provide voice samples for enrollment by running `register.py`. The system extracts voice features and stores them in Azure Blob Storage.
2. **Feature Extraction**: The system processes voice data and saves extracted features for authentication.
3. **Authentication**: Users verify their identity using `authentication.py`, which compares their voice against stored data.

## Project Structure

```
Voice-Based-Authentication/
│── authentication.py      # Code that authenticates the person
│── register.py            # Code that registers the person
├── ishu.npy               # Stored voice features
├── ishu.wav               # Sample voice data
│── requirements.txt       # Required dependencies
│── README.md              # Project documentation
```

## Future Enhancements

- Implementing **real-time noise reduction** for better accuracy.
- Adding **multi-factor authentication** (e.g., password + voice).
- Deploying as a **cloud-based service** for wider accessibility.
- Enhancing **voice spoofing detection** to prevent security breaches.

## Contributors

- **Mohammed Ishaque Inamdar** ([GitHub](https://github.com/Mohammed8ishaque))

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
