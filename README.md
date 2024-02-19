# Investigation of yeast ribosome paralogs baseline transcription profiles using  RNA-seq data.

## Sample
- Saccharomyces cerevisiae in log growth phase in rich media
- Raw data comes from [SRR8690267](https://www.ncbi.nlm.nih.gov/sra/SRR8690267)

## Method 

*See [rna_seq_analysis.ipynb](https://github.com/samuelcampione/RNAseq_Transcription_Analysis_Ribosome_Paralogs/blob/main/rna_seq_analysis.ipynb) for workflow.*

Steps of the workflow:
- (1) Data Acquisition
- (2) Alignment with HISAT2
- (3) Post-Alignment Processing
- (4) Read Counting with featureCounts
- (5) Normalization of Read Counts
- (6) Analysis of Paralogous Genes


## Results
![tpm_across_ribosome_paralogs](https://github.com/samuelcampione/RNAseq_Transcription_Analysis_Ribosome_Paralogs/assets/138845231/3f7cf9a1-b231-491d-bd5c-6c8f955b9713)



## Code
RNA-Seq workflow for transcription analysus included here: [rna_seq_analysis.ipynb](https://github.com/samuelcampione/RNAseq_Transcription_Analysis_Ribosome_Paralogs/blob/main/rna_seq_analysis.ipynb)

RNA-Seq analysis tools: [rna_seq_counts_tools.py](https://github.com/samuelcampione/RNAseq_Transcription_Analysis_Ribosome_Paralogs/blob/main/rna_seq_counts_tools.py)

