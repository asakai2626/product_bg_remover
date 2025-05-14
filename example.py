#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用例: ProductBackgroundRemoverクラスを直接インポートして使用する方法
"""

from product_bg_remove import ProductBackgroundRemover
import os

def process_batch_images(input_dir, output_dir):
    """
    指定ディレクトリ内の全画像を処理する
    
    Args:
        input_dir (str): 入力画像が格納されているディレクトリ
        output_dir (str): 出力画像を保存するディレクトリ
    """
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 背景除去クラスのインスタンス化
    remover = ProductBackgroundRemover()
    
    # 入力ディレクトリの画像を処理
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    processed_count = 0
    
    for filename in os.listdir(input_dir):
        # 画像ファイルのみを処理
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            input_path = os.path.join(input_dir, filename)
            
            # 出力ファイル名を生成
            output_filename = f"{os.path.splitext(filename)[0]}_nobg.png"
            output_path = os.path.join(output_dir, output_filename)
            
            # 背景除去を実行
            try:
                print(f"処理中: {filename}")
                remover.remove_background(input_path, output_path)
                processed_count += 1
            except Exception as e:
                print(f"エラー ({filename}): {str(e)}")
    
    print(f"処理完了: {processed_count}枚の画像を処理しました。")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='フォルダ内の商品画像の背景を一括除去する')
    parser.add_argument('input_dir', help='入力画像のディレクトリ')
    parser.add_argument('--output_dir', help='出力画像のディレクトリ（指定がない場合は input_dir/output）')
    
    args = parser.parse_args()
    
    # 出力ディレクトリが指定されていない場合はデフォルト値を使用
    output_dir = args.output_dir
    if output_dir is None:
        output_dir = os.path.join(args.input_dir, 'output')
    
    # バッチ処理を実行
    process_batch_images(args.input_dir, output_dir) 