import maya.cmds as cmds
import subprocess
import mtoa.aovs as raovs
import os
import platform
import quick_composite_lanh as qcl
import importlib as il

il.reload(qcl)

def  send_data (aovs_selected):
    '''
    Description: Gathers the information and stores it in a dictionary,
                it passes it to quick composite.
    Inputs:
    Output: data (dict): paths, integers, and names set by the gui in maya.
    '''
    # Runing this functions to get the paths for these two variables.
    nuke_python_script = get_nuke_directory()
    nuke_program_path = get_nuke_exe()
    list_of_aovs = aovs_selected
    print (type(nuke_program_path))
    print(type(list_of_aovs))

    # Transforming from string to int before passing through.
    width = int(cmds.intFieldGrp(
                                'width_ifg',
                                query = True,
                                value= True)[0]
                )   
    height = int(cmds.intFieldGrp(
                                'height_ifg',
                                query = True,
                                value= True)[0]
                )
    start_frame = int(cmds.intFieldGrp(
                                'start_frame_ifg',
                                query = True,
                                value= True)[0])
    end_frame = int(cmds.intFieldGrp(
                                'end_frame_ifg',
                                query = True,
                                value= True)[0])
    
    # Storing the camera data into its own dictiionary to subnest.
    camera_data = {'camera_name':cmds.textFieldButtonGrp(
                                'camera_name_tfbg',
                                query = True,
                                text = True),
                'camera_path': cmds.textFieldButtonGrp(
                                'camera_alembic_tfbg',
                                query = True,
                                text = True)}

    # Sets the variables into a dictionary to passthrough.
    data = {
            'output_name': cmds.textFieldGrp(
                                                'file_name_tfg', 
                                                query = True,
                                                text = True
                                                        ),
            'maya_render_path': cmds.textFieldButtonGrp(
                                'maya_render_path_tfbg',
                                query = True,
                                text = True),
            'nuke_render_path': cmds.textFieldButtonGrp(
                                'nuke_render_path_tfbg',
                                query = True,
                                text = True),
            'camera_data': camera_data,
            'nuke_python_script': nuke_python_script,
            'active_aovs': list_of_aovs,
            'start_frame': start_frame,
            'end_frame': end_frame,
            'width': width,
            'height': height,
            'NUKE': nuke_program_path,
            'background_image':  cmds.textFieldButtonGrp(
                                'image_bg_path_tfbg',
                                query = True,
                                text = True)
            }
    
    print(data)
    print(type(data))
    print(type(nuke_program_path))
    #Runs quick composite      
    qcl.quick_composite(data)
    return data

