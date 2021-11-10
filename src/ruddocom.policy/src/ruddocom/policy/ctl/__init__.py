#!/usr/bin/env python

import os


def createsite(adjustedzope2cmd, unused_extra_cmdline_args):
    embedded = os.path.join(os.path.dirname(__file__), "createsite_embedded.py")
    adjustedzope2cmd.options.program += ["upgrader"]
    adjustedzope2cmd.options.args = ["-c", embedded] + adjustedzope2cmd.options.args[1:]
    return adjustedzope2cmd.do_run("")
