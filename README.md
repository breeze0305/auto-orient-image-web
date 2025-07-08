# 圖片 EXIF 批次移除與自動重新命名工具

本專案提供一個簡易的 Flask 網頁服務，讓使用者能夠批次上傳圖片，自動移除 EXIF 資訊，並將圖片重新命名後打包下載。支援常見圖片格式以及 `.heic` 格式。

## 🖼️ 功能簡介

* ✅ 支援多檔圖片同時上傳
* ✅ 自動移除 EXIF 資訊（包含方向、GPS 等敏感資料）
* ✅ 圖片自動重新命名為 `picture_00001`\~`picture_XXXXX`
* ✅ 處理完成後自動提供 ZIP 檔下載
* ✅ 支援 `.jpg`, `.png`, `.heic` 等格式
* ✅ 顯示處理進度條

## 📸 使用畫面

Web 介面簡潔明瞭，使用者只需拖曳圖片上傳，即可開始處理：

> （可於此加入介面預覽圖或影片教學連結）

## 🚀 快速使用方式（Docker 版本）

若你不想手動安裝環境，可直接使用 Docker Image：

```bash
docker pull breeze0305/auto-orient-image-web:latest

docker run -it --rm -p 8000:22000 breeze0305/auto-orient-image-web
```

然後在瀏覽器輸入 `http://localhost:8000` 即可使用

> ❗ 請記得將 `-p` 指定的 port `8000` 替換為你希望對外開放的 port，內部 port 固定為 `22000`

## 🔧 安裝與執行（本機環境）

1. 下載專案並安裝依賴：

   ```bash
   git clone https://github.com/yourname/remove-exif-tool.git
   cd remove-exif-tool
   pip install -r requirements.txt
   ```

2. 啟動 Flask 應用程式：

   ```bash
   python app.py
   ```

3. 打開瀏覽器輸入 `http://127.0.0.1:5000` 即可使用

## 📂 專案結構

```
.
├── app.py             # Flask 主程式
├── index.html         # 前端介面（bootstrap + JS）
├── requirements.txt   # 所需套件清單
```

## 📦 主要套件

* [Flask](https://flask.palletsprojects.com/) - Web 框架
* [Pillow](https://pillow.readthedocs.io/) - 圖片處理
* [pillow-heif](https://github.com/carsales/pillow-heif) - 支援 HEIC 圖片格式


## 🧑‍💻 作者

本專案由 \[breeze] 開發，如需合作或建議請聯繫 [benfeng99@gmail.com](mailto:benfeng99@gmail.com)

---

> Docker Hub 位置：[https://hub.docker.com/repository/docker/breeze0305/auto-orient-image-web](https://hub.docker.com/repository/docker/breeze0305/auto-orient-image-web)
