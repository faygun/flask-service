import os, pathlib
from utility import config
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = config.ALLOWED_EXT.rsplit(',')
# UPLOAD_PATH = os.path.join(pathlib.Path().resolve(), config.UPLOAD_PATH) 
UPLOAD_PATH = config.UPLOAD_PATH

def uploadProductFile(request):
    if 'file' not in request.files:
        raise Exception("File not found!")
    
    file = request.files['file']
    
    if file.filename == '':
        raise Exception("File name is empty!")
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filePath = os.path.join(UPLOAD_PATH, filename) 
        checkFolderExist()
        file.save(filePath)
        return True

    raise Exception("The file type is not supported!")

def allowed_file(filename):
    try:
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    except Exception as err:
        print(err)
        return False
    
def checkFolderExist():
    try:
        if os.path.exists(UPLOAD_PATH) == False:
            os.makedirs(UPLOAD_PATH)
    except:
        None
    finally:
        None