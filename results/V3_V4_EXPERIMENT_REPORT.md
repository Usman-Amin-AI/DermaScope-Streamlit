# DermaScope — V3 vs V4 Controlled Experiment Record

## 1. Purpose

This experiment evaluates whether increasing the input resolution of the
EfficientNet-B0 skin-lesion classifier from 128x128 to 224x224 improves
classification performance.

V3 is the frozen baseline.

V4 changes only the input resolution while keeping the training procedure,
model architecture, dataset, split, seed, batch size, and number of epochs
constant.

The experiment was completed before making further application changes.

---

## 2. Dataset

- Dataset: DermaMNIST
- Source: MedMNIST
- Task: 7-class skin-lesion image classification
- Train split: 7,007 images
- Validation split: 1,003 images
- Test split: 2,005 images
- Training class counts:
  - Actinic keratoses / intraepithelial carcinoma: 228
  - Basal cell carcinoma: 359
  - Benign keratosis-like lesions: 769
  - Dermatofibroma: 80
  - Melanoma: 779
  - Melanocytic nevi: 4,693
  - Vascular lesions: 99

Important limitation: DermaMNIST contains dermoscopic lesion images. It is
not a dataset of arbitrary smartphone skin photographs. Therefore the
prototype should describe its supported input as dermoscopic images.

---

## 3. Model

Architecture:

- EfficientNet-B0
- ImageNet pretrained initialization
- Final classifier replaced with a 7-class output layer
- Full-model fine-tuning
- PyTorch / torchvision

Training strategy:

- Class-balanced WeightedRandomSampler
- CrossEntropyLoss
- AdamW
- Actual optimizer learning rate: 0.0001
- Weight decay: 0.0001
- Seed: 42
- Device: CPU
- Batch size: 32
- Epochs: 5
- Workers: 2

Training augmentation:

- Resize
- Random horizontal flip
- Random vertical flip
- Random rotation up to 15 degrees
- ColorJitter:
  - brightness 0.15
  - contrast 0.15
  - saturation 0.10
- ImageNet normalization

---

## 4. Controlled Variable

The primary experimental variable is input resolution.

| Configuration | Input Resolution |
|---|---:|
| V3 baseline | 128x128 |
| V4 experiment | 224x224 |

All other major training settings were held constant.

The V4 experiment therefore evaluates the effect of increasing spatial
input resolution rather than combining multiple changes.

---

## 5. V3 Baseline

Best validation accuracy:

- 0.7727

Final test results:

| Metric | V3 |
|---|---:|
| Accuracy | 0.7666 |
| Macro Precision | 0.6080 |
| Macro Recall | 0.7786 |
| Macro F1 | 0.6729 |
| Correct | 1537 |
| Incorrect | 468 |
| Mean confidence | 0.7872 |

Per-class F1:

| Class | F1 |
|---|---:|
| Actinic keratoses / intraepithelial carcinoma | 0.5568 |
| Basal cell carcinoma | 0.6870 |
| Benign keratosis-like lesions | 0.6137 |
| Dermatofibroma | 0.6792 |
| Melanoma | 0.5527 |
| Melanocytic nevi | 0.8704 |
| Vascular lesions | 0.7500 |

V3 checkpoint:

`models/best_efficientnet_b0_dermamnist.pt`

V3 checkpoint SHA-256:

`69b3746bae537da12734a884fd5f93f9f83443f5cc0ffc24ef0cecec19523179`

The V3 baseline is associated with the previously created
`fyp-baseline-v1` tag and must not be modified.

---

## 6. V4 Experiment

V4 configuration:

- EfficientNet-B0
- Full fine-tuning
- ImageNet initialization
- Same DermaMNIST dataset and split
- Same class-balanced sampler
- Same CrossEntropyLoss
- Same AdamW optimizer
- Same actual learning rate: 0.0001
- Same weight decay: 0.0001
- Same seed: 42
- Same batch size: 32
- Same epochs: 5
- Same augmentation
- Changed input resolution: 224x224

Best validation accuracy:

0.8415

Final test results:

| Metric | V4 |
|---|---:|
| Accuracy | 0.8259 |
| Macro Precision | 0.7214 |
| Macro Recall | 0.8265 |
| Macro F1 | 0.7637 |
| Correct | 1656 |
| Incorrect | 349 |
| Mean confidence | 0.8441 |

Per-class F1:

| Class | V3 | V4 | Change |
|---|---:|---:|---:|
| Actinic keratoses / intraepithelial carcinoma | 0.5568 | 0.6939 | +0.1371 |
| Basal cell carcinoma | 0.6870 | 0.8017 | +0.1147 |
| Benign keratosis-like lesions | 0.6137 | 0.7086 | +0.0949 |
| Dermatofibroma | 0.6792 | 0.7826 | +0.1034 |
| Melanoma | 0.5527 | 0.6162 | +0.0635 |
| Melanocytic nevi | 0.8704 | 0.9023 | +0.0319 |
| Vascular lesions | 0.7500 | 0.8406 | +0.0906 |