def main():
    '''
    Description: Runs the UI.
    Input: None
    Output: None
    '''

    # Deletes the window if it exists.
    if cmds.window('comp_win', exists = True):
        cmds.deleteUI('comp_win')
    cmds.window('comp_win', title = 'Quick composite')

    # Builds the UI.
    cmds.columnLayout(adjustableColumn = True, rowSpacing = 5)
    cmds.text(label = 'Render Pipeline')
    cmds.text(
            label = 'Render the scene into Nuke into a multipass comp', 
            align = 'left'
            )
    cmds.text(
            label = 'Set the name, and location of where you want to export \n'
                    'the exrs, nuke composites, and camera alembic.\n' 
                    'The Nuke path will be set for you. \n'
                    'Select the camera to grab its name. \n'
                    'Set the frame render range. \n'
                    'The AOVS will be selected when double clicked, once \n'
                    'It will be added, if it turns yellow it is removed.',
            align = 'left',
            rs = True
            )
    cmds.textFieldGrp(
        'file_name_tfg', 
        adjustableColumn = 2,
        columnWidth = [(1,100), (3,100)],
        columnAlign = (1,'left'),
        label = 'File Name:',
                )
    cmds.textFieldButtonGrp(
            'maya_render_path_tfbg', 
            label = 'Maya Render Path:',
            adjustableColumn = 2,
            columnWidth = [(1,100), (3,100)],
            columnAlign = (1,'left'),
            annotation = 'Set the Maya output files location.',
            buttonLabel = 'Set',
            buttonCommand = lambda *args: get_path_cb("maya_render_path_tfbg")
                    )

    cmds.textFieldButtonGrp (
            'nuke_render_path_tfbg', 
            label = 'Nuke Render Path:',
            annotation = 'Set the Final Nuke output files location.',
            columnWidth = [(1,100), (3,100)],
            columnAlign = (1,'left'),
            adjustableColumn = 2,
            buttonLabel = 'Set',
            buttonCommand = lambda *args: get_path_cb("nuke_render_path_tfbg") 
            )
    cmds.textFieldButtonGrp (
            'nuke_python_script_tfbg', 
            label = 'Nuke Python Path:',
            annotation = 'Set the Nuke script location to process exrs.',
            columnWidth = [(1,100), (3,100)],
            columnAlign = (1,'left'),
            adjustableColumn = 2,
            buttonLabel = 'Set',
            buttonCommand = lambda *args: get_nuke_directory() 
            )
    cmds.textFieldButtonGrp (
            'camera_alembic_tfbg', 
            label = 'Camera Alembic Path:',
            annotation = 'Set the Camera Alembic location to process exrs.',
            columnWidth = [(1,120), (3,100)],
            columnAlign = (1,'left'),
            adjustableColumn = 2,
            buttonLabel = 'Set',
            buttonCommand = lambda *args: get_path_cb("camera_alembic_tfbg") 
            )
    cmds.textFieldButtonGrp (
                        'camera_name_tfbg', 
                        label = 'Camera Alembic Name:',
                        annotation = 'Set the Camera Name.',
                        columnWidth = [(1,120), (3,100)],
                        columnAlign = (1,'left'),
                        adjustableColumn = 2,
                        buttonLabel = 'Set',
                        buttonCommand = lambda *args: get_camera_name () 
                        )
    cmds.textFieldButtonGrp (
            'image_bg_path_tfbg', 
            label = 'Background Image Path:',
            annotation = 'Set the Background Image files location.',
            columnWidth = [(1,100), (3,100)],
            columnAlign = (1,'left'),
            adjustableColumn = 2,
            buttonLabel = 'Set',
            buttonCommand = lambda *args: get_file_cb("image_bg_path_tfbg") 
            )
    cmds.intFieldGrp(
                    'start_frame_ifg', 
                    columnWidth = [(1,100), (2,50)],
                    columnAlign = (1,'left'),
                    label = 'Start Frame:',
                            )
    cmds.intFieldGrp(
                    'end_frame_ifg', 
                    columnWidth = [(1,100), (2,50)],
                    columnAlign = (1,'left'),
                    label = 'End Frame:',
                            )
    cmds.intFieldGrp(
                        'width_ifg', 
                        columnWidth = [(1,100), (2,100)],
                        columnAlign = (1,'left'),
                        label = 'Width:',
                    )
    cmds.intFieldGrp(
                        'height_ifg', 
                        columnWidth = [(1,100), (2,100)],
                        columnAlign = (1,'left'),
                        label = 'Height:',
                        )
    
    # Gets a list of available AOVs maya has as a list for the list below.
    raovs_avail = raovs.getLightingAOVs()
    raovs_avail.extend(raovs.getBuiltinAOVs())
    aovs_selected = list()
    cmds.textScrollList(
            'aovs_avaialable_tsl',
            numberOfRows=10,
            allowMultiSelection=True,
            manage = True,
            append = raovs_avail,
            dcc = lambda *args: set_selected_aovs(aovs_selected),
            )
    
    # Runs the main UI with the button and shows the UI.
    cmds.button( label = 'Go', command = lambda *args: send_data(aovs_selected))
    cmds.showWindow()

    return 

def get_path_cb(tfbg):
    '''
    Description: Querys a location path for the UI.
    Input:
        tfbg (str): Name of the button that runs this function.
    Output:
        path(str): The file path requested.
    '''

    # Runs the function that sets the project file standard.
    set_ui_defaults(tfbg)

    # Opens up the window and edits the text field in the button.
    path = cmds.fileDialog2(fileMode = 2, dialogStyle = 2)[0]
    cmds.textFieldButtonGrp(tfbg, edit = True, text = path + '/')
    print(type(path))
    return path

def get_file_cb(tfbg):
    '''
    Description: Querys a file path for the UI.
    Input:
        tfbg (str): Name of the button that runs this function.
    Output:
        path(str): The file path requested.
    '''
    # Runs the function that sets the projects location.
    set_ui_defaults(tfbg)

    # Opens up a window to select a file.
    path = cmds.fileDialog2(fileMode = 0, dialogStyle = 2)[0]
    cmds.textFieldButtonGrp(tfbg, edit = True, text = path)
    print (type(path))
    return path

