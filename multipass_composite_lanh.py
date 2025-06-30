import nuke
import sys

def multipass_composite(
                        file_name,
                        input_path,
                        output_path,
                        active_aovs, 
                        camera_path,
                        camera_name,
                        width,
                        height,
                        start_frame,
                        end_frame,
                        background_image):
    '''
    Description: Runs a Nuke Script with Data to automatically comp multipass.
    
    Inputs:
        file_name (str): Name of the file.
        input_path (str): Location of the EXRs.
        output_name (str): Location of the of the final renders.
        output_aovs (list): list of aovs in the exr.
        camera_path (str): Path to the alembic file
        Camera_name (str): Name of the camera.
        width(int): Width of the project file.
        height(int):  Height of the project file.
        Start_frame(int): Start of the nuke file.
        End_frame(int): End of the nuke file.
        background_image(str): Image to place behind exr.
        
    Output:
        None: A nk file with an exr of final composites.
    '''
    # Sets the path for the exr sequence and the camera.
    sequence = '{}{}.####.exr'.format(input_path, file_name)
    composite_sequence = '{}{}.####.exr'.format(output_path, file_name)
    camera = '{}/{}.abc'.format(camera_path,camera_name)
    
    # Sets the project settings.
    nuke.addFormat(f"{width} {height} tmCustom")
    nuke.root()['format'].setValue('tmCustom')
    nuke.root()['first_frame'].setValue(start_frame)
    nuke.root()['last_frame'].setValue(end_frame)
    
    # Reads in exr and shuffles in the rgba.
    nRead = nuke.nodes.Read(file = sequence)
    # Sets each channel of the exr into a new variable as a last.
    existing_layers = set([ch.split('.')[0] for ch in nRead.channels()])
    nShuffle = nuke.nodes.Shuffle2(label ='None')
    nShuffle['in1'].setValue('rgb')
    

    composite = nShuffle
    
    # Ses up the multipass composoting script going through each aov.
    #listed_aovs = list(active_aovs)
    for aov in existing_layers:
        nLayer = nuke.nodes.Shuffle2( label = aov, inputs = [nRead])
        nLayer['in1'].setValue(str(aov))
        nLayer['out1'].setValue('rgb')
        

        if aov == 'emission':
            nLayer = nuke.nodes.Glow(inputs = ([nLayer]))
            nLayer['tint'].setValue([1,0.3,0.05])
            nLayer['brightness'].setValue(15)
            nLayer['size'].setValue(25)
            
            
        nMerge = nuke.nodes.Merge2()
        nMerge['operation'].setValue('plus')
        nMerge.setInput (1,nLayer)
        nMerge.setInput (0,composite)
        
        composite = nMerge
    
    # Copys back the alpha on top of the EXR.
    nAlpha = nuke.nodes.Copy()
    nAlpha.setInput(0,composite)
    nAlpha.setInput(1,nRead)

    # Sets up the camera node.
    nCamera = nuke.nodes.Camera2()
    nCamera['read_from_file'].setValue(True)
    nCamera['file'].setValue(str(camera))

    # Attaches the background to the sphere object, scales and rotates it.
    nBackground = nuke.nodes.Read(file = background_image)
    nSphere = nuke.nodes.Sphere()
    nSphere.setInput(0,nBackground)
    nSphere['scaling'].setValue(1000)
    nSphere['rotate'].setValue(100)

    # Sets up a scanline render.
    nRender = nuke.nodes.ScanlineRender()
    nRender.setInput(1,nSphere)
    nRender.setInput(2,nCamera)

    # Sets up a final_merge of BG with EXR.
    final_merge = nuke.nodes.Merge()
    final_merge.setInput(0,nRender)
    final_merge.setInput(1,nAlpha)

    # Crops bounding box.
    nCrop = nuke.nodes.Crop()
    nCrop['crop'].setValue(False)
    nCrop.setInput(0,final_merge)
    
    # Writes the file
    nWrite = nuke.nodes.Write(file = composite_sequence,inputs = [nCrop])

    return    
#print('Script Name: ',sys.argv[0])
#print('Arguments: ',sys.argv[1]) 


# Checks if there is data information to run the script.
if __name__ == '__main__': 
    data = eval(sys.argv[1])
    #print (data)
    # Creates the script.
    nuke.scriptSave(data['nuke_script_path'])
    multipass_composite(
                        data['output_name'], 
                        data['maya_render_path'], 
                        data['nuke_render_path'],
                        data['active_aovs'],
                        data['camera_data']['camera_path'],
                        data['camera_data']['camera_name'],
                        data['width'],
                        data['height'],
                        data['start_frame'],
                        data['end_frame'],
                        data['background_image']
                        )
    # Saves the final version of the script.
    nuke.scriptSave(data['nuke_script_path'])
                        
   