---

## 7. Overall Comparison

| Metric | V3 128px | V4 224px | Improvement |
|---|---:|---:|---:|
| Accuracy | 0.7666 | 0.8259 | +0.0593 |
| Macro Precision | 0.6080 | 0.7214 | +0.1134 |
| Macro Recall | 0.7786 | 0.8265 | +0.0479 |
| Macro F1 | 0.6729 | 0.7637 | +0.0908 |
| Correct predictions | 1537 | 1656 | +119 |
| Incorrect predictions | 468 | 349 | -119 |

The V4 model improved all four primary test metrics.

Accuracy increased by 5.93 percentage points.

Macro Precision increased by 11.34 percentage points.

Macro Recall increased by 4.79 percentage points.

Macro F1 increased by 9.08 percentage points.

These results support selecting V4 as the stronger experimental model.

---

## 8. V4 Confidence Analysis

The confidence analysis used the model's softmax output.

This confidence is not a calibrated clinical probability.

| Threshold | Accepted | Coverage | Accuracy |
|---:|---:|---:|---:|
| 0.50 | 1884 | 0.9397 | 0.8487 |
| 0.60 | 1711 | 0.8534 | 0.8802 |
| 0.70 | 1530 | 0.7631 | 0.9065 |
| 0.80 | 1360 | 0.6783 | 0.9353 |
| 0.90 | 1127 | 0.5621 | 0.9645 |

Increasing the acceptance threshold reduced coverage while increasing
test-set accuracy among accepted predictions.

However, V4 still produced 40 test-set errors with softmax confidence
greater than or equal to 0.90.

Therefore confidence thresholds should be treated as an uncertainty-handling
mechanism, not as proof of clinical reliability.

---

## 9. V4 High-Confidence Error Examples

Examples of high-confidence errors include:

- True benign keratosis-like lesion → predicted actinic keratoses /
  intraepithelial carcinoma, confidence 0.9951
- True melanocytic nevi → predicted basal cell carcinoma, confidence 0.9930
- True benign keratosis-like lesion → predicted basal cell carcinoma,
  confidence 0.9923
- True melanoma → predicted actinic keratoses / intraepithelial carcinoma,
  confidence 0.9922
- True benign keratosis-like lesion → predicted basal cell carcinoma,
  confidence 0.9914

These examples demonstrate why the system must not present model predictions
as definitive medical diagnoses.

---

## 10. V4 Checkpoint

Checkpoint:

`models/v4_efficientnet_b0_dermamnist_224.pt`

SHA-256:

`6635b008476be869cefcc7ca550f7c2a7b8d8819c27624c65b7f82c906ce6af9`

The checkpoint was renamed from the temporary `_160` filename to `_224`.
The SHA-256 hash remained identical after the rename.

---

## 11. Evaluation Artifacts

V4 final validation artifacts:

- `results/final_validation_v4/final_validation.json`
- `results/final_validation_v4/final_validation_report.txt`
- `results/final_validation_v4/confusion_matrix.csv`
- `results/final_validation_v4/high_confidence_errors.json`

V4 training metadata:

- `results/v4_training_config_160.json`

The training metadata filename contains `_160` because the training script
was initially prepared with a temporary filename before the supported
224x224 experiment was executed. The recorded image_size inside the JSON is
224.

---

## 12. Learning-Rate Metadata Note

The training configuration JSON records:

`"learning_rate": 0.001`

However, inspection of the actual training implementation shows that the
AdamW optimizer was instantiated with:

`lr=1e-4`

Therefore the actual optimizer learning rate used by both V3 and V4 was
0.0001.

The JSON field is a metadata-recording inconsistency and does not represent
the optimizer value actually used during training.

For this experiment record, the executable training code is treated as the
authoritative source for the optimizer setting.

---

## 13. Experimental Conclusion

V4 is the stronger model under the tested configuration.

Increasing input resolution from 128x128 to 224x224 while keeping the rest
of the experiment controlled produced:

- higher validation accuracy,
- higher test accuracy,
- higher macro precision,
- higher macro recall,
- higher macro F1,
- improved F1 for all seven classes.

Therefore V4 is selected as the current experimental model for subsequent
application integration.

The result does not establish clinical validity.

The model remains an educational skin-lesion classification prototype,
evaluated on the DermaMNIST test split.

---

## 14. Freeze Boundary

This document freezes the V3→V4 experimental comparison.

The following must remain unchanged for reproducibility:

1. V3 baseline checkpoint.
2. `fyp-baseline-v1` tag.
3. V3 final validation artifacts.
4. V4 checkpoint.
5. V4 final validation artifacts.
6. Reported V3/V4 metrics.
7. Dataset split used for evaluation.

Future application work may change the UI, inference integration, image
quality handling, explainability presentation, and surrounding software,
but must not silently alter these frozen experimental results.

Any future model-training experiment must receive a new version identifier
and a separate evaluation record.
