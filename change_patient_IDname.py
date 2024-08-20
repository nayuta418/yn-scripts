#!/usr/bin/env python3

# change_patient_IDname.py {directory}
#→directory以下のdicom file全てについて、patient ID及び patient nameをカレントディレクトリの親ディレクトリの名前に変更する

import os
import pydicom
import argparse

def update_patient_name_and_id_in_dicom(directory):
    # 指定したディレクトリ内のすべてのファイルを走査
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".dcm"):
                dicom_file_path = os.path.join(root, file_name)
                try:
                    # DICOMファイルを読み込む
                    dicom_data = pydicom.dcmread(dicom_file_path)
                    
                    # 親ディレクトリの親ディレクトリの名前を取得
                    grandparent_directory_name = os.path.basename(os.path.dirname(root))
                    
                    # DICOMのPatientNameとPatientIDを祖父ディレクトリの名前に変更
                    dicom_data.PatientName = grandparent_directory_name
                    dicom_data.PatientID = grandparent_directory_name
                    
                    # 変更をファイルに保存
                    dicom_data.save_as(dicom_file_path)
                    
                    print(f"Updated PatientName and PatientID in {dicom_file_path} to {grandparent_directory_name}")
                
                except Exception as e:
                    print(f"Failed to update {dicom_file_path}: {e}")

def main():
    # argparseを使ってコマンドライン引数をパース
    parser = argparse.ArgumentParser(description="Update DICOM PatientName and PatientID to match grandparent directory name.")
    parser.add_argument("directory", help="The directory containing DICOM files.")
    
    # 引数を取得
    args = parser.parse_args()
    
    # 関数を呼び出して処理を実行
    update_patient_name_and_id_in_dicom(args.directory)

if __name__ == "__main__":
    main()