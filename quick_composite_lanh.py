import maya.cmds as cmds
import subprocess
import mtoa.aovs as raovs
import os
import platform
import json

def quick_composite (data):
    '''
    Description: Exports the information from maya into nuke.
    Input:
        Data (dict): Is the data required to run the functions of the tool.
    Output:
        Data (dict): updated version storing nuke path information.
    ''' 
    # Set Maya Render Attributes.
    setup_render_attributes(data)
    
    # Create AOVs.
    setup_AOVS(data)
    
    # Get Camera Data.
    export_camera_alembic(data)

    # Render image sequence in maya as EXR.
    file_sequence_name = '{}.####.exr'.format(data['output_name'])
    maya_file_sequence = os.path.join(data['maya_render_path'],file_sequence_name)
    
    # Run the arnold renderer to render the sequence.
    cmds.arnoldRender(
                      width = data ['width'],
                      height = data ['height'],
                      camera = data ['camera_data']['camera_name'],
                      batch = True
                      )
    
    # Build Nuke Script, file path and file path name.
    nuke_script_name = '{}.nk'.format(data['output_name'])
    nuke_script_path = os.path.join(data['nuke_render_path'],nuke_script_name)
    nuke_file_sequence = os.path.join(data['nuke_render_path'],file_sequence_name)
    
    # Stores the Nuke paths into the data dict.
    data['nuke_script_path'] = nuke_script_path
    data ['input_path'] = maya_file_sequence
    data ['output_path'] = nuke_file_sequence

    # Stores the path to nuke into its variable.
    NUKE = data['NUKE']
    print(type(NUKE))
    print(type(data))
    print(type(data['nuke_python_script']))
    print(type(nuke_script_path))

    #json_data = json.dumps(data)
    # Opens Nukes and passes through the data. 
    
    nuke_script_process = subprocess.Popen(
                        [NUKE, '-ti', data['nuke_python_script'],str(data)],
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE
                        )
    stdout, stderr = nuke_script_process.communicate()
    
    
    # Render Nuke Composite
    render_process = subprocess.Popen(
                                [NUKE,'-ti','-x',nuke_script_path],
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE
                                )
    stdout, stderr = render_process.communicate()
    
                   
    

    return data

def setup_AOVS (data):
    '''
    Description: It sets up a list of the aovs selected to bake in and pass thru.

    Input:
        list_of_aovs (list): A list of AOVS selected by user.

    Output:
        active_aovs(list): A list of aovs active in the renderer.
    '''
    enabled_aovs = list(data['active_aovs'])
    active_aovs = []
    for aov in enabled_aovs:
        active_aovs.append(raovs.AOVInterface().addAOV(aov))

    return active_aovs

def setup_render_attributes (data):
    '''
    Description:
        Sets the attributes of data as projects render settings.
    Input:
        Data (dict): Is the data required to run the functions of the tool.
    Output:
        None.
    '''
    # Set the attributes from data into their respectiva maya settings.
    cmds.setAttr('defaultRenderGlobals.startFrame', data['start_frame'])
    cmds.setAttr('defaultRenderGlobals.endFrame', data['end_frame'])
    cmds.setAttr('defaultRenderGlobals.animation', 1)
    cmds.setAttr('defaultRenderGlobals.outFormatControl', 0)
    cmds.setAttr('defaultRenderGlobals.putFrameBeforeExt', 1)
    cmds.setAttr('defaultArnoldRenderOptions.motion_blur_enable', True)
    cmds.setAttr('defaultRenderGlobals.imageFilePrefix', data['output_name'], type='string')
    cmds.setAttr('defaultArnoldRenderOptions.imageFormat','exr',type = 'string')
    cmds.setAttr('defaultArnoldDriver.mergeAOVs', True)
    cmds.setAttr('defaultResolution.width', data['width'])
    cmds.setAttr('defaultResolution.height', data['height'])

    return

def export_camera_alembic (data):
    '''
    Description: grabs the selected camera selection and exports it as alembic.
    Input:
        Data (dict): Is the data with the nested camera information in it.
    Output:
        abc_file (str): Alembic path file and type of the camera.
        abc_export_cmd (list): strings with the settings of the Alembic. 
    '''
    # Sets the variables from the data to run properly.
    start_frame = int(data['start_frame'])
    end_frame = int(data['end_frame'])
    width = int(data['width'])
    height = int(data['height'])
    camera_name = data['camera_data']['camera_name']
    camera_path = data['camera_data']['camera_path']
    
    # Sets the alembic path file.
    abc_file = f"{camera_path}/{camera_name}.abc"
    
    # Selects the camera.
    cmds.select(data['camera_data']['camera_name'],replace=True)
    
    # Sets the setting of the alembic export into a string (mel type).
    abc_export_cmd = (
    f"-frameRange {start_frame} {end_frame} "
    f"-step 1 -worldSpace -writeVisibility -eulerFilter "
    f"-dataFormat ogawa -root |{data['camera_data']['camera_name']} "
    f"-file \"{abc_file}\""
                    )

    # Runs the Alembic exporter and sets the abc_export_cmd as settings.
    cmds.AbcExport(j=abc_export_cmd)

    # It clears the selection.
    cmds.select(clear = True)

    return abc_file, abc_export_cmd












    


    
