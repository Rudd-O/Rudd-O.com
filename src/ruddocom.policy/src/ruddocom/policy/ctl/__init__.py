#!/usr/bin/env python

import os


def _func(fname, adjustedzope2cmd, unused_extra_cmdline_args):
    embedded = os.path.join(os.path.dirname(__file__), "%s_embedded.py" % fname)
    adjustedzope2cmd.options.program += [fname]
    adjustedzope2cmd.options.args = ["-c", embedded] + adjustedzope2cmd.options.args[1:]
    return adjustedzope2cmd.do_run("")


def createsite(adjustedzope2cmd, unused_extra_cmdline_args):
    return _func("createsite", adjustedzope2cmd, unused_extra_cmdline_args)


def upgrade(adjustedzope2cmd, unused_extra_cmdline_args):
    return _func("upgrade", adjustedzope2cmd, unused_extra_cmdline_args)


def import_(adjustedzope2cmd, unused_extra_cmdline_args):
    return _func("import", adjustedzope2cmd, unused_extra_cmdline_args)
