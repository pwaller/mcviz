#! /usr/bin/env python2.6

# MCViz - Visualize Monte Carlo Events
# Copyright (C) 2010  Peter Waller & Johannes Ebke

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from textwrap import dedent

from . import log; log = log.getChild(__name__)

from . import EventGraph, EventParseError, GraphWorkspace, FatalError, parse_options

from .logger import get_logger_level, log_level
from .utils import Units
from .utils.timer import Timer; timer = Timer(log, log.VERBOSE)


def run(args, argv):

    # Activate the python debugger if requested
    if args.debug:
        from IPython.Shell import IPShellEmbed
        ip = IPShellEmbed(["-pdb"], rc_override=dict(quiet=True))

    if not args.filename:
        log.fatal("Please specify an HepMC file or Pythia log file to run on. "
                  "Use --help for help.")
        raise FatalError

    log.info("MCViz Copyright (C) 2010 Peter Waller & Johannes Ebke")
    log.info("Licensed under GNU AGPL version 3. "
             "Please see http://mcviz.net/license.txt")
    
    #if args.units:
    #    units = Units(args.units)
    #else:
    #    units = Units()

    filename = args.filename
    log.verbose('trying to read event from "%s"' % filename)
    with timer('event from "%s"' % filename):
        try:
            event_graph = EventGraph.load(filename, args)
        except EventParseError, x:
            log.fatal("No success in reading events from %s!" % filename)
            raise FatalError
    log.info('drawing event from "%s"' % (filename))

    gw = GraphWorkspace("local", event_graph, cmdline=" ".join(argv))
    gw.load_tools(args)
    gw.run()

def real_main(argv):
    args = parse_options()
    try:
        with log_level(get_logger_level(args.quiet, args.verbose)):
            with timer("complete run"):
                run(args, argv)
        return 0
    except FatalError:
        return -1
            
def main():
    from sys import argv

    if "--profile" in argv:
        try:
            from profilestats import profile
            to_run = profile(real_main)
        except:
            print dedent("""
            #######
            Profilestats had a problem. Did you install it?
            Are you in the right environment?
            See the mcviz/utils/bootstrap_extenv.sh and source 
            mcviz/utils/extenv/bin/activate
            #######""").strip()
            raise
    else:
        to_run = real_main

    return to_run(argv)

