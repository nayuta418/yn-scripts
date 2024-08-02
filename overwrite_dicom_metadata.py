#!/usr/bin/env python3

import pydicom
import argparse

def copy_ww_wl(source_file, target_file, output_file):
    # ソースDICOMファイルを読み込む
    source_dataset = pydicom.dcmread(source_file)

    # ターゲットDICOMファイルを読み込む
    target_dataset = pydicom.dcmread(target_file)

    # ソースからWWとWLを取得
    if 'WindowWidth' in source_dataset and 'WindowCenter' in source_dataset:
        source_ww = source_dataset.WindowWidth
        source_wl = source_dataset.WindowCenter

        # ターゲットにWWとWLを設定
        target_dataset.WindowWidth = source_ww
        target_dataset.WindowCenter = source_wl

        # 変更されたDICOMファイルを保存
        target_dataset.save_as(output_file)
        print(f"WW and WL from '{source_file}' have been copied to '{output_file}'.")
    else:
        print("Source DICOM file does not contain Window Width and Window Level.")

if __name__ == "__main__":
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description="Copy Window Width and Window Level from one DICOM file to another.")
    parser.add_argument("source_file", help="Path to the source DICOM file.")
    parser.add_argument("target_file", help="Path to the target DICOM file.")
    parser.add_argument("output_file", help="Path to the output DICOM file.")

    args = parser.parse_args()
    
    # WWとWLのコピーを実行
    copy_ww_wl(args.source_file, args.target_file, args.output_file)