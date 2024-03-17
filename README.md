# Paint-2.0
My version of paint 2.0 with a drawing tools pencil, line, rectangle, triangle, circle and eraser. It's is also possible to change color and save image or create a new image.

If you have error "#OSError: Unable to locate Ghostscript on paths" follow these steps

The error message "OSError: Unable to locate Ghostscript on paths" indicates that Python's `tkinter` module is unable to find the Ghostscript executable in the system's PATH. This can happen when Ghostscript is not installed on your system or when the PATH environment variable does not include the directory containing the Ghostscript executable.

To resolve this issue, you can do one of the following:

1. **Install Ghostscript:** Download and install Ghostscript from the official website (https://www.ghostscript.com/download/gsdnld.html) for your operating system. Make sure to add the Ghostscript installation directory to your system's PATH environment variable.

2. **Set the Ghostscript Path in Python:** If you have Ghostscript installed but it's not in the system's PATH, you can set the path to the Ghostscript executable manually in your Python script. For example:

   ```python
   import os
   os.environ["PATH"] += os.pathsep + 'C:/path/to/ghostscript'
   ```

   Replace `'C:/path/to/ghostscript'` with the actual path to your Ghostscript installation directory.

After making these changes, try running your Python script again.
