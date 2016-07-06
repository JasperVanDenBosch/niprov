

def inheritFrom(provenance, parentProvenance):
    inheritableFields = [
    'acquired',
    'subject',
    'protocol',
    'technique',
    'repetition-time',
    'epi-factor',
    'magnetization-transfer-contrast',
    'diffusion',
    'echo-time',
    'flip-angle',
    'inversion-time',
    'duration',
    'subject-position',
    'water-fat-shift',
    ]
    for field in inheritableFields:
        if field in parentProvenance:
            provenance[field] = parentProvenance[field]
    return provenance
