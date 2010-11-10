from __future__ import division

from sys import stderr
from math import sin, cos, atan2, log as ln

from .feynman import FeynmanLayout
from ..utils import Point2D


def get_depth(particle):
    if particle.vertex_out.connecting:
        return 0
    elif particle.descends_both:
        return 1 + min(get_depth(mother) for mother in particle.mothers)
    else:
        if particle.final_state:
            return 0
        return -1 + max(get_depth(daughter) for daughter in particle.daughters)

class PhiLayout(FeynmanLayout):

    def process(self):
        super(PhiLayout, self).process()
        incoming_counter = 0
        cx, cy = 0, 0
        DR = 50

        # create a tree that is used to generate the visuals
        coming = {}
        going = {}
        for edge in self.edges:
            coming.setdefault(edge.coming, []).append(edge)
            going.setdefault(edge.going, []).append(edge)
        print >> stderr, going

        nodes_remaining = list(self.nodes)
        item_nodes = {}
        for node in self.nodes:
            item_nodes[node.item] = node
            if not node.item in going:
                xposition = 10 * DR * 1 if incoming_counter % 2 == 0 else -1
                yposition = cy # - 10 * DR * 1 if incoming_counter % 2 == 0 else -1
                incoming_counter += 1
                node.center = Point2D(xposition, yposition)
                node.dot_args["pos"] = "%s,%s!" % node.center.tuple()
                node.dot_args["pin"] = "true"
                nodes_remaining.remove(node)

        while nodes_remaining:
            for node in list(nodes_remaining):
                pinned = [edge for edge in going[node.item] if item_nodes[edge.coming].center]
                if pinned:
                    nongluons = [p for p in pinned if not p.item.gluon]
                    if nongluons:
                        edge = nongluons[0]
                        force_scale = None
                    else:
                        edge = pinned[0]
                        force_scale = 0.1
                    #phi = edge.item.phi
                    phi = 0
                    #theta = atan2(edge.item.p[2], sin(phi)*edge.item.p[0] + cos(phi)*edge.item.p[1])
                    signum = 1 if sin(phi)*edge.item.p[0] + cos(phi)*edge.item.p[1] > 0 else -1
                    theta = atan2(edge.item.p[2], edge.item.pt * signum)
                    phi = theta
                    #scale = ln(edge.item.e)
                    scale = edge.item.e / 1000.0 + edge.item.pt * 10
                    if scale < 0.1: 
                        scale = 0.1
                    elif scale > 100:
                        scale = 100
                    if force_scale:
                        scale = force_scale
                    print >> stderr, scale

                    delta = Point2D(DR * sin(phi), DR * cos(phi)) * scale

                    node.center = item_nodes[edge.coming].center + delta
                    node.dot_args["pos"] = "%s,%s!" % node.center.tuple()
                    node.dot_args["pin"] = "true"
                    nodes_remaining.remove(node)
                    break

