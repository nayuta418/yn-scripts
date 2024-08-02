#!/usr/bin/env python3

import pydicom
import SimpleITK as sitk
import os
import argparse

def nrrd_to_dicom(input_file, output_directory):
    # Read the NRRD file
    nrrd_image = sitk.ReadImage(input_file)
    
    # Convert image to a DICOM-supported pixel type (UInt16)
    int_image = sitk.Cast(sitk.RescaleIntensity(nrrd_image), sitk.sitkUInt16)

    # Create the output directory if it does not exist
    os.makedirs(output_directory, exist_ok=True)

    # Extract base name for output file
    base_name = os.path.basename(input_file).replace('.nrrd', '')

    # Write the image as a DICOM series
    sitk.WriteImage(int_image, os.path.join(output_directory, f"{base_name}.dcm"))

    print(f"NRRD file '{input_file}' has been converted to DICOM format in '{output_directory}'.")

if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Convert NRRD file to DICOM format.")
    parser.add_argument("input_file", help="Path to the input NRRD file.")
    parser.add_argument("output_directory", help="Directory to save the output DICOM files.")
    
    args = parser.parse_args()
    
    # Execute the conversion process
    nrrd_to_dicom(args.input_file, args.output_directory)