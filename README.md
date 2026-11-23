# CT-RATE Report Analysis and Data Preparation

This project prepares the CT-RATE radiology reports and their metadata so they can be used for natural-language retrieval experiments later on. The work covers loading the data, an exploratory look at reporting style, text normalisation, query templates based on two interviews, and a final database export.

The retrieval system itself (LLM-based) is not part of this project and was neither implemented nor evaluated.

## Work packages

| WP | Notebook | Content |
|---|---|---|
| WP1 | `WP1/wp1_data_ingestion.ipynb` | Loading and merging reports, metadata and abnormality labels; data quality checks |
| WP2 | `WP2/wp2_hybrid.ipynb` | Deduplication per study and exploration of reporting styles |
| WP3 | `WP3/wp3_normalisation.ipynb` | Normalised findings and impressions, original text kept |
| WP4 | `WP4/wp4_prompt_library.ipynb` | Documentation of two interviews and analysis of the query templates |
| WP5 | `WP5/wp5_data_export.ipynb` | Export of the selected data, summary of results and limitations |

Besides the notebooks and figures, some WP folders contain supporting files: `style_profiles.txt` (WP2), `lexical_mappings.json` and `spelling_corrections.json` (WP3), and `pacs_prompt_library.json` (WP4).

## Results

After loading, 47,119 training entries with 66 columns remain (WP1). Many of these are different reconstructions of the same study, so WP2 removes 23,006 duplicates, leaving 24,113 study-level reports. Based on recurring trachea phrases and BiomedBERT embeddings, WP2 identifies 16 exploratory reporting style groups.

For normalisation, WP3 uses 19 lexical mapping groups and 21 spelling correction rules. Apart from lowercasing, this changes 69.3% of the findings and 70.1% of the impressions.

WP4 contains 15 query templates in seven categories, derived from the interviews.

The final export in WP5 has 24,113 rows and 20 columns and is written as both Parquet and CSV. The Parquet file is about 22.2 MiB, the CSV of the same table 74.8 MiB, so Parquet is 70.3% smaller.

## Data access

The dataset is available on Hugging Face: https://huggingface.co/datasets/ibrahimhamamci/CT-RATE

You need a Hugging Face account and have to accept the dataset's access conditions. WP1 reads the token from the `HF_TOKEN` environment variable; tokens should not end up in the notebooks or in Git.

Generated datasets and model caches are not part of the repository and are created locally when the notebooks are run.

## Environment

Python 3.10.19 in a Conda environment. Main packages: `datasets`, `huggingface_hub`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `torch`, `transformers`, `gensim`, `pyarrow` and `ipykernel`.

WP2 uses `microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext`. The embeddings are much faster on a CUDA GPU, but the notebook also runs on CPU. The first run needs network access to download the dataset and the model.

## Running the notebooks

Install the dependencies, select the kernel and set `HF_TOKEN`. Then run WP1 to WP5 in order. Paths are relative to each WP folder, so that folder has to be the working directory. The JSON files should stay where they are.

WP4 only loads the existing prompt library; the interview material is not regenerated.

WP2 caches the embeddings together with their inputs. The cache is only reused if model, input texts, report order and embedding shape all match.

Main output files:

- `data/ctrate_train_combined.csv`
- `WP2/df_wp2_final.csv`
- `data/ctrate_train_normalised.csv`
- `data/ctrate_llm_database.parquet`
- `data/ctrate_llm_database.csv`

## Export contents and checks

The export contains identifiers, the original and normalised report text, selected demographic and acquisition metadata, and the style group assignments. The abnormality labels are still in the upstream datasets but were not selected for the final export.

The Parquet file was reloaded and compared with the original table (values, column order, data types). For the CSV, dimensions, column order, identifiers and the original and normalised findings and impressions were checked.

## Limitations

- The style groups are exploratory and do not correspond to individual annotators.
- Clinical content can still influence the clustering despite masking. The embeddings only see the first 256 tokens.
- The lexical mappings need to be reviewed in context. Mapping infiltrate/infiltration variants to `lung_opacity` in particular is provisional.
- The change rates say nothing about clinical correctness or better retrieval.
- The prompt library is based on only two interviews and has not been validated as a retrieval benchmark.
- `SliceThickness` is missing from the loaded tables. `ZSpacing` was not used as a replacement.
- Since only one reconstruction per study is kept, protocol-specific queries are limited.
- Retrieval performance and the feasibility of longitudinal queries were not evaluated.

## References

- CT-RATE: https://arxiv.org/abs/2403.17834
- Biomedical language model pretraining: https://arxiv.org/abs/2007.15779
- FastText: https://doi.org/10.1162/tacl_a_00051
