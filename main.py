from os import listdir, getcwd, makedirs, chdir
from os.path import join, isdir, exists
import zipfile
import shutil

def remove_dir_if_exists(dirname):
    if exists(dirname) and isdir(dirname):
        shutil.rmtree(dirname)

def get_exam_dir(dirname):
    files = listdir(dirname)
    if 'manage.py' not in files:
        # return get_exam_dir(join(dirname, next(f for f in files if isdir(join(dirname, f)))))
        return get_exam_dir(join(dirname, files[0]))
    return dirname

# Remove and create `exams` dir if exists
EXAMS_DIR = join(getcwd(), 'exams')
remove_dir_if_exists(EXAMS_DIR)
if not exists(EXAMS_DIR):
    makedirs(EXAMS_DIR)

# Extract downloaded zip file
for f in listdir('.'):
    if '.zip' in f:
        exams_file = zipfile.ZipFile(f)
        exams_file.extractall(EXAMS_DIR)

# Extract exam zipfile
chdir(EXAMS_DIR)
for f in listdir('.'):
    _, name = f.split('_')
    TMP_DIR = join(EXAMS_DIR, 'tmp')
    EXAM_DIR = get_exam_dir(TMP_DIR)
    NAME_DIR = join(EXAMS_DIR, name)

    # Extract exam zipfile
    exam_file = zipfile.ZipFile(join(f, listdir(f)[0]))
    exam_file.extractall(TMP_DIR)

    shutil.move(EXAM_DIR, NAME_DIR)
    remove_dir_if_exists(f)
    remove_dir_if_exists('tmp')
    print(name)
