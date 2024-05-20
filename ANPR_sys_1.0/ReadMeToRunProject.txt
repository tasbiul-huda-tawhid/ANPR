Goto CMD:
C:\Users\Tawhid>D:

D:\>cd "D:\study\Intern_Mahsa (2024)\ANPR_sys_1.0"

D:\study\Intern_Mahsa (2024)\ANPR_sys_1.0>D:\tools\Anaconda\Anaconda_sftwer\Scripts\activate anpr

(anpr) D:\study\Intern_Mahsa (2024)\ANPR_sys_1.0>code .

(anpr) D:\study\Intern_Mahsa (2024)\ANPR_sys_1.0>pip install -r requirements.txt


To use pytesseract (already in requirements) in your Python code on Windows:
Install Tesseract-OCR:
Download and install the Tesseract OCR executable. You can download the installer from the official Tesseract GitHub repository or directly from this link.

Download the installer for Windows (e.g., tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe).
Run the installer and follow the installation instructions.
Note the installation path, e.g., C:\Program Files\Tesseract-OCR.
Add Tesseract to the System Path:

Open the Start Menu, search for "Environment Variables," and select "Edit the system environment variables."
In the System Properties window, click the "Environment Variables" button.
Under "System variables," find the Path variable, select it, and click "Edit."
Click "New" and add the path to the Tesseract executable, e.g., C:\Program Files\Tesseract-OCR.
Install pytesseract Python Library:
Open a terminal or Command Prompt and install the pytesseract package using pip:

Copy code
pip install pytesseract
Using pytesseract in Your Python Code:
In your Python script, import pytesseract and set the tesseract_cmd path to point to the Tesseract executable.