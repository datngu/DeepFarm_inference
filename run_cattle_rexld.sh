#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --nodes=1                
#SBATCH --job-name=reld-cat   
#SBATCH --mem=4G                
#SBATCH --partition=gpu
#SBATCH --mail-user=nguyen.thanh.dat@nmbu.no
#SBATCH --mail-type=ALL


module load Nextflow/24.04.2
module load singularity/rpm



export NXF_SINGULARITY_CACHEDIR=/mnt/users/ngda/sofware/singularity
export TOWER_ACCESS_TOKEN=eyJ0aWQiOiA3OTAxfS4xNGY5NTFmOWNiZmEwNjZhOGFkYzliZTg3MDc4YWI4ZTRiYTk4ZmI5


SPEC='cattle'

vcf_dir=/mnt/ScratchProjects/Aqua-Faang/dat_projects/vip_nf/data_vcf
model_dir="/mnt/ScratchProjects/Aqua-Faang/dat_projects/dl_project/analysis_paper/selected_models"
model="${model_dir}/${SPEC}_DanQ.h5"

#genome='/mnt/users/ngda/genomes/pig/Sus_scrofa.Sscrofa11.1.dna.toplevel.fa'
genome='/mnt/users/ngda/genomes/cattle/Bos_taurus.ARS-UCD1.2.dna_sm.toplevel.fa'
#genome='/mnt/users/ngda/genomes/chicken/chromosomes_1_to_28_and_MT.fa'
#genome='/mnt/users/ngda/genomes/atlantic_salmon/Salmo_salar.Ssal_v3.1.dna_sm.toplevel.fa'

col_file="$PWD/data/col_files/${SPEC}_colnames.txt"

chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
random_chars=$(printf "%s" "${chars:RANDOM%${#chars}:1}${chars:RANDOM%${#chars}:1}")

nextflow run main_RExLD.nf -resume \
    -w "work_dir_reld" \
    -name "RExLD_${SPEC}_keras_${random_chars}" \
    --col_file "$col_file" \
    --model "$model" \
    --vcfs "$vcf_dir/${SPEC}/chr25.vcf.gz" \
    --genome "$genome" \
    -with-tower