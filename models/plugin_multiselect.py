def plugin_multiselect_include():
    response.files.append(URL(r=request,c='static',f='plugin_multiselect/jquery.dimensions.js'))
    response.files.append(URL(r=request,c='static',f='plugin_multiselect/jquery.multiselect.js'))
    response.files.append(URL(r=request,c='static',f='plugin_multiselect/jquery.multiselect.css'))

def plugin_multiselect(id='table_field'):
    if isinstance(id,Field):
        id=str(id).replace('.','_') 
    return SCRIPT("jQuery(document).ready(function(){jQuery('#%s').multiSelect();});" % id)

plugin_multiselect_include()
