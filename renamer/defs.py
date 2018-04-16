#----------------------------------------------------------------------
# renamer.defs
# Author : felixlechA.com | f.rault
# Date   : May 2015
# Decription : renamer commun definitions
#----------------------------------------------------------------------
import maya.cmds as mc

#----------------------------------------------------------------------
def sort_objectByHierarchy( in_obj ):
    '''
    Sort object_list object by place in hierarchy

    :param in_obj: List of object as longName
    :type in_obj: list

    :return: Sorted Objects
    :rtype: list
    '''
    # --- Sort object by hierarchy level
    # - Create dictionnary
    sort_dict= dict()

    upper_rank= 0
    for item in in_obj:
        # - Split longName
        rank= len(item.split('|'))

        # - Update upper_rank
        if rank > upper_rank:
            upper_rank= rank

        # - Create rank key if needs
        if not rank in sort_dict.keys():
            sort_dict[rank]= list()
        # - Add iterm to key
        sort_dict[rank].append( item )

    # --- Build a return list object by hierarchy
    result= list()
    for i in range( upper_rank, -1, -1):
        if i in sort_dict.keys():
            result.extend( sort_dict[i] )

    return result

#---------------------------------------------------
def numbering( name, nbr ):
    '''
    On a base name replace ## by numbering as 01
    ::
        example :
        in name ### with nbr = 1 > 001
        in name ### with nbr = 5687 > 5687
        in name ###_## with nbr = 2 > 'invalid_hastTag'

    :param name: The name where found #
    :type name: string

    :param nbr: The number of current
    :type nbr: integer

    :return: The name with numbering include
    :rtype: string
    '''

    first_hastTag= name.find('#')
    last_hastTag= name.rfind('#')
    sub_hastTag= last_hastTag+1 - first_hastTag
    nbr_hastTag= name.count('#')

    if not sub_hastTag - nbr_hastTag == 0:
        return '#_invalid'

    hastTag= ''
    for i in range( 0, nbr_hastTag):
        hastTag += '#'

    numbering= ''
    nbr_zero= nbr_hastTag - len(str(nbr))
    if nbr_zero <= 0:
        numbering= str(nbr)
    else:
        for i in range( 0, nbr_zero):
            numbering += '0'
        numbering += str(nbr)

    return name.replace( hastTag, numbering )

#----------------------------------------------------------------------
def get_objectType( in_obj ):
    '''
    Get type of a given object

    :param in_obj : The object that give shapes
    :type in_obj: string

    :return: The object type
    :rtype: string
    '''
    type= mc.nodeType( in_obj )

    if type == 'transform':
        # - Get All Shapes
        shape_list = mc.listRelatives( in_obj, s= True, fullPath= True )

        # - Filter shapes by type
        if shape_list:
            type= mc.nodeType( shape_list[0] )
        else:
            type= 'grp'

    if type == 'nurbsCurve':
        type= 'curve'

    if type == 'nurbsSurface':
        type= 'surface'

    return type

#---------------------------------------------------
def convert_extra_pattern( object, name ):
    # - %parent
    if '%parent' in name:
        parent_list = mc.listRelatives( object, p=True, fullPath= True )
        if parent_list:
            name= name.replace( '%parent', parent_list[0].split('|')[-1] )
        else:
            name= '%parent_invalid'

    # - %type
    if '%type' in name:
        type= get_objectType( in_obj= object )
        if type:
            name= name.replace( '%type', type )
        else:
            name= '%type_invalid'

    return name

#---------------------------------------------------
def build_name( object, search= '', replace= '', remove_first= 0, remove_last= 0, prefix= '', suffix= '', base_name= '', nbr= 1 ):
    '''
    Build name for renaming  based on given args

    :param object: The long name object
    :type object: string

    :param search: Define pattern string to search
    :type search: string

    :param replace: Define pattern string to replace the search found
    :type replace: string

    :param remove_first: Define how many first characters remove
    :type remove_first: integer

    :param remove_last: Define how many last characters remove
    :type remove_last: integer

    :param prefix: Define prefix to add
    :type prefix: string

    :param suffix: Define suffix to add
    :type suffix: string

    :param base_name: Define name to overide name
    :type base_name: string

    :param nbr: Define the numbering of the current object
    :type nbr: integer

    :return: The new name
    :rtype: string
    '''
    # - Build name
    name= object.split('|')[-1]

    # - Base name
    if base_name:
        name= convert_extra_pattern( object, base_name )

    # - Search and Replace
    if search:
        name = name.replace( convert_extra_pattern( object, search ), convert_extra_pattern( object, replace ) )

    # - remove First
    if remove_first > 0 and not name in ['#_invalid', '%parent_invalid', '%type_invalid']:
        if remove_first > len(name):
            remove_first= len(name)
        name= name[remove_first:]

    # - remove Last
    if remove_last > 0 and not name in ['#_invalid', '%parent_invalid', '%type_invalid']:
        if remove_last > len(name):
            remove_last= len(name)
        name= name[:-remove_last]

    # - Prefix
    if prefix and not name in ['#_invalid', '%parent_invalid', '%type_invalid']:
        name= convert_extra_pattern( object, prefix ) + name

    # - Suffix
    if suffix and not name in ['#_invalid', '%parent_invalid', '%type_invalid']:
        name= name + convert_extra_pattern( object, suffix )

    # - Numbering
    if '#' in name:
        name= numbering( name, nbr )

    # - Return
    return name

#---------------------------------------------------
def on_selected( in_obj, rename_dict ):
    '''
    Rename given objects based on dictionnary given
    Sort object to rename first deeper object

    :param in_obj: Object to rename
    :type in_obj: list

    :param rename_dict: Dictionnary who contain name - newName
    :type rename_dict: dictionnary

    :return: none
    '''

    obj_toRename= sort_objectByHierarchy( in_obj= in_obj )

    # Rename Object
    for item in obj_toRename:
        if not item in rename_dict.keys():
            continue

        if not mc.objExists( item ):
            continue

        new_name= rename_dict[ item ][1]

        if new_name in ['#_invalid', '%parent_invalid', '%type_invalid']:
            continue

        mc.rename( item, new_name )
