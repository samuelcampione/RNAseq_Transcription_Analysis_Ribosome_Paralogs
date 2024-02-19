import subprocess
import os

ref_genome = "/Users/scampione/data/yeast_genome_ncbi/R64_index"
gtf_file = "/Users/scampione/data/yeast_genome_ncbi/genomic.gtf"


def download_sra_data(sra_accession):
    """
    * Downloads the RNA-seq data from NCBI and convert to fastq
    * Software: SRAtoolkit
    * Output: SRA file into new f"{sra_accession}" directory in current directory
    """
    # try:
    #     os.mkdir(sra_accession)
    # except FileExistsError:
    #     print("Project directory exists already")
        
    # os.chdir(sra_accession)
    subprocess.run(["prefetch", sra_accession])


def convert_sra_data(sra_accession, project_dir, paired=True):
    """
    * Downloads the RNA-seq data from NCBI and convert to fastq
    * Software: SRAtoolkit
    * Output: if paired 2 converted fastq files or if unpaired 1 fastq file into current directory
    """    
    if paired == True:
        subprocess.run(["fasterq-dump", sra_accession, "--split-files", "--threads", "8", "-O", project_dir])
    else:
        subprocess.run(["fasterq-dump", sra_accession, "--threads", "8", "-O", project_dir])


def run_fastqc(sra_accession, paired=True):
    """
    * Get quality control report on RNA reads (into current directory)
    * Software: FastQC
    * Output: if paired 2 fastq files or if unpaired 1 fastq file into current directory
    """
    if paired == True:
        subprocess.run(["fastqc", "-@ 8", f"{sra_accession}_1.fastq"])
        subprocess.run(["fastqc", "-@ 8", f"{sra_accession}_2.fastq"])
    else:
        subprocess.run(["fastqc", "-@ 8", f"{sra_accession}.fastq"])


def run_hisat2(sra_accession, paired=True):
    """
    * Align the reads to the reference genome using HISAT2 (into current directory)
    * Software: HISAT2
    * Output: aligned SAM file into current directory
    """
    if paired == True:
        subprocess.run(["hisat2", "-p", "8", "-x", ref_genome, 
                        "-1", f"{sra_accession}_1.fastq", "-2", f"{sra_accession}_2.fastq", 
                        "-S", f"{sra_accession}.sam"])
    else:
        subprocess.run(["hisat2", "8", "-x", ref_genome, 
                        "-1", f"{sra_accession}.fastq",
                        "-S", f"{sra_accession}.sam"])


def process_bam(sra_accession):
    """
    * Convert SAM to BAM, sort and index BAM file 
    * Software: SAMtools
    * Output: sorted BAM into current directory
    """
    subprocess.run(["samtools", "view", "-bS", f"{sra_accession}.sam", "-o", f"{sra_accession}.bam"])
    subprocess.run(["samtools", "sort", f"{sra_accession}.bam", "-o", f"{sra_accession}_sorted.bam"])
    subprocess.run(["samtools", "index", f"{sra_accession}_sorted.bam"])


def run_feature_counts(sra_accession, paired=True):
    """
    * Quantify the reads to get gene expression levels (into current directory)
    * Software: FeatureCounts
    * Output: gene_counts.txt & gene_counts.txt.summary into current directory
    """    
    if paired==True:
        subprocess.run(["featureCounts", "-T", "8", "-p", "-a", gtf_file, "-o", f"{sra_accession}_gene_counts.txt", f"{sra_accession}_sorted.bam"])
    else:
        subprocess.run(["featureCounts", "-T", "8", "-a", gtf_file, "-o", f"{sra_accession}_gene_counts.txt", f"{sra_accession}_sorted.bam"])



# def main():
#     sra_accession = input("Enter the SRA accession number: ")  # prompts user to enter the accession number
#     project_dir = f"/Users/scampione/Projects/Buck_Institute/RNA/{sra_accession}"
#     # os.mkdir(project_dir)  # ensure the project directory exists
#     os.chdir(project_dir) # Set the directory for project
    
#     # print(" ** Downloading SRA Data ** ")
#     download_sra_data(sra_accession, project_dir)
    
#     print(" ** Running FastQC ** ")
#     run_fastqc(sra_accession)
    
#     print(" ** Trimming Reads ** ")
#     trimmed_fastq_1 = f"{sra_accession}_1_trimmed.fastq"
#     trimmed_fastq_2 = f"{sra_accession}_2_trimmed.fastq"
#     # trim_reads_with_fastp(sra_accession, trimmed_fastq_1, trimmed_fastq_2)


#     print(" ** Running HISAT2 ** ")
#     run_hisat2(sra_accession, trimmed_fastq_1, trimmed_fastq_2)
    
#     print(" ** Processing SAM/BAM output ** ")
#     process_bam(sra_accession)
    
#     print(" ** Running FeatureCounts ** ")
#     run_feature_counts(sra_accession)



# if __name__ == "__main__":
#     main()
        

# adapter_file = "/Users/scampione/anaconda3/pkgs/trimmomatic-0.39-hdfd78af_2/share/trimmomatic-0.39-2/adapters/TruSeq3-PE-2.fa"

# def trim_reads(sra_accession, trimmed_fastq_1, trimmed_fastq_2):
#     """
#     * Trim the reads to remove adapters and low-quality sequences
#     * Software: Trimmomatic
#     """
#     subprocess.run([
#     "trimmomatic", "PE",
#     "-threads", "8",
#     f"{sra_accession}_1.fastq",
#     f"{sra_accession}_2.fastq",
#     f"{trimmed_fastq_1}", "unpaired_1.fastq",
#     f"{trimmed_fastq_2}", "unpaired_2.fastq",
#     "ILLUMINACLIP:TruSeq3-PE-2.fa/:2:30:10",
#      "LEADING:3", 
#      "TRAILING:3", 
#      "MINLEN:36"
#     ])

# def trim_reads_with_fastp(sra_accession, trimmed_fastq_1, trimmed_fastq_2):
#     """
#     Trim the reads to remove adapters and low-quality sequences using fastp.
#     """
#     # Path for output JSON and HTML reports
#     json_report = f"{sra_accession}_fastp_report.json"
#     html_report = f"{sra_accession}_fastp_report.html"

#     cmd = [
#         'fastp',
#         '-i', f"{sra_accession}_1.fastq",  # Input file for read 1
#         '-I', f"{sra_accession}_2.fastq",  # Input file for read 2
#         '-o', f"{trimmed_fastq_1}",  # Output file for trimmed read 1
#         '-O', f"{trimmed_fastq_2}",  # Output file for trimmed read 2
#         '-j', json_report,  # JSON report
#         '-h', html_report,  # HTML report
#         '-w', '8'  # Number of threads
#     ]
#     # Execute the command
#     subprocess.run(cmd)