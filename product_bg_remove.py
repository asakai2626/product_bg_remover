#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from ultralytics import YOLO, SAM
import torch

class ProductBackgroundRemover:
    def __init__(self):
        # MobileSAMモデルをロード
        self.sam_model = SAM('mobile_sam.pt')
        
    def remove_background(self, image_path, output_path=None):
        """
        商品画像の背景を切り抜く
        
        Args:
            image_path (str): 入力画像のパス
            output_path (str, optional): 出力画像のパス、Noneの場合は元のファイル名_nobg.pngとして保存
            
        Returns:
            PIL.Image: 背景が透明な画像
        """
        if output_path is None:
            filename = os.path.splitext(os.path.basename(image_path))[0]
            output_path = f"{filename}_nobg.png"
            
        # 画像の読み込み
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # MobileSAMで自動セグメンテーション実行
        results = self.sam_model(image_rgb, device='cpu')
        
        # マスクを取得（最も確率の高いマスクを使用）
        masks = results[0].masks.data
        if len(masks) == 0:
            print("マスクが検出されませんでした。")
            return None
        
        # 最大のマスクを選択（通常は主要な物体）
        mask_areas = [mask.sum().item() for mask in masks]
        best_mask_idx = np.argmax(mask_areas)
        mask = masks[best_mask_idx].cpu().numpy()
        
        # PILで画像処理
        image_pil = Image.fromarray(image_rgb)
        mask_binary = np.where(mask > 0, 255, 0).astype(np.uint8)
        mask_pil = Image.fromarray(mask_binary)
        
        # 透明背景の画像を作成
        result = Image.new("RGBA", image_pil.size, (0, 0, 0, 0))
        result.paste(image_pil, (0, 0), mask_pil)
        
        # 結果を保存
        result.save(output_path)
        print(f"背景除去した画像を保存しました: {output_path}")
        
        return result
    
    def visualize_result(self, original_path, output_path):
        """結果を可視化する"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # 元画像
        original = Image.open(original_path)
        ax1.imshow(original)
        ax1.set_title('元画像')
        ax1.axis('off')
        
        # 背景除去した画像
        result = Image.open(output_path)
        ax2.imshow(result)
        ax2.set_title('背景除去結果')
        ax2.axis('off')
        
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='商品画像の背景を除去するツール')
    parser.add_argument('input', help='入力画像のパス')
    parser.add_argument('--output', help='出力画像のパス (指定がない場合は入力ファイル名_nobg.png)')
    parser.add_argument('--visualize', action='store_true', help='処理結果を表示する')
    
    args = parser.parse_args()
    
    # モデルのダウンロードと背景除去の実行
    remover = ProductBackgroundRemover()
    output_path = args.output
    
    if output_path is None:
        filename = os.path.splitext(os.path.basename(args.input))[0]
        output_path = f"{filename}_nobg.png"
    
    # 背景除去を実行
    remover.remove_background(args.input, output_path)
    
    # 結果の可視化
    if args.visualize:
        remover.visualize_result(args.input, output_path)
        
    print("処理が完了しました。") 