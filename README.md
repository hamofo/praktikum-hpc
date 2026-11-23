# CT-RATE Report Analysis and Data Preparation

This project prepares CT-RATE radiology reports and metadata for future natural-language retrieval experiments. It covers data ingestion, exploratory reporting style analysis, text normalisation, interview-derived query templates, and database export.

An LLM-based retrieval system was not implemented or evaluated.

## Work packages

| WP | Notebook | Purpose |
|---|---|---|
| WP1 | `WP1/wp1_data_ingestion.ipynb` | Load and combine reports, metadata, and abnormality labels; inspect data quality |
| WP2 | `WP2/wp2_hybrid.ipynb` | Deduplicate reports by study and explore reporting style variation |
| WP3 | `WP3/wp3_normalisation.ipynb` | Add normalised findings and impressions while preserving the original text |
| WP4 | `WP4/wp4_prompt_library.ipynb` | Document two interviews and analyse the query template library |
| WP5 | `WP5/wp5_data_export.ipynb` | Export selected data and summarise results and limitations |

The WP folders also contain figures and supporting files:
- WP2: `style_profiles.txt`
- WP3: `lexical_mappings.json` and `spelling_corrections.json`
- WP4: `pacs_prompt_library.json`

## Main results

- WP1: 47,119 retained training entries with 66 columns.
- WP2: 24,113 study-level reports after removing 23,006 duplicate reconstruction entries.
- WP2: 16 exploratory reporting style groups, based on recurring trachea phrases and BiomedBERT embeddings.
- WP3: 19 lexical mapping groups and 21 spelling correction rules.
- WP3: 69.3% of findings and 70.1% of impressions changed beyond lowercasing.
- WP4: 15 interview-derived query templates across seven categories.
- WP5: 24,113 rows and 20 columns exported as Parquet and CSV.

The Parquet export occupies approximately 22.2 MiB, compared with 74.8 MiB for the same table in CSV format: a 70.3% reduction.

## Data access

The source dataset is available at:
https://huggingface.co/datasets/ibrahimhamamci/CT-RATE

Access requires a Hugging Face account and compliance with the dataset's access conditions. WP1 reads authentication from the `HF_TOKEN` environment variable. Do not store tokens in notebooks or commit them to Git.

Generated datasets and model caches are not included in the repository. Running the notebooks creates these files locally.

## Environment

The notebooks were run with Python 3.10.19 in a Conda environment.

Main dependencies:
- `datasets` and `huggingface_hub`
- `pandas` and `numpy`
- `matplotlib` and `seaborn`
- `scikit-learn`
- `torch` and `transformers`
- `gensim`
- `pyarrow`
- `ipykernel`

WP2 uses the model:
`microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext`

A CUDA-capable GPU accelerates embedding computation. The notebook also supports CPU execution. Initial runs require network access to download the dataset and pretrained model.

## Running the notebooks

1. Install the dependencies and select the intended Python kernel.
2. Configure `HF_TOKEN` in your environment.
3. Run WP1 through WP5 in order.
4. Use each notebook's own WP folder as its working directory, since paths are relative to that folder.
5. Keep the supporting JSON files in their existing locations.

WP4 loads the existing prompt library; it does not recreate the interview material.

WP2 caches embeddings together with their matching inputs. The cache is reused only when the recorded model, input texts, report order, and embedding shape match.

Main generated data files:
- `data/ctrate_train_combined.csv`
- `WP2/df_wp2_final.csv`
- `data/ctrate_train_normalised.csv`
- `data/ctrate_llm_database.parquet`
- `data/ctrate_llm_database.csv`

## Export contents and checks

The final export includes identifiers, original and normalised report text, selected demographic and acquisition metadata, and exploratory style-group assignments.

Original report text is retained alongside normalised text. The abnormality labels remain in upstream datasets but are not included in the final selected export.

After reloading, the Parquet export was checked for equality of values, column order, and data types. CSV checks covered dimensions, column order, identifiers, and original and normalised findings and impressions.

## Limitations

- The style groups are exploratory and do not identify individual annotators.
- Clinical content may influence clustering despite masking; embeddings use at most 256 input tokens.
- Lexical mappings require contextual review. In particular, mapping infiltrate/infiltration variants to `lung_opacity` remains provisional.
- Change rates do not demonstrate clinical correctness or improved retrieval.
- The prompt library reflects two interview perspectives and has not been validated as a retrieval benchmark.
- `SliceThickness` is absent from the loaded tables; `ZSpacing` is not treated as an equivalent substitute.
- Study-level deduplication retains one reconstruction per study, which limits protocol-specific queries.
- Retrieval performance and longitudinal query feasibility have not been evaluated.

## References

- CT-RATE: https://arxiv.org/abs/2403.17834
- Biomedical language model pretraining: https://arxiv.org/abs/2007.15779
- FastText: https://doi.org/10.1162/tacl_a_00051
