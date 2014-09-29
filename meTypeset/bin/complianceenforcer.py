__author__ = "Martin Paul Eve"
__email__ = "martin@martineve.com"

from debug import Debuggable
from nlmmanipulate import *


class ComplianceEnforcer(Debuggable):
    def __init__(self, global_variables):
        self.gv = global_variables
        self.debug = self.gv.debug
        Debuggable.__init__(self, 'Compliance Enforcer')

    def run(self):
        manipulate = NlmManipulate(self.gv)

        self.debug.print_debug(self, u'Removing meTypeset specific attributes and tags')

        tree = manipulate.load_dom_tree()

        render_attributes = tree.xpath('//*[@meTypesetRender]')

        for attribute in render_attributes:
            del attribute.attrib['meTypesetRender']

        manipulate.save_tree(tree)
        self.debug.print_debug(self, u'Removing {0} meTypesetRender attributes'.format(len(render_attributes)))

        reflist_attributes = tree.xpath('//*[@reflist]')

        for attribute in  reflist_attributes:
            del attribute.attrib['reflist']

        manipulate.save_tree(tree)
        self.debug.print_debug(self, u'Removing {0} reflist attributes'.format(len(reflist_attributes)))

        unlinked_xrefs = tree.xpath('//xref')

        for xref in unlinked_xrefs:
            if 'rid' in xref.attrib and (xref.attrib['rid'] == 'TO_LINK' or xref.attrib['rid'] == 'TO_LINK_NUMBER'):
                xref.tag = 'REMOVE'
                etree.strip_tags(xref.getparent(), 'REMOVE')

        manipulate.save_tree(tree)
        self.debug.print_debug(self, u'Removing {0} unlinked xref elements'.format(len(unlinked_xrefs)))

        mis_nested_xrefs = tree.xpath('//ext-link/xref')

        for tag in mis_nested_xrefs:
            tag.tag = 'REMOVE'

        etree.strip_tags(tree, 'REMOVE')
        manipulate.save_tree(tree)
        self.debug.print_debug(self, u'Removing {0} mis-nested ext-link/xref tags'.format(len(mis_nested_xrefs)))
