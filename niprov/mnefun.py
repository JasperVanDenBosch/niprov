import os
from niprov.discovery import discover


def handler(text, func, out, params):
    for subj in params.subjects:
        subjrawdir = os.path.join(params.work_dir, subj, params.raw_dir)
        discover(subjrawdir)
