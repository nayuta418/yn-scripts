import pydicom
import pandas as pd
import argparse

def compare_dicom_files(file1_path, file2_path):
    # Load the two DICOM files
    dicom_file_1 = pydicom.dcmread(file1_path)
    dicom_file_2 = pydicom.dcmread(file2_path)

    # Extract the metadata from both DICOM files and compare them
    metadata_1 = {elem.tag: elem for elem in dicom_file_1}
    metadata_2 = {elem.tag: elem for elem in dicom_file_2}

    # Find differences between the two metadata dictionaries
    differences = {
        tag: (metadata_1.get(tag), metadata_2.get(tag))
        for tag in set(metadata_1) | set(metadata_2)
        if metadata_1.get(tag) != metadata_2.get(tag)
    }

    # Create a DataFrame to display differences
    differences_df = pd.DataFrame([{
        'Tag': tag,
        'Name': metadata_1.get(tag).name if metadata_1.get(tag) else metadata_2.get(tag).name,
        'File 1': metadata_1.get(tag).value if metadata_1.get(tag) else None,
        'File 2': metadata_2.get(tag).value if metadata_2.get(tag) else None,
    } for tag in differences])

    return differences_df

def main():
    parser = argparse.ArgumentParser(description="Compare metadata of two DICOM files.")
    parser.add_argument("file1", type=str, help="Path to the first DICOM file")
    parser.add_argument("file2", type=str, help="Path to the second DICOM file")

    args = parser.parse_args()

    differences_df = compare_dicom_files(args.file1, args.file2)
    print(differences_df)

if __name__ == "__main__":
    main()