#!/usr/bin/env python3

import shutil
import os
import argparse

def copy_file_to_matching_directory(source_base_dir, destination_base_dir, file_name):
    # ソースディレクトリ内のすべてのディレクトリを取得
    source_directories = [d for d in os.listdir(source_base_dir) if os.path.isdir(os.path.join(source_base_dir, d))]

    for directory in source_directories:
        source_file = os.path.join(source_base_dir, directory, file_name)
        destination_dir = os.path.join(destination_base_dir, directory)
        destination_file = os.path.join(destination_dir, file_name)
        
        # ソースファイルが存在する場合のみ処理を行う
        if os.path.exists(source_file):
            # コピー先のディレクトリが存在しない場合は作成
            os.makedirs(destination_dir, exist_ok=True)

            # ファイルをコピー
            shutil.copy2(source_file, destination_file)
            print(f"ファイルがコピーされました: {destination_file}")

def main():
    parser = argparse.ArgumentParser(description='Copy files from source to destination directories.')
    parser.add_argument('source_base_dir', type=str, help='Source base directory')
    parser.add_argument('destination_base_dir', type=str, help='Destination base directory')
    parser.add_argument('--file_name', type=str, default='Na_correct_v4.nrrd', help='Name of the file to copy (default: Na_correct_v4.nrrd)')

    args = parser.parse_args()

    copy_file_to_matching_directory(args.source_base_dir, args.destination_base_dir, args.file_name)

if __name__ == '__main__':
    main()