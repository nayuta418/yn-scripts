import os
import pydicom

# ディレクトリパス
source_dir = "03"  # UIDを取得する元のDICOMファイルがあるディレクトリ
target_dir = "Na_correct_v5_NSA40"  # UIDを書き換えるDICOMファイルがあるディレクトリ

# 置き換える対象のタグ（Instance UID に関するもの）
uid_tags = [
    "SOPInstanceUID",        # SOP インスタンス UID
    "SeriesInstanceUID",     # シリーズ インスタンス UID
    "StudyInstanceUID",      # スタディ インスタンス UID
]

# UIDを格納する辞書
uid_mapping = {}

# 03ディレクトリのUIDを取得
for i in range(1, 29):  # 00001.dcm ~ 00028.dcm
    file_name = f"{i:05d}.dcm"  # 5桁のゼロパディング
    source_path = os.path.join(source_dir, file_name)
    
    if os.path.exists(source_path):
        ds = pydicom.dcmread(source_path)
        uid_mapping[file_name] = {tag: getattr(ds, tag, None) for tag in uid_tags}

# 04ディレクトリのDICOMファイルを修正
for i in range(1, 29):
    file_name = f"{i:05d}.dcm"
    target_path = os.path.join(target_dir, file_name)
    
    if os.path.exists(target_path) and file_name in uid_mapping:
        ds = pydicom.dcmread(target_path)
        
        # UIDを置き換える
        for tag, new_uid in uid_mapping[file_name].items():
            if new_uid:
                setattr(ds, tag, new_uid)
        
        # 変更を保存（上書き）
        ds.save_as(target_path)
        print(f"Updated UID in {file_name}")

print("UID replacement completed.")