
%matplotlib inline

import os, sys, functools
import pandas as pd
import numpy as np

def calcJobScore(jobno, df):
    return df.loc[int(jobno)].score

def sortJobScore(job_list, score_func):
    scores = [score_func(x) for x in job_list]
    indice = np.argsort(scores)[::-1]
    return [job_list[x] for x in indice]

def main(input_file, output_file, meta_file):
    
    # Load meta file and preprocess
    df_stat = pd.read_csv(meta_file)
    for col in df_stat.columns:
        if col == 'jobno':
            continue
        df_stat[col] = df_stat[col] / df_stat[col].max()
    df_stat['score'] = df_stat.clickJob + df_stat.clickSave + df_stat.clickApply
    df_stat.set_index('jobno', inplace=True)

    # Set apply function
    apply_func = functools.partial(sortJobScore,
                               score_func=functools.partial(calcJobScore, df=df_stat))
    

    df_job = pd.read_json(input_file, lines=True)
    
    df_job = df_job.filter(items=['id', 'joblist-score'])
    df_job.rename(columns={'joblist-score':'joblist'}, inplace=True)
    df_job.to_json(output_file, orient='records', lines=True)

if __name__ == "__main__" and len(sys.argv) == 2:
    
    meta = 'job-action-stat.csv'
    
    data_folder = '2018-104Hackathon-Recommendation-dataset'
    
    input_file = 'testset-click.json'
    output_file = 'submit.jsonl'
    