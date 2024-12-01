#!/usr/bin/env python3

import os
import sys
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm

def main(score_file, ld_file, pick_string, out_reld):
    # Load score file and create an ID column
    all_score = pd.read_table(score_file)
    all_score['id'] = all_score['chr'].astype(str) + '_' + all_score['pos'].astype(str)
    all_score = all_score.set_index('id')

    # Filter relevant columns based on the pick_string
    pick = [True if pick_string in col else False for col in all_score.columns]
    sub_score = all_score.iloc[:, pick].mean(1)
    sub_score = np.abs(sub_score)
    sub_score = {k:v for k,v in zip(sub_score.index, sub_score.values)}

    RExLD = dict()
    LD = dict()

    # Process the LD file
    with open(ld_file, "r") as file:
        for i, line in tqdm(enumerate(file)):
            if i == 0:
                continue  # Skip header
            tokens = line.strip().split()
            a_id = tokens[0] + '_' + tokens[1]
            b_id = tokens[3] + '_' + tokens[4]

            # Update RExLD and LD dictionaries
            if a_id not in RExLD:
                RExLD[a_id] = sub_score.get(a_id, 0) + float(tokens[6]) * sub_score.get(b_id, 0)
                LD[a_id] = 1 + float(tokens[6])
            else:
                RExLD[a_id] += float(tokens[6]) * sub_score.get(b_id, 0)
                LD[a_id] += float(tokens[6])

            if b_id not in RExLD:
                RExLD[b_id] = sub_score.get(b_id, 0) + float(tokens[6]) * sub_score.get(a_id, 0)
                LD[b_id] = 1 + float(tokens[6])
            else:
                RExLD[b_id] += float(tokens[6]) * sub_score.get(a_id, 0)
                LD[b_id] += float(tokens[6])

    # Write results to output file
    with open(out_reld, 'w') as file:
        for key, value in RExLD.items():
            ld_value = LD.get(key, 1)
            file.write(f'{key}\t{value}\t{ld_value}\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute RExLD scores")
    parser.add_argument('--score_file', type=str, required=True, help='Path to score file')
    parser.add_argument('--ld_file', type=str, required=True, help='Path to LD file')
    parser.add_argument('--pick_string', type=str, required=True, help='String to pick columns from score file')
    parser.add_argument('--out_reld', type=str, required=True, help='Output file for RExLD results')

    args = parser.parse_args()

    main(args.score_file, args.ld_file, args.pick_string, args.out_reld)


# python cli_reld.py --score_file '../chr10_lightning_danq.txt' --ld_file 'out_fn.ld' --pick_string 'ATAC_Liver' --out_reld 'reld_score_lightning_wrapper.txt'



# from tqdm import tqdm
# import numpy as np
# import pandas as pd
# import os, sys, argparse

# score_file = '../chr10_lightning_danq.txt'
# ld_file = 'out_fn.ld'
# pick_string = 'ATAC_Liver'

# out_reld = 'reld_score_lightning.txt'

# all_score = pd.read_table(score_file)
# all_score['id'] = all_score['chr'].astype(str) + '_' + all_score['pos'].astype(str)
# all_score = all_score.set_index('id')
# pick = [True if pick_string in col else False for col in all_score.columns]
# sub_score = all_score.iloc[:, pick].mean(1)
# sub_score = np.abs(sub_score)
# sub_score = {k:v for k,v in zip(sub_score.index, sub_score.values)}


# RExLD = dict()
# LD = dict()

# i = 0
# with open(ld_file, "r") as file:
#     # Iterate over each line in the file
#     for line in file:
#         if i == 0:
#             i += 1
#             continue
#         else:
#             tokens = line.strip().split()
#             a_id = tokens[0] + '_' + tokens[1]
#             b_id = tokens[3] + '_' + tokens[4]
#             if a_id not in RExLD:
#                 RExLD[a_id] = sub_score.get(a_id, 0) + float(tokens[6]) * sub_score.get(b_id, 0)
#                 LD[a_id] = 1 + float(tokens[6])
#             else:
#                 RExLD[a_id] += float(tokens[6]) * sub_score.get(b_id, 0)
#                 LD[a_id] += float(tokens[6])

#             if b_id not in RExLD:
#                 RExLD[b_id] = sub_score.get(b_id, 0) + float(tokens[6]) * sub_score.get(a_id, 0)
#                 LD[b_id] = 1 + float(tokens[6])
#             else:
#                 RExLD[b_id] += float(tokens[6]) * sub_score.get(a_id, 0)
#                 LD[b_id] += float(tokens[6])


# with open(out_reld, 'w') as file:
#     for key, value in RExLD.items():
#         ld_value = LD.get(key, 1)
#         file.write(f'{key}\t{value}\t{ld_value}\n')

