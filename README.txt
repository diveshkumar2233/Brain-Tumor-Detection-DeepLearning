═══════════════════════════════════════════════════════════════
   BRAIN TUMOR DIAGNOSIS USING DEEP LEARNING
   Flask + TensorFlow + InceptionV3
═══════════════════════════════════════════════════════════════

PROJECT STRUCTURE
─────────────────
BRAIN TUMOR DIAGNOSIS USING DEEP LEARNING\
│
├── models\
│   └── model.h5               ← PUT YOUR TRAINED MODEL HERE
│
├── sample MRI Images\
│   ├── Te-gl_0015.jpg         ← Test images (glioma)
│   ├── Te-meTr_0001.jpg       ← Test images (meningioma)
│   ├── Te-noTr_0004.jpg       ← Test images (no tumor)
│   └── Te-piTr_0003.jpg       ← Test images (pituitary)
│
├── templates\
│   └── index.html             ← Web UI (dark theme, results)
│
├── uploads\                   ← Auto-created (user uploads)
│
├── venv\                      ← Auto-created by install.bat
│
├── app.py                     ← Flask application (FIXED)
├── requirements.txt           ← Python packages (FIXED)
├── install.bat                ← Double-click to install
├── run.bat                    ← Double-click to start app
└── README.txt                 ← This file


QUICK START (Windows)
─────────────────────
STEP 1: Copy your model
        Place model.h5 into the  models\  folder

STEP 2: Install dependencies
        Double-click  install.bat
        (takes 3-5 minutes — downloads TensorFlow)

STEP 3: Run the app
        Double-click  run.bat
        Open browser: http://localhost:5000


MANUAL INSTALL (if install.bat fails)
──────────────────────────────────────
Open CMD in this folder:

  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  python app.py


ERROR FIX — TypeError: batch_shape / optional
──────────────────────────────────────────────
If you see:
  TypeError: Unrecognized keyword arguments: ['batch_shape', 'optional']

This means the old tensorflow==2.15.1 was installed.
This project uses tensorflow==2.16.2 which fixes that.

Fix:
  venv\Scripts\activate
  pip uninstall -y tensorflow tensorflow-intel keras
  pip install tensorflow==2.16.2
  python app.py


CLASSES DETECTED
────────────────
  ✅ No Tumor     (notumor)
  ⚠️ Pituitary   (pituitary)
  🔴 Glioma      (glioma)
  🔴 Meningioma  (meningioma)


DISCLAIMER
──────────
This tool is for RESEARCH PURPOSES ONLY.
Always consult a qualified medical professional
for any medical diagnosis or treatment decisions.
═══════════════════════════════════════════════════════════════
