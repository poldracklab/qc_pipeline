subject_list = ['S0799AAW',
 'S9905QEN',
 'S0784SQF',
 'S0784SQF',
 'S8886NLT',
 'S0157UTB',
 'S8634TJO',
 'S2800WSU',
 'S6086STG',
 'S6086STG',
 'S9650KBD',
 'S4379IUI',
 'S3543JIU',
 'S9184VMG',
 'S6009OQW',
 'S8576CQQ',
 'S4188NBT',
 'S9161QLW',
 'S2531WXG',
 'S2059FAY',
 'S9841CIS',
 'S7064WVQ',
 'S1169XRJ',
 'S0799AAW',
 'S8417WRM',
 'S7988XOU',
 'S1543TWL']

#subject_list = [subject_list[0]]

data_dir = "/corral-repl/utexas/poldracklab/data/AA_Connectivity"
work_dir = "/scratch/03273/cmoodie"
plugin = "SLURM"
plugin_args = {"sbatch_args": "-t 00:30:00 -n 1 -p normal"}
