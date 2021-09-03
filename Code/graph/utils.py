import os
import math
import Gaussian_2d, NodeDistribution, Mesh_node, Mesh_link
import node_distance, IR


def gen_graph(loc, gateway_prob, path_loss):
    # generate nodes
    Nodes = [
    Mesh_node.Node(gateway_prob, loc.iloc[i, 0], loc.iloc[i, 1], i)
    for i in range(len(loc))
    ]
    # calculate the interference range between nodes and generate links
    # Note: link (a->b) and (b->a) cannot exist at the same time
    Links = []
    for i in range(len(Nodes)):
        for j in range(len(Nodes)):
            if i >= j:
                continue
            dis = node_distance.Dis.cal_dis(Nodes[i], Nodes[j])
            #dis = math.sqrt((Nodes[i].x_pos - Nodes[j].x_pos)**2+(Nodes[i].y_pos - Nodes[j].y_pos)**2)
            # node interference range
            nir = IR.Node_IR(Nodes[i], Nodes[j], path_loss)
            node_ir = nir.ir
            if node_ir >= dis:
                Links.append(Mesh_link.Link(Nodes[i], Nodes[j], dis))
                Nodes[i].out_neighbours.append(j)
                Nodes[j].in_neighbours.append(i)
    return Nodes, Links


def gen_conflict_graph(links, interference_range):
    c_links = []
    for i in range(len(links)):
        for j in range(len(links)):
            if i >= j:
                continue

            dis = node_distance.Dis.cal_dis_link(links[i], links[j])
            if interference_range >= dis:
                c_links.append(Mesh_link.Link(links[i], links[j], dis))
                links[i].out_neighbours.append(j)
                links[j].in_neighbours.append(i)
    return c_links


def cal_fni(c_links, interference_range):
    interf = 0
    for l in c_links:
        diff = abs(l.node1.channel - l.node2.channel)
        if diff > 4:
            continue
        else:
            interf += (l.node1.busy_idle_ratio * l.node2.busy_idle_ratio *
                (1 - l.distance / interference_range) * (1 - diff / 4))

    total_i = len(c_links)
    if total_i == 0 and interf == 0:
        return 0
    else:
        return interf / total_i


def mkdir(folder, recurse=True):
    """ mkdir, make parent directory if not exist
    """
    if folder != '' and not os.path.exists(folder):
        if recurse:
            mkdir(os.path.dirname(folder), recurse=recurse)
        os.mkdir(folder)
