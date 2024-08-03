#!/usr/bin/env python3

# Converting NRRD files to DICOM files using pydicom and SimpleITK
# 03 Aug 2024 Y. Nakahashi

#$ python nrrd2dcm.py path/to/input.nrrd path/to/reference/dicom/dir path/to/output/dir --series_number 5000

import os
import re
import argparse
import SimpleITK as sitk
import pydicom
import numpy as np

# メタデータの参考にするDICOMファイルのリストを作成する
def list_sequential_files(directory, suffix=".dcm"):
    # 指定したディレクトリ内のファイルをリストする
    all_files = os.listdir(directory)

    # サフィックスを持つファイルのみをフィルタ
    sequential_files = [f for f in all_files if f.endswith(suffix)]

    # 数値部分を抽出してソート
    sequential_files.sort(key=lambda f: int(re.search(r'\d+', f).group()))

    # フルパスを返す
    return [os.path.join(directory, f) for f in sequential_files]

def convert_nrrd_to_single_frame_dicoms(input_nrrd_file, reference_dir, output_dir, series_number):
    # メタデータの参考にするDICOMファイルのリストを作成
    files_list = list_sequential_files(reference_dir)

    # NRRDファイルを読み込む
    nrrd_image = sitk.ReadImage(input_nrrd_file)

    # 出力ディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)

    # 画像データをnumpy配列に変換
    image_array = sitk.GetArrayFromImage(nrrd_image)

    # 各スライスをDICOMファイルとして保存
    for i, slice_2d in enumerate(image_array):
        # 各スライスに対する参照用DICOMファイルを読み込む
        reference_file = files_list[i]

        # ファイルが存在するか確認
        if not os.path.exists(reference_file):
            raise FileNotFoundError(f"Reference file not found: {reference_file}")

        reference_dataset = pydicom.dcmread(reference_file)

        # 新しいDICOMデータセットを参照用データセットからコピー
        new_dataset = reference_dataset.copy()

        # メタデータの更新
        new_dataset.SOPInstanceUID = pydicom.uid.generate_uid()
        new_dataset.InstanceNumber = i + 1
        new_dataset.SeriesNumber = series_number  # Series Numberを更新

        # 画像の属性を設定
        new_dataset.Rows, new_dataset.Columns = slice_2d.shape
        new_dataset.PixelSpacing = [format(float(nrrd_image.GetSpacing()[0]), ".10g"), format(float(nrrd_image.GetSpacing()[1]), ".10g")]
        new_dataset.SliceThickness = format(float(nrrd_image.GetSpacing()[2]), ".10g")

        # ピクセルデータを非圧縮で設定
        new_dataset.PixelData = slice_2d.astype(np.uint16).tobytes()
        new_dataset.BitsAllocated = 16
        new_dataset.BitsStored = 16
        new_dataset.HighBit = 15
        new_dataset.SamplesPerPixel = 1
        new_dataset.PhotometricInterpretation = "MONOCHROME2"

        # 転送構文の設定
        new_dataset.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

        # DICOMファイルの作成
        dicom_file = os.path.join(output_dir, f"{(i+1):05d}.dcm")
        pydicom.dcmwrite(dicom_file, new_dataset, write_like_original=False)
        print(f"Saved: {dicom_file}")

if __name__ == "__main__":
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description="Convert NRRD file to single-frame DICOM files with individual metadata.")
    parser.add_argument("input_nrrd_file", help="Path to the input NRRD file.")
    parser.add_argument("reference_dir", help="Directory containing reference DICOM files.")
    parser.add_argument("output_dir", help="Directory to save the output single-frame DICOM files.")
    parser.add_argument("--series_number", type=int, default=4000, help="Series Number for the DICOM files. Default is 4000.")

    args = parser.parse_args()

    # NRRDからシングルフレームDICOMへの変換を実行
    convert_nrrd_to_single_frame_dicoms(args.input_nrrd_file, args.reference_dir, args.output_dir, args.series_number)