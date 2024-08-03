#!/usr/bin/env python

import os
import re

def list_sequential_files(directory, suffix=".dcm"):
    # 指定したディレクトリ内のファイルをリストする
    all_files = os.listdir(directory)

    # サフィックスを持つファイルのみをフィルタ
    sequential_files = [f for f in all_files if f.endswith(suffix)]

    # 数値部分を抽出してソート
    sequential_files.sort(key=lambda f: int(re.search(r'\d+', f).group()))

    return sequential_files

# ディレクトリのパスを指定
directory_path = "."

# 関数を実行してファイルをリスト化
files_list = list_sequential_files(directory_path)

# 結果を表示
print(files_list)