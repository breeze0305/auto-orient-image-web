from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image, ImageOps
import pillow_heif
pillow_heif.register_heif_opener()
import os, uuid, threading, zipfile, shutil, io
from concurrent.futures import ProcessPoolExecutor

app = Flask(__name__)
# 暫存進度 dict，key 為 job_id，value 為百分比
PROGRESS = {}

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"



def init_folder():
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)
    if os.path.exists(RESULT_FOLDER):
        shutil.rmtree(RESULT_FOLDER)
        
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(RESULT_FOLDER, exist_ok=True)

def auto_orient(args):
    idx, src_path = args
    try:
        with Image.open(src_path) as img:
            img = ImageOps.exif_transpose(img).convert("RGB")
            buffer = io.BytesIO()
            img.save(buffer, "JPEG", quality=85, optimize=True, exif=b"")
            return (idx, f"picture_{idx:05d}.jpg", buffer.getvalue())
    except Exception as e:
        return (idx, f"picture_{idx:05d}.jpg", None)

def process_images(job_id):
    upload_dir = os.path.join(UPLOAD_FOLDER, job_id)
    zip_path = os.path.join(RESULT_FOLDER, f"{job_id}.zip")
    files = sorted(os.listdir(upload_dir))
    total = len(files)

    input_args = [(i + 1, os.path.join(upload_dir, f)) for i, f in enumerate(files)]

    with ProcessPoolExecutor() as pool, zipfile.ZipFile(zip_path, 'w') as zf:
        for idx, fname, img_data in pool.map(auto_orient, input_args):
            if img_data is not None:
                zf.writestr(fname, img_data)
            PROGRESS[job_id] = int(idx / total * 100)

    PROGRESS[job_id] = 100
    shutil.rmtree(upload_dir)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def start_process():
    files = request.files.getlist("images")
    if not files:
        return jsonify({"error": "請上傳至少一張圖片"}), 400

    job_id = uuid.uuid4().hex
    save_dir = os.path.join(UPLOAD_FOLDER, job_id)
    os.makedirs(save_dir, exist_ok=True)

    for f in files:
        f.save(os.path.join(save_dir, f.filename))

    PROGRESS[job_id] = 0
    thread = threading.Thread(target=process_images, args=(job_id,))
    thread.daemon = True
    thread.start()

    return jsonify({"job_id": job_id})

@app.route("/progress/<job_id>")
def progress(job_id):
    pct = PROGRESS.get(job_id, 0)
    return jsonify({"progress": pct})

@app.route("/download/<job_id>")
def download(job_id):
    zip_path = os.path.join(RESULT_FOLDER, f"{job_id}.zip")
    if not os.path.exists(zip_path):
        return "檔案不存在或尚未產生", 404
    return send_file(zip_path, as_attachment=True, download_name="result.zip")

if __name__ == "__main__":
    init_folder()
    # 指定 port 為 22000
    # app.run(host="0.0.0.0", port=22000, debug=False)
    
    app.run(host="0.0.0.0", port=22000, debug=False)
