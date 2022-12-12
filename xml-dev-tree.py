from ctypes import c_wchar, c_int, byref, windll
from xml.dom.minidom import Document

cfg = windll.cfgmgr32

CM_DRP_DEVICEDESC = 1
CM_DRP_DRIVER = 0x0000A
NULL = 0

proc_buf = (c_wchar * 1024)()


def get_dev_desc(dev_inst):
    return proc_buf.value if cfg.CM_Get_DevNode_Registry_PropertyW(dev_inst, CM_DRP_DEVICEDESC, NULL, proc_buf, byref(c_int(1024)), 0) == 0 else None


def get_dev_id(dev_inst):
    return proc_buf.value if cfg.CM_Get_Device_IDW(dev_inst, proc_buf, byref(c_int(1024)), 0) == 0 else None


def get_dev_driver(dev_inst):
    return proc_buf.value if cfg.CM_Get_DevNode_Registry_PropertyW(dev_inst, CM_DRP_DRIVER, NULL, proc_buf, byref(c_int(1024)), 0) == 0 else None


def set_node(dev_child_id, dom, level):
    node = dom.createElement("Device")
    attr_dict = {"DevInst": str(dev_child_id.value), "Desc": get_dev_desc(dev_child_id.value), "Lev": str(level), "DevId": get_dev_id(dev_child_id.value), "Driver": get_dev_driver(dev_child_id.value)}
    [node.setAttribute(key, value) for key, value in attr_dict.items()]
    return node


def dev_child(dev_inst_in, tree, level, dom):
    dev_parent = c_int(dev_inst_in)
    dev_child_id = c_int(0)
    dev_next_child = c_int(0)
    if cfg.CM_Get_Child(byref(dev_child_id), dev_parent, 0) == 0:
        node = set_node(dev_child_id, dom, level)
        tree.appendChild(node)
        dev_child(dev_child_id.value, node, level + 1, dom)
        while cfg.CM_Get_Sibling(byref(dev_next_child), dev_child_id, 0) == 0:
            dev_child_id.value = dev_next_child.value
            node = set_node(dev_child_id, dom, level)
            tree.appendChild(node)
            dev_child(dev_child_id.value, node, level + 1, dom)


def dev_xml():
    dom = Document()
    dom.appendChild(dom.createElement("DeviceTree"))
    dev_inst = c_int(0)
    dev_inst_next = c_int(0)
    level = 0
    if cfg.CM_Locate_DevNodeW(byref(dev_inst), 0, 0) == 0:
        dom.documentElement.appendChild(set_node(dev_inst, dom, level))
        while cfg.CM_Get_Sibling(byref(dev_inst_next), dev_inst, 0) == 0:
            dev_inst.value = dev_inst_next.value
            dom.documentElement.appendChild(set_node(dev_inst, dom, level))
    for child in dom.documentElement.childNodes:
        k = int(child.getAttribute("DevInst"))
        dev_child(k, child, level + 1, dom)
    return dom.toprettyxml()


xml = dev_xml()
open("c:\\Users\\pdm\\DeviceTree.xml", "wb").write(xml.encode("utf8"))
