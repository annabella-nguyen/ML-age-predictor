"""
UTKFace Dataset Organizer
This script organizes the UTKFace dataset into a structured table and preprocesses images.
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from PIL import Image
import shutil
from sklearn.model_selection import train_test_split

class UTKFaceOrganizer:
    def __init__(self, dataset_path, output_path="organized_dataset"):
        """
        Initialize the organizer
        
        Args:
            dataset_path: Path to the downloaded UTKFace dataset folder
            output_path: Path where organized dataset will be saved
        """
        self.dataset_path = Path(dataset_path)
        self.output_path = Path(output_path)
        self.output_path.mkdir(exist_ok=True, parents=True)
        
        # Race mapping
        self.race_map = {
            0: "White",
            1: "Black", 
            2: "Asian",
            3: "Indian",
            4: "Others"
        }
        
        # Gender mapping
        self.gender_map = {
            0: "Male",
            1: "Female"
        }
    
    def parse_filename(self, filename):
        """
        Parse the UTKFace filename to extract age, gender, race
        Format: [age]_[gender]_[race]_[date&time].jpg
        
        Returns:
            dict with age, gender, race, or None if parsing fails
        """
        try:
            # Remove file extension
            name = filename.split('.')[0]
            parts = name.split('_')
            
            if len(parts) < 4:
                return None
            
            age = int(parts[0])
            gender = int(parts[1])
            race = int(parts[2])
            
            # Validate ranges
            if age < 0 or age > 116:
                return None
            if gender not in [0, 1]:
                return None
            if race not in [0, 1, 2, 3, 4]:
                return None
            
            return {
                'age': age,
                'gender': gender,
                'gender_label': self.gender_map[gender],
                'race': race,
                'race_label': self.race_map[race]
            }
        except (ValueError, IndexError):
            return None
    
    def scan_dataset(self):
        """
        Scan the dataset folder and create a dataframe with all image information
        
        Returns:
            pandas DataFrame with image information
        """
        print("Scanning dataset directory...")
        
        image_data = []
        skipped_files = []
        
        # Find all jpg images
        image_files = list(self.dataset_path.glob("**/*.jpg")) + \
                     list(self.dataset_path.glob("**/*.jpeg")) + \
                     list(self.dataset_path.glob("**/*.png"))
        
        print(f"Found {len(image_files)} image files")
        
        for img_path in image_files:
            parsed = self.parse_filename(img_path.name)
            
            if parsed is None:
                skipped_files.append(img_path.name)
                continue
            
            image_data.append({
                'filename': img_path.name,
                'image_path': str(img_path),
                'age': parsed['age'],
                'gender': parsed['gender'],
                'gender_label': parsed['gender_label'],
                'race': parsed['race'],
                'race_label': parsed['race_label']
            })
        
        if skipped_files:
            print(f"Warning: Skipped {len(skipped_files)} files that couldn't be parsed")
            print(f"First few skipped: {skipped_files[:5]}")
        
        df = pd.DataFrame(image_data)
        print(f"Successfully parsed {len(df)} images")
        
        return df
    
    def split_dataset(self, df, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, 
                     stratify_by='age_group', random_state=42):
        """
        Split dataset into train/val/test sets
        
        Args:
            df: DataFrame with image information
            train_ratio: Proportion for training set
            val_ratio: Proportion for validation set
            test_ratio: Proportion for test set
            stratify_by: Column to stratify by ('age_group', 'gender', 'race', or None)
            random_state: Random seed for reproducibility
        
        Returns:
            DataFrame with additional 'set' column
        """
        print(f"\nSplitting dataset: {train_ratio:.0%} train, {val_ratio:.0%} val, {test_ratio:.0%} test")
        
        # Create age groups for stratification if requested
        if stratify_by == 'age_group':
            df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 50, 65, 120], 
                                    labels=['0-18', '19-35', '36-50', '51-65', '66+'])
            stratify_col = df['age_group']
        elif stratify_by in df.columns:
            stratify_col = df[stratify_by]
        else:
            stratify_col = None
        
        # First split: train vs (val + test)
        train_df, temp_df = train_test_split(
            df, 
            test_size=(val_ratio + test_ratio),
            stratify=stratify_col,
            random_state=random_state
        )
        
        # Second split: val vs test
        if stratify_col is not None:
            temp_stratify = temp_df[stratify_by] if stratify_by in temp_df.columns else None
        else:
            temp_stratify = None
            
        val_df, test_df = train_test_split(
            temp_df,
            test_size=test_ratio/(val_ratio + test_ratio),
            stratify=temp_stratify,
            random_state=random_state
        )
        
        # Assign set labels
        train_df['set'] = 'Train'
        val_df['set'] = 'Val'
        test_df['set'] = 'Test'
        
        # Combine back
        result_df = pd.concat([train_df, val_df, test_df], ignore_index=True)
        
        # Remove temporary age_group column if created
        if stratify_by == 'age_group' and 'age_group' in result_df.columns:
            result_df = result_df.drop('age_group', axis=1)
        
        print(f"Train: {len(train_df)} images")
        print(f"Val: {len(val_df)} images")
        print(f"Test: {len(test_df)} images")
        
        return result_df
    
    def preprocess_images(self, df, target_size=(224, 224), normalize=True, 
                         copy_images=True, output_format='jpg'):
        """
        Preprocess images: resize, normalize, and optionally copy to organized folders
        
        Args:
            df: DataFrame with image information
            target_size: Tuple (width, height) for resizing
            normalize: Whether to normalize pixel values to [0, 1]
            copy_images: Whether to copy/save images to organized folder structure
            output_format: Output image format ('jpg', 'png')
        
        Returns:
            DataFrame with updated image paths (if copy_images=True)
        """
        print(f"\nPreprocessing images...")
        print(f"Target size: {target_size}")
        print(f"Copy images: {copy_images}")
        
        if copy_images:
            # Create folder structure
            for set_name in ['Train', 'Val', 'Test']:
                set_path = self.output_path / set_name
                set_path.mkdir(exist_ok=True)
        
        processed_df = df.copy()
        failed_images = []
        
        for idx, row in df.iterrows():
            try:
                # Load image
                img = Image.open(row['image_path'])
                
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize
                img = img.resize(target_size, Image.LANCZOS)
                
                if copy_images:
                    # Save to organized folder
                    new_filename = f"{row['filename'].split('.')[0]}.{output_format}"
                    new_path = self.output_path / row['set'] / new_filename
                    
                    img.save(new_path, quality=95)
                    processed_df.at[idx, 'image_path'] = str(new_path)
                
                if (idx + 1) % 1000 == 0:
                    print(f"Processed {idx + 1}/{len(df)} images...")
                    
            except Exception as e:
                failed_images.append((row['filename'], str(e)))
                print(f"Failed to process {row['filename']}: {e}")
        
        if failed_images:
            print(f"\nWarning: Failed to process {len(failed_images)} images")
        
        print(f"Successfully preprocessed {len(df) - len(failed_images)} images")
        
        return processed_df
    
    def save_csv(self, df, filename="utkface_organized.csv", include_optional=True):
        """
        Save the organized dataset to CSV
        
        Args:
            df: DataFrame to save
            filename: Output CSV filename
            include_optional: Whether to include gender and race columns
        """
        output_csv = self.output_path / filename
        
        # Select columns based on include_optional
        if include_optional:
            columns = ['image_path', 'age', 'gender', 'gender_label', 'race', 'race_label', 'set']
        else:
            columns = ['image_path', 'age', 'set']
        
        # Filter to only include columns that exist in df
        columns = [col for col in columns if col in df.columns]
        
        df[columns].to_csv(output_csv, index=False)
        print(f"\nSaved organized dataset to: {output_csv}")
        
        return output_csv
    
    def generate_summary_stats(self, df):
        """
        Generate and print summary statistics
        """
        print("\n" + "="*60)
        print("DATASET SUMMARY STATISTICS")
        print("="*60)
        
        print(f"\nTotal images: {len(df)}")
        
        print("\n--- Distribution by Set ---")
        print(df['set'].value_counts().sort_index())
        
        print("\n--- Age Statistics ---")
        print(f"Mean age: {df['age'].mean():.1f}")
        print(f"Median age: {df['age'].median():.1f}")
        print(f"Age range: {df['age'].min()} - {df['age'].max()}")
        
        if 'gender_label' in df.columns:
            print("\n--- Gender Distribution ---")
            for set_name in ['Train', 'Val', 'Test']:
                set_df = df[df['set'] == set_name]
                print(f"\n{set_name}:")
                print(set_df['gender_label'].value_counts())
        
        if 'race_label' in df.columns:
            print("\n--- Race Distribution ---")
            for set_name in ['Train', 'Val', 'Test']:
                set_df = df[df['set'] == set_name]
                print(f"\n{set_name}:")
                print(set_df['race_label'].value_counts())
        
        print("\n" + "="*60)


def main():
    """
    Main execution function - customize these parameters
    """
    # =========================================================================
    # CONFIGURATION - ADJUST THESE PARAMETERS
    # =========================================================================
    
    # Path to your downloaded UTKFace dataset
    DATASET_PATH = "/path/to/UTKFace"  # <-- CHANGE THIS
    
    # Output path for organized dataset
    OUTPUT_PATH = "organized_utkface"
    
    # Train/Val/Test split ratios
    TRAIN_RATIO = 0.7
    VAL_RATIO = 0.15
    TEST_RATIO = 0.15
    
    # Preprocessing options
    PREPROCESS_IMAGES = True  # Set to False to skip preprocessing
    TARGET_SIZE = (224, 224)  # Resize images to this size
    COPY_IMAGES = True  # Copy images to organized folders (set False to just create CSV)
    OUTPUT_FORMAT = 'jpg'  # 'jpg' or 'png'
    
    # CSV options
    INCLUDE_OPTIONAL = True  # Include gender and race columns
    
    # Stratification option
    STRATIFY_BY = 'age_group'  # 'age_group', 'gender', 'race', or None
    
    # =========================================================================
    
    # Create organizer
    organizer = UTKFaceOrganizer(DATASET_PATH, OUTPUT_PATH)
    
    # Step 1: Scan dataset
    df = organizer.scan_dataset()
    
    if len(df) == 0:
        print("Error: No images found! Please check your dataset path.")
        return
    
    # Step 2: Split into train/val/test
    df = organizer.split_dataset(df, TRAIN_RATIO, VAL_RATIO, TEST_RATIO, 
                                 stratify_by=STRATIFY_BY)
    
    # Step 3: Preprocess images (optional)
    if PREPROCESS_IMAGES:
        df = organizer.preprocess_images(df, target_size=TARGET_SIZE, 
                                        copy_images=COPY_IMAGES,
                                        output_format=OUTPUT_FORMAT)
    
    # Step 4: Save to CSV
    csv_path = organizer.save_csv(df, include_optional=INCLUDE_OPTIONAL)
    
    # Step 5: Generate summary statistics
    organizer.generate_summary_stats(df)
    
    print(f"\n✓ All done! Your organized dataset is in: {OUTPUT_PATH}")
    print(f"✓ CSV file: {csv_path}")


if __name__ == "__main__":
    main()
