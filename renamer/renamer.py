#----------------------------------------------------------------------
# renamer.renamer
# Author : felixlechA.com | f.rault
# Date   : May 2015
# Decription : renamer Tool UI
#----------------------------------------------------------------------
import maya.cmds as mc
import defs as renamer_defs
reload( renamer_defs )

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Renamer():
    def __init__( self ):
        '''
        init Class
        '''
        self.tool_name= 'renamerTool_Window'
        self.tool_title= 'renamer Tool'
        self.preview_name= dict()
        self.widgets = {} # Dictionnary who store the tool's UI

    #----------------------------------------------------------------------
    def UI( self, *args ):
        '''
        The UI
        '''
        # --- Check existing Windows
        if mc.window( self.tool_name, exists=True ):
            mc.deleteUI( self.tool_name, window=True )

        # --- Create window
        self.widgets['win'] = mc.window( self.tool_name, title= self.tool_title, sizeable= False , toolbox= True )

        self.widgets['win_col'] = mc.columnLayout( adj= True )
        self.widgets['frame_layout'] = mc.frameLayout(bs='etchedIn', mh=5, mw=5, cll= False, bgc=[0.719, 0.424, 0.0], l= '', labelVisible= True, bv= False )

        self.widgets['base_name'] = mc.textFieldGrp( l=' Base name : ', cw2= [ 65, 195], text='', annotation= 'Define suffix to add')
        self.widgets['separator'] = mc.separator( style='in' )

        self.widgets['row_col1'] = mc.rowLayout(numberOfColumns= 2 )
        self.widgets['search'] = mc.textFieldGrp( l='Search for ', cw2= [ 55, 70], text='', annotation= 'Define characters to search')
        self.widgets['replace'] = mc.textFieldGrp( l='& Replace ', cw2= [ 50, 75], text='', annotation= 'Define characters to Replace by')

        mc.setParent( self.widgets['frame_layout'] )
        self.widgets['row_col2'] = mc.rowLayout(numberOfColumns= 2 )
        self.widgets['remove_first'] = mc.intFieldGrp( numberOfFields=1, label=' Remove fisrt', value1= 0, cl2= [ 'left', 'right' ], cw2= [ 90, 35], annotation='remove n first characters' )
        self.widgets['prefix'] = mc.textFieldGrp( l='Prefix : ', cw2= [ 50, 75], text='', annotation= 'remove n last characters')

        mc.setParent( self.widgets['frame_layout'] )
        self.widgets['row_col3'] = mc.rowLayout(numberOfColumns= 2 )
        self.widgets['remove_last'] = mc.intFieldGrp( numberOfFields=1, label=' Remove last', value1= 0, cl2= [ 'left', 'right' ], cw2= [ 90, 35], annotation='Define prefix to add' )
        self.widgets['suffix'] = mc.textFieldGrp( l='Suffix : ', cw2= [ 50, 75], text='', annotation= 'Define suffix to add')

        mc.setParent( self.widgets['frame_layout'] )
        self.widgets['frame_layout_preview'] = mc.frameLayout(bs='etchedIn', mh=0, mw=0, l='preview', cll= True, collapse= True, expandCommand= self.preview, bv= False )
        self.widgets['win_col_preview'] = mc.columnLayout( adj= True )
        self.widgets['win_bt_preview'] = mc.button(l='refresh preview list', height= 25, c= self.preview )

        mc.setParent( self.widgets['frame_layout'] )
        self.widgets['row_col4'] = mc.rowLayout(numberOfColumns= 2 )
        self.widgets['win_bt_reset'] = mc.button(l='reset', height= 35, width= 40, c= self.reset_UI, annotation= 'Clear UI' )
        self.widgets['win_bt_launch'] = mc.button(l='Rename Selected', height= 35, width= 226, c= self.launch, annotation= 'Rename selected objects' )

        # --- Show window
        mc.showWindow(self.widgets['win'])

    #----------------------------------------------------------------------
    def reset_UI( self, *args ):
        '''
        Reset all UI input values

        :return: none
        '''
        # - Reset UI values
        mc.textFieldGrp( self.widgets['search'], e= True, tx= '' )
        mc.textFieldGrp( self.widgets['replace'], e= True, tx= '' )

        mc.intFieldGrp( self.widgets['remove_first'], e= True, value1= 0 )
        mc.intFieldGrp( self.widgets['remove_last'], e= True, value1= 0)

        mc.textFieldGrp( self.widgets['prefix'], e= True, tx= '' )
        mc.textFieldGrp( self.widgets['suffix'], e= True, tx= '' )

        mc.textFieldGrp( self.widgets['base_name'], e=True, tx= '' )

    #----------------------------------------------------------------------
    def launch( self, *args ):
        '''
        Rename selected object with params define in UI

        :return: none
        '''
        # - Get current selection
        sel= mc.ls( sl= True ) or list()

        if not sel:
            return

        self.build_name_for_renaming( sel= sel )

        renamer_defs.on_selected( sel, self.preview_name )

    #----------------------------------------------------------------------
    def preview( self, *args ):
        '''
        Preview in preview frame the result of the renaming

        :return: none
        '''

        # - Get current selection
        sel= mc.ls( sl= True ) or list()

        if not sel:
            # - reBuild UI Preview
            mc.deleteUI( self.widgets['win_col_preview'] )

            mc.setParent( self.widgets['frame_layout_preview'] )
            self.widgets['win_col_preview'] = mc.columnLayout( adj= True )
            self.widgets['win_bt_preview'] = mc.button(l='refresh preview list', height= 25, c= self.preview )
            return

        self.build_name_for_renaming( sel= sel )

        if not self.preview_name:
            return

        # - reBuild UI Preview
        mc.deleteUI( self.widgets['win_col_preview'] )

        mc.setParent( self.widgets['frame_layout_preview'] )
        self.widgets['win_col_preview'] = mc.columnLayout( adj= True )
        self.widgets['scroll_layout'] = mc.scrollLayout( verticalScrollBarThickness= 16, height= 120 )
        mc.rowColumnLayout( numberOfColumns= 2 )

        # - labels
        mc.textField( text= 'current', backgroundColor= [0.4,0.4,0.4], width= 120, editable= False )
        mc.textField( text= 'renamed', backgroundColor= [0.4,0.4,0.4], width= 120, editable= False )

        for i in range(0, len( sel ), 1):
            # - Check if name are unique
            unique_result= self.check_unique( in_obj= sel[i] )

            # - Set bg color
            MultR_old, MultR_new, Mult_error = 1, 1, 1
            annotation_old= ''
            annotation_new= ''
            if not unique_result[0]:
                MultR_old= 1.5
                annotation_old= 'is not a unique name'
            if not unique_result[1]:
                MultR_new= 1.5
                annotation_new= 'is not a unique name'
            if self.preview_name[sel[i]][1] in ['#_invalid', '%parent_invalid', '%type_invalid']:
                MultR_new= 1.5
                Mult_error= 2
                annotation_new= 'invalid name, check renamer input'

            if (i%2 == 0):
                bg_color_old= [0.28*MultR_old, 0.28, 0.28]
                bg_color_new= [0.28*MultR_new*Mult_error, 0.28, 0.28/Mult_error]
            else:
                bg_color_old= [0.25*MultR_old, 0.25, 0.25]
                bg_color_new= [0.25*MultR_new*Mult_error, 0.25, 0.25/Mult_error]

            # - Build textField
            mc.textField( text= self.preview_name[sel[i]][0], backgroundColor= bg_color_old, width= 120, editable= False, annotation= annotation_old )
            mc.textField( text= self.preview_name[sel[i]][1], backgroundColor= bg_color_new, width= 120, editable= False, annotation= annotation_new )

        mc.setParent( self.widgets['win_col_preview'] )
        self.widgets['win_bt_preview'] = mc.button(l='refresh preview list', height= 25, c= self.preview )

    #----------------------------------------------------------------------
    def build_name_for_renaming(self, sel, *args):
        '''
        Build dictonnary of renaming name for selected obj
        Populate self.preview_name class var

        :param sel: List object to rename
        :type sel: list

        :return: none
        '''

        if not sel:
            if not self.preview_name:
                return

        # - Get UI values
        search= mc.textFieldGrp( self.widgets['search'], q=True, tx=True )
        replace= mc.textFieldGrp( self.widgets['replace'], q=True, tx=True )

        remove_first= mc.intFieldGrp( self.widgets['remove_first'], q= True, value1= True)
        remove_last= mc.intFieldGrp( self.widgets['remove_last'], q= True, value1= True)

        prefix= mc.textFieldGrp( self.widgets['prefix'], q=True, tx=True )
        suffix= mc.textFieldGrp( self.widgets['suffix'], q=True, tx=True )

        base_name= mc.textFieldGrp( self.widgets['base_name'], q=True, tx=True )

        # - Build rename name list
        rename_dict= dict()
        i= 1
        for item in sel:
            rename_dict[item]= [item.split('|')[-1], renamer_defs.build_name( object= item, search= search, replace= replace, remove_first= remove_first, remove_last= remove_last, prefix= prefix, suffix= suffix, base_name= base_name, nbr= i)]
            i += 1

        self.preview_name= rename_dict

    #----------------------------------------------------------------------
    def check_unique(self, in_obj):
        '''
        Check for given object if current and futur name are unique

        :param in_obj: object longName
        :type in_obj: string

        :return: List of boolean [True, True] to define current and futur name are unique
        :rtype: list
        '''
        # - Get All futur name
        new_list= list()
        for item in self.preview_name.keys():
            new_list.append( self.preview_name[item][1] )

        # - Get Current and futur name from dict
        name_old= self.preview_name[in_obj][0]
        name_new= self.preview_name[in_obj][1]

        # - Check in scene how many object we found
        objects_old= mc.ls( name_old ) or list()
        if name_new in ['#_invalid', '%parent_invalid', '%type_invalid']:
            objects_new= list()
        else:
            objects_new= mc.ls( name_new ) or list()

        if name_old == name_new:
            objects_new.remove( in_obj )

        # - Build result list
        result= [ True, True ]

        if len( objects_old ) > 1:
            result[0]= False
        if len( objects_new ) > 0 or new_list.count( name_new ) > 1:
            result[1]= False

        return result



