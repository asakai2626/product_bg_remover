# 商品画像背景除去ツール

このツールはMobile SAMを使用して商品画像から背景を自動的に除去し、透明な背景の画像を生成します。

## 機能

- 商品画像の背景を自動的に検出して除去
- 透明背景（PNG形式）での保存
- 処理結果の可視化オプション

## 必要条件

- Python 3.8以上
- 必要なライブラリ:
  - ultralytics
  - numpy
  - opencv-python (cv2)
  - matplotlib
  - PIL (Pillow)
  - torch

## インストール方法

```bash
# 必要なライブラリをインストール
pip install ultralytics pillow matplotlib
```

## 使用方法

### 基本的な使い方

```bash
python product_bg_remove.py 商品画像.jpg
```

これにより、`商品画像_nobg.png`という名前で背景が除去された画像が保存されます。

### 出力ファイル名を指定する場合

```bash
python product_bg_remove.py 商品画像.jpg --output 出力画像.png
```

### 処理結果を可視化する場合

```bash
python product_bg_remove.py 商品画像.jpg --visualize
```

## 注意事項

- 初回実行時は自動的にMobile SAMモデル（mobile_sam.pt）がダウンロードされます。
- 複雑な背景や商品が明確に区別できない画像では、結果が期待通りにならない場合があります。
- GPUがある環境ではGPUが自動的に使用されます。

## ライセンス

このプロジェクトはMITライセンスのもとで提供されています。 