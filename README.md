# Image Processing and Classification Project

This repository contains a project for image processing and classification using Python. The project includes scripts for cropping images and training a convolutional neural network (CNN) model for image classification.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Scripts](#scripts)
- [Model Training](#model-training)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Cropping Images

1. Ensure the `config.json` file is properly configured with the source and destination directories for the images.
2. Run the `crop-im.py` script to start the image cropping tool:
    ```sh
    python crop-im.py
    ```

### Model Training

1. Ensure the images are organized in the `data/train/` directory.
2. Run the `test.py` script to start training the CNN model:
    ```sh
    python test.py
    ```

## Configuration

The `config.json` file should contain the source and destination directories for the images. Example:
```json
[
    {
        "src": "original\\train\\cendol",
        "dest": "data\\train\\cendol"
    },
    {
        "src": "original\\train\\tauhuay",
        "dest": "data\\train\\tauhuay"
    },
    {
        "src": "original\\train\\tausuan",
        "dest": "data\\train\\tausuan"
    }
]
```

## Scripts

### `crop-im.py`

This script provides a GUI tool for cropping images. It uses the `tkinter` library for the GUI and `PIL` for image processing.

### `test.py`

This script trains a CNN model using the `tensorflow.keras` library. It includes data augmentation using `ImageDataGenerator` and saves the best model based on validation accuracy.

## Model Training

The model is defined in the `createModel` function in `test.py`. It uses several convolutional layers, batch normalization, and dropout for regularization. The model is trained using the Adam optimizer and categorical cross-entropy loss.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.