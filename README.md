# Maya-to-Nuke-Multipass_Composite

Hi, welcome to the Maya to Nuke composite.
This tool is for animators who want a Playblast with Nuke glows and a background replacement for their animated scene. A fast, directable playblast.

# How to install
To install, there are three scripts. the UI script, the function script, and the Nuke script. 
  The multipass_pass_composite_lanh goes into your .nuke folder inside your computer.
  The other two scripts go into your Maya - Scripts folder on your computer.

  To run it, open your script editor in your Maya scene (it's the icon in the bottom right of the UI)
  And type this once the folders are located.

  import quick_composite_ui_lanh_v02 as qcui
  import importlib
  importlib.reload(qcui)
  qcui.main()

  You can select these lines and drag and drop them into your Maya toolbar to set up as a button, and be done.

# The problem
To learn data transfer between DCCs and software. This really encapsulates selections into a single library to open and use process in nuke.

# The solution
UI path selection and grabbing references.


