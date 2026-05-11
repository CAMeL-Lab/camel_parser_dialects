# camel_parser_dialects

**CamelParser-Dialects** is a state-of-the-art dependency parsing model for **dialectal Arabic** and Modern Standard Arabic (MSA), designed under the **CATiB dependency formalism**.

It is based on the **biaffine attention parser** architecture introduced by [Dozat and Manning (2017)](https://openreview.net/pdf?id=Hk95PK9le), implemented using [SuPar](https://github.com/yzhangcs/parser).
The model leverages [CamelBERT-MIX](https://huggingface.co/CAMeL-Lab/bert-base-arabic-camelbert-mix), a pretrained language model trained on a large and diverse Arabic corpus.

Full details are available in our paper:
**"Parsing Arabic Dialects Revisited: New Benchmarks, Models, and Insights"**


## 📊 Model Variants
||Checkpoint|Training Data|MSA|EGY|GLF|AVG|
|:-----:|:-----|:--------|:--------|:--------|:--------|:--------|
||[`CAMeL-Lab/camelparser-dialects-MSA`](https://huggingface.co/CAMeL-Lab/camelparser-dialects-MSA)|CamelTB, PATB|87.3|73.0|73.3|77.9|
||[`CAMeL-Lab/camelparser-dialects-EGY`](https://huggingface.co/CAMeL-Lab/camelparser-dialects-EGY)|ARZTB|79.2|83.9|68.7|77.3|
||[`CAMeL-Lab/camelparser-dialects-GLF`](https://huggingface.co/CAMeL-Lab/camelparser-dialects-GLF)|CamelTB-Gumar|65.4|58.7|73.8|66.0|
||[`CAMeL-Lab/camelparser-dialects-MSA-EGY`](https://huggingface.co/CAMeL-Lab/camelparser-dialects-MSA-EGY)|CamelTB, PATB, ARZTB|87.1|84.4|70.1|79.8|
||[`CAMeL-Lab/camelparser-dialects-MSA-GLF`](https://huggingface.co/CAMeL-Lab/camelparser-dialects-MSA-GLF)|CamelTB, PATB, CamelTB-Gumar|87.2|74.4|81.0|80.9|
||[`CAMeL-Lab/camelparser-dialects-EGY-GLF`](https://huggingface.co/CAMeL-Lab/camelparser-dialects-EGY-GLF)|ARZTB, CamelTB-Gumar|80.0|83.8|79.4|81.1|
||[`CAMeL-Lab/camelparser-dialects-MSA-EGY-GLF`](https://huggingface.co/CAMeL-Lab/camelparser-dialects-MSA-EGY-GLF)|CamelTB, PATB, ARZTB, CamelTB-Gumar|87.2|84.2|80.3|83.9|

* LAS (Labeled Attachment Score) on TEST
* The recommended checkpoint is the **all-variety model (`MSA-EGY-GLF`)**, which provides the best overall cross-dialect performance.
* Model weights are compatible with [CamelParser2.0](https://github.com/CAMeL-Lab/camel_parser) and [SuPar](https://github.com/yzhangcs/parser) libarary. Please refer to these libraries to run these model checkpoints. Further documentattion will be provided shortly in this repository.

## 📚Data

The models are trained on combinations of the following treebanks:

- **CamelTB** (MSA): [camel_treebank_1.1.zip](https://sites.google.com/nyu.edu/camel-treebank/resources)
- **PATB** (Penn Arabic Treebank): [LDC2010T13](https://catalog.ldc.upenn.edu/LDC2010T13), [LDC2011T09](https://catalog.ldc.upenn.edu/LDC2011T09), [LDC2010T08](https://catalog.ldc.upenn.edu/LDC2010T08)
- **ARZTB** (Egyptian Arabic Treebank): [LDC2018T23](https://catalog.ldc.upenn.edu/LDC2018T23)
- **CamelTB-Gumar** (Gulf Arabic): [`CamelTB-Gumar.1.0.zip`](https://forms.gle/54WSUt7Z9m9vk6p69)

The preprocesessed data can be extracted using [muddler](https://github.com/CAMeL-Lab/muddler).
Once installed with `pip install muddler`, extract muddled files provided under `data/` directory with the following files.

-  **CamelTB** (MSA):
    1. Download `camel_treebank_1.1.zip` from:
        - https://sites.google.com/nyu.edu/camel-treebank/resources

    2. Run the following command to unlock the muddled file.
        ```bash
        muddler unmuddle -s camel_treebank_1.1.zip -m data/CamelTB.zip.muddle data/CamelTB.zip
        ```
    3. Unzip the file with `unzip data/CamelTB.zip -f data`

- **PATB** (Penn Arabic Treebank):
    1. Download the following files from the following LDC releases:
        - `atb1_v4_1_LDC2010T13.tgz`: https://catalog.ldc.upenn.edu/LDC2010T13
        - `atb_2_3.1_LDC2011T09.tgz`: https://catalog.ldc.upenn.edu/LDC2011T09
        - `atb3_v3_2_LDC2010T08.tgz`: https://catalog.ldc.upenn.edu/LDC2010T08

    2. Place them in a directory, e.g., `ldc_files/`

    3. Run the following command to unlock the muddled file.
        ```bash
        muddler unmuddle -s ldc_files -m data/PATB.zip.muddle data/PATB.zip
        ```
    4. Unzip the file with `unzip data/PATB.zip -d data`

- **ARZTB** (Egyptian Arabic Treebank): 
    1. Download `bolt_arz-df_LDC2018T23.tgz` from:
        - https://catalog.ldc.upenn.edu/LDC2018T23

    2. Run the following command to unlock the muddled file.
        ```bash
        muddler unmuddle -s bolt_arz-df_LDC2018T23.tgz -m data/arz_data.zip.muddle data/arz_data.zip
        ```
    3. Unzip the file with `unzip data/arz_data.zip -d data`

- **CamelTB-Gumar** (Gulf Arabic):
    1. Download `CamelTB-Gumar.1.0.zip` from:
        - https://forms.gle/54WSUt7Z9m9vk6p69

    2. Run the following command to unlock the muddled file.
        ```bash
        muddler unmuddle -s CamelTB-Gumar.1.0.zip -m data/CamelTB-Gumar_data.zip.muddle data/CamelTB-Gumar_data.zip
        ```

    3. Unzip the file with `unzip data/CamelTB-Gumar_data.zip -data`



## 📖 Citation
If you use this model, please cite:

```bibtex
@inproceedings{Elshabrawy:2026:camelparser-dialects,
    title = "{Parsing Arabic Dialects Revisited: New Benchmarks, Models, and Insights}",
    author = {Ahmed Elshabrawy and
              Go Inoue and
              Muhammed AbuOdeh and
              Nizar Habash} ,
    booktitle = {Proceedings of The 7th Workshop on Open-Source Arabic Corpora and Processing Tools (OSACT)},
    year = "2026",
    address = "Palma, Spain"
}
```