# Brain Tumor Diagnosis using Deep Learning

A Flask web app that classifies brain MRI scans into one of four categories using a fine-tuned **VGG16** convolutional neural network: **glioma**, **meningioma**, **pituitary tumor**, or **no tumor**.

Upload an MRI image through the browser and get an instant prediction with a confidence score and full class-probability breakdown.

> **Author:** Divesh Kumar

---

## Screenshot

![Brain Tumor Diagnosis UI](assets/screenshot.png)

*Example: the app correctly returns a low-stakes "No Tumor Detected" style result when given a non-MRI test image, demonstrating the running pipeline. For real diagnostic testing, use actual MRI scans from `sample MRI Images/` — see the note below.*

---

## How it works

The model is a VGG16 backbone (pretrained on ImageNet, with the final convolutional block fine-tuned) feeding into a small classification head:

```
Input (128 × 128 × 3)
   │
   ▼
VGG16 (blocks 1–4 frozen, block 5 fine-tuned)
   │
   ▼
Flatten
   │
   ▼
Dropout (0.3)
   │
   ▼
Dense (128, ReLU)
   │
   ▼
Dropout (0.2)
   │
   ▼
Dense (4, Softmax) → [pituitary, glioma, notumor, meningioma]
```

The trained weights live in `models/model.h5`. Flask loads this model once at startup and reuses it for every prediction request.

⚠️ **Note:** This model only recognizes brain MRI scans. Feeding it a non-MRI photo (a pet photo, a landscape, etc.) will still produce a confident-looking prediction — the model has no way to detect "this isn't an MRI" and will force the image into one of its four known classes. Only test it with actual MRI images, such as the samples in `sample MRI Images/`.

---

## Project structure

```
BRAIN TUMOR DIAGNOSIS USING DEEP LEARNING/
├── models/
│   └── model.h5              ← trained model weights (you provide this)
├── sample MRI Images/        ← example MRI scans for testing
├── templates/
│   └── index.html            ← web UI
├── uploads/                  ← auto-created; stores user-uploaded scans
├── app.py                    ← Flask app
├── requirements.txt          ← Python dependencies
├── install.bat                ← one-click setup (Windows)
├── run.bat                    ← one-click start (Windows)
└── README.md
```

---

## Setup

### Requirements
- Python 3.10
- `models/model.h5` present (the trained model file — not included in this repo if it's large; see note below)

### Windows (quick start)
Double-click, in order:
1. `install.bat` — creates the virtual environment and installs dependencies
2. `run.bat` — starts the server

### Manual setup (Windows / macOS / Linux)

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## Usage

1. Open the app in your browser.
2. Drag and drop an MRI image (JPG, PNG, BMP, or WEBP) onto the upload area, or click to browse.
3. Click **Analyse MRI Scan**.
4. View the predicted class, confidence percentage, and the full probability breakdown across all four classes.
5. Click **Reset** to upload a different scan.

---

## Troubleshooting

### `TypeError: Unrecognized keyword arguments passed to Dense: {'quantization_config': None}`

This means the `model.h5` file was saved with a newer version of Keras than the one installed in your environment. The saved layer config includes a `quantization_config` field that older Keras versions don't recognize when rebuilding the model.

**Fix already applied in this repo's `app.py`:** instead of calling `keras.models.load_model()` (which fails on the mismatched config), the app:
1. Rebuilds the exact model architecture in code (VGG16 backbone + custom classification head).
2. Loads only the raw weight arrays from `model.h5` directly via `h5py`, bypassing Keras's architecture deserialization entirely.

If you ever retrain and re-save the model, you can re-run the included `inspect_model.py` script to confirm the saved architecture and HDF5 weight-group paths still match what `app.py` expects:

```bash
python inspect_model.py
```

### `numpy.core._exceptions._ArrayMemoryError: Unable to allocate X MiB`

This is usually **not** a real memory shortage — it typically happens when Flask's debug auto-reloader restarts the app and tries to load the model a second time while the first instance is still finishing teardown. The app is configured with `debug=False, use_reloader=False` to prevent this. If you re-enable debug mode for development, expect this to resurface.

### Model badge says the wrong architecture in the UI

`templates/index.html` may still show an old label (e.g. "InceptionV3") from an earlier iteration of the project. The actual model in `models/model.h5` is **VGG16**. Update the badge text in `index.html` if needed — it's cosmetic only and doesn't affect predictions.

---

## Tech stack

- **Backend:** Flask
- **Model:** TensorFlow / Keras (VGG16 transfer learning)
- **Frontend:** HTML/CSS (dark theme, drag-and-drop upload)

---

## Disclaimer

This tool is for educational and research purposes only. It is **not** a certified medical device and must not be used for actual clinical diagnosis. Always consult a qualified radiologist or physician for medical decisions.
