# MAKEOHIO10
Implementation of RoundSquare's MakeOhio10 project.

Developer Set Up:
Install python3, make sure version is up to date (3.9.0 or above)
Install pip3, make sure version is up to date (24.0)
Using pip3, install tk (pip3 install tk)

Need tkinter / tk toolkit to open new window
Install depends on device, so look up instructions
If DEPRACATED warning appears, it means install was done incorrectly
Most likely, version of python does not match to tk version.
After installing python3 and python-tk@3.11 with homebrew, I was
able to fix the incompatability issue by running "brew install python-tk."

For text to speech, need to create a virtual environment with venv.
From there, install gtts (Google's text-to-speech API) and playsound.
You may need to upgrade your version of wheel (or uninstall and reinstall)
to make this work. 