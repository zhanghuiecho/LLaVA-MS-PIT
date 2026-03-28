# LLaVA-MS-PIT: Multi-Modal Schema-Guided Progressive Instruction Tuning for Multi-Modal Event Extraction

[![AAAI](https://img.shields.io/badge/AAAI-2026-ff69b4)](https://ojs.aaai.org/index.php/AAAI/article/view/40770)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

&gt; Official implementation of "LLaVA-MS-PIT: Multi-Modal Schema-Guided Progressive Instruction Tuning for Multi-Modal Event Extraction" (AAAI 2026).

---

## Overview

This repository contains the code, processed resources, and training data for **multimodal event extraction (MEE)**. The project is built upon heterogeneous textual and visual event sources, including **ACE05** and **SWiG**, with additional data curation and schema alignment designed for multimodal event extraction settings.

We revisit the commonly used hard mapping from lexical words to event types in prior work and introduce a refined event-type remapping strategy for visual data. We also provide stage-wise training data for our framework.

---

## Data

### 1. Event Type Remapping

#### `new_ace_sr_mapping.txt`

This file contains the remapping between event types in the **ACE** dataset and event-related labels in the **SWiG** dataset.

The remapping is built upon the data processing pipeline from the [M2E2 repository](https://github.com/limanling/m2e2). Unlike prior work that relies on a fixed hard mapping from words to event types, we re-evaluate the event semantics of each image using **GPT-4o-based event type identification**.

This design addresses the observation that the previously adopted hard mapping strategy may introduce inaccurate alignments in visually complex or ambiguous scenarios. The new remapping provides a more reliable bridge between textual event schemas and visual event annotations.

---

### 2. SWiG-Based Multimodal Data

#### `swig_with_text_label.json`

This file contains a curated subset of images selected from the **SWiG** dataset suitable for multimodal event extraction.

For each selected image, we additionally generate:
- a textual description guided by the target event schema, and
- corresponding event annotations.

The text generation process follows a **schema-guided prompting strategy**, intended to align the generated textual content with event extraction objectives.

---

## Training Data

### Stage 1 Training Data

#### `s1_textual_event_schema_data_desensitized.json`

This file contains the **Stage 1 textual event schema training data** derived from the **ACE05** dataset.

Due to the original licensing and distribution restrictions of ACE05, the content in this file has been **desensitized**. Users with legitimate access to the original ACE05 dataset may recover the original content by replacing the desensitized fields according to the provided instance identifiers.

Each instance ID is constructed by concatenating:
- the **ACE document ID**, and
- the **sentence ID**

using `:` as the separator.

This design allows users with authorized ACE05 access to reconstruct the corresponding original examples.

#### `s1_visual_event_schema_data.json`

This file contains the **Stage 1 visual event schema training data**, constructed from the **SWiG** dataset.

It supports schema-aware learning on the visual side and serves as the visual counterpart to the textual schema training data used in Stage 1.

---

### Stage 2 Training Data

#### `s2_merge_ace_swig_sft_llava_sft_desensitized.json`

This file contains the **Stage 2 merged supervised fine-tuning data**, built from both **ACE** and **SWiG** sources for multimodal instruction tuning.

As with the Stage 1 ACE-based textual data, all ACE-related content in this file has been **desensitized** due to licensing restrictions. Users with authorized access to the original ACE05 dataset may restore the original textual content based on the corresponding instance IDs.

---

## Code

Our implementation is built upon the [LLaVA](https://github.com/haotian-liu/LLaVA) framework. We extend the original training pipeline to support multimodal event extraction with schema-guided progressive instruction tuning.

For detailed implementation of the base model architecture and training infrastructure, please refer to the [original LLaVA repository](https://github.com/haotian-liu/LLaVA).

---

### Appendix
#### `LLaVA-MS-PIT Multi-Modal Schema-Guided Progressive Instruction Tuning for Multi-Modal Event Extraction`

This attachment provides supplementary experimental analyses and additional implementation details for the project.

---

## Data Access and License Notes

### ACE05-related Data

**ACE05 is not redistributed in raw form** in this repository. Any ACE-derived data provided here have been desensitized to comply with dataset licensing and usage restrictions.

To use the ACE-based portions of our training data:

1. Obtain access to the original ACE05 dataset through the appropriate official channels;
2. Use the provided instance IDs to align the desensitized samples with your local licensed copy of ACE05.

### SWiG-related Data

The SWiG-derived files in this repository are processed resources intended for research use. Please refer to the original SWiG dataset license and terms of use before redistribution or commercial usage.

### External Resources

This project is partially built upon data processing ideas and resources from:

- [M2E2](https://github.com/limanling/m2e2)
- [SWiG](https://github.com/allenai/swig)
- [ACE2005](https://catalog.ldc.upenn.edu/LDC2006T06)
- [LLaVA](https://github.com/haotian-liu/LLaVA)

Please cite the original papers and repositories where appropriate.

---

### ACE05-related Data Notice

ACE05-related data are not included in this repository due to licensing restrictions.

To avoid potential compliance issues, we do not publicly release any ACE05-derived text data at this time. Users interested in reproducing the ACE-related parts of this project should obtain ACE05 through the official distribution channels and prepare the data locally.

### Update on ACE-related Desensitized Files

The following files are temporarily withheld from public release:

- `s2_merge_ace_swig_sft_llava_sft_desensitized.json`
- `s1_textual_event_schema_data_desensitized.json`

Although preliminary desensitization has been applied, the current version may still be insufficient for safe public dissemination under potential licensing and compliance considerations. Therefore, these files are not included in the current public repository release.

We are actively investigating improved desensitization methods and will consider releasing an updated public version once a more reliable solution is available.

## License

This project is released under the **MIT License** (see [LICENSE](LICENSE)).

Please note that third-party datasets (ACE05, SWiG) are subject to their own original licenses. The MIT License applies to original contents released by the authors.
