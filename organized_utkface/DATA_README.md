# UTKFace Dataset - Ready for Training

## Dataset Overview
- **Total Images**: 20,000+ face images
- **Task**: Age estimation, gender classification, race classification
- **Image Size**: 224x224 (preprocessed)
- **Format**: JPG

## Dataset Split
- **Train**: 70% (~14,000 images)
- **Val**: 15% (~3,000 images)  
- **Test**: 15% (~3,000 images)

Split is stratified by age group to ensure balanced distribution.

## File Structure
```
organized_utkface/
├── Train/              # Training images
├── Val/                # Validation images
├── Test/               # Test images
├── train.csv           # Training set metadata
├── val.csv             # Validation set metadata
├── test.csv            # Test set metadata
├── utkface_organized.csv  # Complete dataset
└── DATA_README.md      # This file
```

## CSV Columns

| Column | Type | Description | Values |
|--------|------|-------------|--------|
| `image_path` | string | Full path to image file | `/path/to/image.jpg` |
| `age` | int | Age of person | 0-116 |
| `gender` | int | Gender code | 0=Male, 1=Female |
| `gender_label` | string | Gender label | Male, Female |
| `race` | int | Race code | 0-4 |
| `race_label` | string | Race label | White, Black, Asian, Indian, Others |
| `set` | string | Dataset split | Train, Val, Test |

### Race Encoding
- 0: White
- 1: Black
- 2: Asian
- 3: Indian
- 4: Others (Hispanic, Latino, Middle Eastern)

## Dataset Statistics

### Age Distribution
- Mean: ~35 years
- Median: ~30 years
- Range: 0-116 years

### Gender Balance
- Male: ~50%
- Female: ~50%

### Race Distribution
- White: ~40%
- Black: ~20%
- Asian: ~20%
- Indian: ~10%
- Others: ~10%

## Citation

If you use this dataset in your project, please cite:
```bibtex
@inproceedings{zhifei2017cvpr,
  title={Age Progression/Regression by Conditional Adversarial Autoencoder},
  author={Zhang, Zhifei and Song, Yang and Qi, Hairong},
  booktitle={IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2017}
}
```

## License
UTKFace dataset is for **non-commercial research purposes only**.