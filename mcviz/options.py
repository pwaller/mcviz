
from optparse import OptionParser
import sys

def get_option_parser():
    
    p = OptionParser()
    o = p.add_option
    #
    # Program control
    #
    o("-m", "--method", choices=["pt", "eta", "generations"], default="pt",
      help="Specify a method [not implemented]")

    o("-d", "--dual", action="store_true",
      help="Draw the dual of the Feynman graph [long untested]")

    o("-D", "--debug", action="store_true",
      help="Drop to ipython shell on exception")
    
    o("-L", "--limit", type=int, default=None,
      help="Limit number of particles made")
    
    o("-w", "--penwidth", choices=["pt", "off"], default="off", help="[not implemented]")
    o("-W", "--edge-weight", choices=["e", "off"], default="off", help="[not implemented]")
    
    o("-t", "--line-thickness", type=float, default=1.,
      help="Controls the thickness of the graph edges")
    
    o("-I", "--show-id", action="store_true",
      help="Controls labelling particle ids")
    
    o("-c", "--contract", action="append", type=str, default=[],
      help="Particle graph contraction. Value: 'gluballs', 'kinks'")

    o("-C", "--color-mechanism", default="color_charge",
      help="Changes the way particles are colored. "
           "Possible values: color_charge, ascendents.")
           
    o("-S", "--strip-outer-nodes", type=int, default=0, metavar="N",
      help="Performs outer node stripping N times.")
    
    #
    # Presentation
    #
    o("-E", "--layout-engine", choices=["fdp", "neato", "dot", "sfdp", "circo", "twopi"],
      help="If specified, pipes output through specified graphviz engine")
    
    o("-x", "--extra-dot", default="",
      help="Additional information to be inserted into the graph properties")
    
    o("--ratio", default="0.5", 
      help="Ratio of output graph")
      
    o("-F", "--fix-initial", action="store_true",
      help="Fix the initial vertex positions.")
      
    # These two only have an effect if fix_initial is on.
    o("--width", default=100, type=float, help="Arbitrary units.")
    o("--stretch", default=20, type=float,
      help="Ranges from 0 to width/2. 0 pulls the initial particles apart the "
           "furthest.")
    
    o("-U", "--use-unicode", action="store_true",
      help="Use unicode for labels. (Default False)")
    
    return p
    
def parse_options(argv=None):
    p = get_option_parser()

    if argv is None:
        argv = sys.argv

    if "--" in argv:
        extraopts_index = argv.index("--")
        extra_gv_options = argv[extraopts_index+1:]
        argv = argv[:extraopts_index]
    else:
        extra_gv_options = ["-Tplain"]

    result = options, args = p.parse_args(argv)
    options.extra_gv_options = extra_gv_options
        
    return result
