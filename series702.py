import pydicom
import os
import argparse

def update_series_number(dicom_file, output_file, series_number):
    # DICOMファイルを読み込む
    dataset = pydicom.dcmread(dicom_file)

    # SeriesNumberを更新
    dataset.SeriesNumber = series_number

    # 変更を保存
    dataset.save_as(output_file)
    print(f"Updated SeriesNumber to {series_number} in '{output_file}'.")

if __name__ == "__main__":
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description="Update SeriesNumber in a DICOM file.")
    parser.add_argument("dicom_file", help="Path to the input DICOM file.")
    parser.add_argument("output_file", help="Path to save the updated DICOM file.")
    parser.add_argument("--series_number", type=int, default=702, help="New series number to set (default: 702).")
    
    args = parser.parse_args()
    
    # DICOMのSeriesNumberを更新
    update_series_number(args.dicom_file, args.output_file, args.series_number)