def set_selected_aovs (list_of_aovs):
    '''
    Description: 
        Sets the queried items of AOVS from the UI into a list.
    Input:
        None*: It queries the UI.
    Output:
        list_of_aovs (list): A list of strings of the AOVS queried.    
    '''
    
    # Queries the list and sets it in an obj. 
    selected_aovs = cmds.textScrollList(
            'aovs_avaialable_tsl',
            query = True,
            selectItem = True
            )
    # It filters through each item to see if it exits and appends it or deletes.
    for item in selected_aovs:
        if item in list_of_aovs:
            cmds.textScrollList(
                                'aovs_avaialable_tsl',
                                edit = True, 
                                selectItem = selected_aovs,
                                highlightColor = [1,1,0]
                                )
            list_of_aovs.remove(item)
        else:
            cmds.textScrollList(
                                'aovs_avaialable_tsl',
                                edit = True, 
                                selectItem = selected_aovs,
                                highlightColor = [0,0,0]
                                )
            list_of_aovs.append(item)
    print(list_of_aovs)
    print(type(list_of_aovs))
    return list_of_aovs

def set_ui_defaults(tfbg):
    '''
    Description:
        Sets the UI render path default to the project location.
    Input:
        None
    Output:
        root_dir(str): A path to the projects location.
    '''
    
    # It queries the projects path. 
    root_dir = cmds.workspace(query = True, rootDirectory = True)
    
    # It edits the text button.
    cmds.textFieldButtonGrp (
                        tfbg, 
                        edit = True,
                        text = '{}'.format(root_dir)
                    )
    print(type(root_dir))
    return root_dir

def get_nuke_directory():
    '''
    Description: It gets the nuke directory from the system
    Input: None
    Output:
        nuke_puthon_script_path (str): It queries the python file for Nuke.
    '''
    # Checks if there is a Z drive.
    if os.path.exists('Z:'):
        directory = os.listdir('z:')
        working_directory = 'Z:/'
    else:
        directory = os.listdir ('c:')
        working_directory = 'C:'

    # Stores the script path with the directory.
    nuke_python_script_path = os.path.join(
                                            working_directory,
                                            '.nuke/',
                                            'multipass_composite_lanh.py'
                                            ) 
    # It edits the UI button.
    cmds.textFieldButtonGrp (
                        'nuke_python_script_tfbg', 
                        edit = True,
                        text = '{}'.format(nuke_python_script_path))
    print (type(nuke_python_script_path))
    return nuke_python_script_path 

def get_nuke_exe ():
    '''
    Description: It gets the location path for the newest version of Nuke.
    Input: None
    Output:
        nuke_program_path (str): A path to the location of nukes program.
    '''
    # Checks which operating system is the system, and sets the root.
    if platform.system() == 'Windows':
        app_directory = 'C:/Program Files'
    elif platform.system () == 'Darwin':
        app_directory = '/Applications'
    elif platform.system () == 'Linux' :
        app_directory = '/usr/bin'

    # Validate application path.
    if not os.path.exists(app_directory):
        print (
                f'{app_directory} does not exist.'
                )
        quit ()
    
    # Checks each item in the directory for Nuke.
    for item in os.listdir(app_directory):
        if item == 'Nuke15.1v4':
            #print (item)
            item_path = os.path.join('{}/'.format(app_directory), '{}/'.format(item))
            #print (item_path)

            # Checks for the .exe file.
            for i in os.listdir(item_path):
                if i == 'Nuke15.1.exe':
                    nuke_program_path = os.path.join(item_path,i)
                    # print (nuke_program_path)
    print (type(nuke_program_path))  
    return nuke_program_path

def get_camera_name ():
    '''
    Description: It queries the name and sets it to the UI.
    Input: none
    Output: 
        camera_name_tfbg (list): The object selected in Maya.
    '''
    # It queries the selection and edits the text of the UI.
    camera_text = cmds.ls(sl = True)
    cmds.textFieldButtonGrp (
                    'camera_name_tfbg', 
                    edit = True,
                    text = '{}'.format(str(camera_text[0])))
    camera_name = str(camera_text)
    return camera_name









    


    
