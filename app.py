import os
import h5py
import numpy as np
from flask import Flask, render_template, request, send_from_directory

from tensorflow.keras import Sequential
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Flatten, Dropout, Dense, Input
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# ── App setup ─────────────────────────────────────────────────────────
app = Flask(__name__)

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

IMAGE_SIZE   = 128
CLASS_LABELS = ["pituitary", "glioma", "notumor", "meningioma"]
MODEL_PATH   = "models/model.h5"


# ── Rebuild the exact architecture (confirmed via inspect_model.py) ──
#   InputLayer(128,128,3)
#   VGG16(include_top=False, weights=None)   <- weights loaded manually below
#   Flatten
#   Dropout(0.3)
#   Dense(128, relu)
#   Dropout(0.2)
#   Dense(4, softmax)
def build_model():
    vgg = VGG16(
        include_top=False,
        weights=None,                       # don't fetch imagenet weights, we load our own below
        input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
    )
    model = Sequential([
        Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3)),
        vgg,
        Flatten(),
        Dropout(0.3),
        Dense(128, activation="relu"),
        Dropout(0.2),
        Dense(len(CLASS_LABELS), activation="softmax"),
    ])
    return model, vgg


# ── Load weights directly from the H5 file with h5py, bypassing  ─────
# ── Keras's from_config() entirely (that's what was breaking).   ─────
def load_weights_manually(model, vgg, path):
    with h5py.File(path, "r") as f:
        w = f["model_weights"]

        # --- VGG16 conv layers: paths look like vgg16/block1_conv1/{kernel,bias} ---
        vgg_group = w["vgg16"]
        for layer in vgg.layers:
            if layer.name in vgg_group:
                grp = vgg_group[layer.name]
                if "kernel" in grp and "bias" in grp:
                    kernel = grp["kernel"][()]
                    bias = grp["bias"][()]
                    layer.set_weights([kernel, bias])

        # --- Dense layers: nested as dense/sequential/dense/{kernel,bias} ---
        dense_layer  = model.get_layer("dense")
        dense1_layer = model.get_layer("dense_1")

        d0 = w["dense"]["sequential"]["dense"]
        dense_layer.set_weights([d0["kernel"][()], d0["bias"][()]])

        d1 = w["dense_1"]["sequential"]["dense_1"]
        dense1_layer.set_weights([d1["kernel"][()], d1["bias"][()]])

    print(f"[OK] Weights loaded manually from {path}")


def load_brain_model(path=MODEL_PATH):
    model, vgg = build_model()
    try:
        load_weights_manually(model, vgg, path)
    except Exception as e:
        raise RuntimeError(
            f"Failed to manually load weights from {path}.\n"
            f"Check that the HDF5 group structure still matches what "
            f"inspect_model.py reported.\nOriginal error: {e}"
        ) from e
    return model


model = load_brain_model()

# ── Prediction helper ─────────────────────────────────────────────────
TUMOR_INFO = {
    "notumor":     {"label": "No Tumor Detected",          "color": "success",  "icon": "✅"},
    "pituitary":   {"label": "Pituitary Tumor Detected",   "color": "warning",  "icon": "⚠️"},
    "glioma":      {"label": "Glioma Tumor Detected",      "color": "danger",   "icon": "🔴"},
    "meningioma":  {"label": "Meningioma Tumor Detected",  "color": "danger",   "icon": "🔴"},
}

def predict_tumor(image_path: str) -> dict:
    img  = load_img(image_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
    arr  = img_to_array(img) / 255.0
    arr  = np.expand_dims(arr, axis=0)

    preds = model.predict(arr, verbose=0)[0]
    idx   = int(np.argmax(preds))
    conf  = float(preds[idx])
    cls   = CLASS_LABELS[idx]

    info  = TUMOR_INFO.get(cls, {"label": cls, "color": "secondary", "icon": "❓"})

    all_probs = [
        {"class": CLASS_LABELS[i], "prob": round(float(preds[i]) * 100, 2)}
        for i in range(len(CLASS_LABELS))
    ]

    return {
        "result":     info["label"],
        "color":      info["color"],
        "icon":       info["icon"],
        "confidence": f"{conf * 100:.2f}",
        "all_probs":  all_probs,
        "raw_class":  cls,
    }

# ── Routes ────────────────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    context = {"result": None}

    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            context["error"] = "No file selected. Please choose an MRI image."
            return render_template("index.html", **context)

        ext = file.filename.rsplit(".", 1)[-1].lower()
        if ext not in {"jpg", "jpeg", "png", "bmp", "webp"}:
            context["error"] = "Invalid file type. Upload JPG, PNG, or BMP."
            return render_template("index.html", **context)

        save_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(save_path)

        prediction = predict_tumor(save_path)
        context.update(prediction)
        context["file_path"] = f"/uploads/{file.filename}"

    return render_template("index.html", **context)


@app.route("/uploads/<filename>")
def get_uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, host="0.0.0.0", port=5000)