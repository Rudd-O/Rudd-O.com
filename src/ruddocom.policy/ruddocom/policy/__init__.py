# -*- extra stuff goes here -*-

import os
import ruddocom.policy.workarounds


def _func(fname, adjustedzope2cmd, unused_extra_cmdline_args):
    embedded = os.path.join(os.path.dirname(__file__), "%s_embedded.py" % fname)
    adjustedzope2cmd.options.program += [fname]
    adjustedzope2cmd.options.args = ["-c", embedded] + adjustedzope2cmd.options.args[1:]
    return adjustedzope2cmd.do_run("")


def export(adjustedzope2cmd, unused_extra_cmdline_args):
    return _func("export", adjustedzope2cmd, unused_extra_cmdline_args)
