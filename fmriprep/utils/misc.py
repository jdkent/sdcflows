#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Miscellaneous utilities
"""


def remove_rotation_and_shear(img):
    from transforms3d.affines import decompose, compose
    import numpy as np

    T, _, Z, _ = decompose(img.affine)
    affine = compose(T=T, R=np.diag([1, 1, 1]), Z=Z)
    return img.__class__(np.asanyarray(img.dataobj), affine, img.header)


def split_and_rm_rotshear_func(in_file):
    import os
    import nibabel as nb
    from fmriprep.utils.misc import remove_rotation_and_shear
    out_files = []
    imgs = nb.four_to_three(nb.load(in_file))
    for i, img in enumerate(imgs):
        out_file = os.path.abspath('vol%04d.nii.gz' % i)
        img = remove_rotation_and_shear(
            nb.as_closest_canonical(img))
        img.to_filename(out_file)
        out_files.append(out_file)
    return out_files


def fix_multi_T1w_source_name(in_files):
    """
    Make up a generic source name when there are multiple T1s

    >>> fix_multi_T1w_source_name([
    ...     '/path/to/sub-045_ses-test_T1w.nii.gz',
    ...     '/path/to/sub-045_ses-retest_T1w.nii.gz'])
    '/path/to/sub-045_T1w.nii.gz'

    """
    import os
    from nipype.utils.filemanip import filename_to_list
    base, in_file = os.path.split(filename_to_list(in_files)[0])
    subject_label = in_file.split("_", 1)[0].split("-")[1]
    return os.path.join(base, "sub-%s_T1w.nii.gz" % subject_label)


def meepi_optimal_comb_source_name(in_files):
    """
    Create a new source name when optimally
    combining multiple multi-echo EPIs

    >>> meepi_optimal_comb_source_name([
    ...     'sub-01_run-01_echo-1_bold.nii.gz',
    ...     'sub-01_run-01_echo-2_bold.nii.gz',
    ...     'sub-01_run-01_echo-3_bold.nii.gz',])
    'sub-01_run-01_bold.nii.gz'

    """
    import os
    from nipype.utils.filemanip import filename_to_list
    base, in_file = os.path.split(filename_to_list(in_files)[0])
    entities = [ent for ent in in_file.split('_') if not ent.startswith('echo-')]
    basename = '_'.join(entities)
    return os.path.join(base, basename)


def add_suffix(in_files, suffix):
    """
    Wrap nipype's fname_presuffix to conveniently just add a prefix

    >>> add_suffix([
    ...     '/path/to/sub-045_ses-test_T1w.nii.gz',
    ...     '/path/to/sub-045_ses-retest_T1w.nii.gz'], '_test')
    'sub-045_ses-test_T1w_test.nii.gz'

    """
    import os.path as op
    from nipype.utils.filemanip import fname_presuffix, filename_to_list
    return op.basename(fname_presuffix(filename_to_list(in_files)[0],
                                       suffix=suffix))


if __name__ == '__main__':
    pass
