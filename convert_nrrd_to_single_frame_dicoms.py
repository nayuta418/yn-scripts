import SimpleITK as sitk
import pydicom
import os
import numpy as np
import argparse

def convert_nrrd_to_single_frame_dicoms(input_nrrd_file, reference_dicom_file, output_dir):
    # NRRDファイルを読み込む
    nrrd_image = sitk.ReadImage(input_nrrd_file)
    
    # 参照用のシングルフレームDICOMファイルを読み込む
    reference_dataset = pydicom.dcmread(reference_dicom_file)

    # 出力ディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)
    
    # 画像データをnumpy配列に変換
    image_array = sitk.GetArrayFromImage(nrrd_image)
    
    # 各スライスをDICOMファイルとして保存
    for i, slice_2d in enumerate(image_array):
        # 新しいDICOMデータセットを参照用データセットからコピー
        new_dataset = reference_dataset.copy()
        
        # メタデータの更新
        new_dataset.SOPInstanceUID = pydicom.uid.generate_uid()
        new_dataset.InstanceNumber = i + 1
        
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
        dicom_file = os.path.join(output_dir, f"slice_{i:03d}.dcm")
        pydicom.dcmwrite(dicom_file, new_dataset, write_like_original=False)
        print(f"Saved: {dicom_file}")

if __name__ == "__main__":
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description="Convert NRRD file to single-frame DICOM files.")
    parser.add_argument("input_nrrd_file", help="Path to the input NRRD file.")
    parser.add_argument("reference_dicom_file", help="Path to the reference single-frame DICOM file.")
    parser.add_argument("output_dir", help="Directory to save the output single-frame DICOM files.")
    
    args = parser.parse_args()
    
    # NRRDからシングルフレームDICOMへの変換を実行
    convert_nrrd_to_single_frame_dicoms(args.input_nrrd_file, args.reference_dicom_file, args.output_dir)