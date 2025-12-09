"""
Quick Start Script for UTKFace Dataset Organization
Simple version with minimal configuration needed.
"""

import sys
from pathlib import Path

# Import the main organizer
try:
    from utkface_organizer import UTKFaceOrganizer
except ImportError:
    print("Error: Make sure utkface_organizer.py is in the same directory!")
    sys.exit(1)


def quick_start():
    """
    Quick start with interactive prompts
    """
    print("=" * 70)
    print("UTKFace Dataset Quick Start Organizer")
    print("=" * 70)
    
    # Get dataset path
    print("\n1. Where is your UTKFace dataset located?")
    print("   (The folder containing .jpg files like '20_0_3_20170116174525125.jpg')")
    dataset_path = input("   Path: ").strip()
    
    if not Path(dataset_path).exists():
        print(f"Error: Path '{dataset_path}' does not exist!")
        sys.exit(1)
    
    # Get output path
    print("\n2. Where should the organized dataset be saved?")
    output_path = input("   Output path (press Enter for 'organized_utkface'): ").strip()
    if not output_path:
        output_path = "organized_utkface"
    
    # Ask about preprocessing
    print("\n3. Do you want to preprocess images (resize to 224x224)?")
    preprocess = input("   (y/n, press Enter for yes): ").strip().lower()
    preprocess = preprocess != 'n'
    
    # Ask about copying images
    if preprocess:
        print("\n4. Do you want to copy images to organized Train/Val/Test folders?")
        print("   (If 'no', only CSV will be created)")
        copy_images = input("   (y/n, press Enter for yes): ").strip().lower()
        copy_images = copy_images != 'n'
    else:
        copy_images = False
    
    # Confirm
    print("\n" + "=" * 70)
    print("CONFIGURATION SUMMARY")
    print("=" * 70)
    print(f"Dataset path: {dataset_path}")
    print(f"Output path: {output_path}")
    print(f"Preprocess images: {preprocess}")
    print(f"Copy images to folders: {copy_images}")
    print(f"Train/Val/Test split: 70% / 15% / 15%")
    print("=" * 70)
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        sys.exit(0)
    
    # Run the organizer
    print("\nStarting organization...")
    print("-" * 70)
    
    try:
        # Create organizer
        organizer = UTKFaceOrganizer(dataset_path, output_path)
        
        # Scan dataset
        df = organizer.scan_dataset()
        
        if len(df) == 0:
            print("Error: No valid images found!")
            sys.exit(1)
        
        # Split dataset
        df = organizer.split_dataset(df, train_ratio=0.7, val_ratio=0.15, 
                                     test_ratio=0.15, stratify_by='age_group')
        
        # Preprocess if requested
        if preprocess:
            df = organizer.preprocess_images(df, target_size=(224, 224),
                                            copy_images=copy_images)
        
        # Save CSV
        csv_path = organizer.save_csv(df, include_optional=True)
        
        # Show statistics
        organizer.generate_summary_stats(df)
        
        print("\n" + "=" * 70)
        print("✓ SUCCESS!")
        print("=" * 70)
        print(f"CSV file: {csv_path}")
        print(f"Output folder: {output_path}")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    quick_start()
