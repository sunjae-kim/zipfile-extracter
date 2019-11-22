from os import listdir, getcwd, makedirs, chdir
from os.path import join, isdir, exists
import zipfile
import shutil

KEY_FILE = 'manage.py'

def remove_dir_if_exists(dirname):
    if exists(dirname) and isdir(dirname):
        shutil.rmtree(dirname)

def get_exam_dir(dirname):
    files = listdir(dirname)
    if KEY_FILE not in files:
        return get_exam_dir(join(dirname, next(f for f in files if isdir(join(dirname, f)))))
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

success_count = 0
failure_count = 0

# Extract exam zipfile
chdir(EXAMS_DIR)
for f in listdir('.'):
    _, name = f.split('_')
    print(f'========== {name} ==========')

    # Extract exam zipfile
    TMP_DIR = join(EXAMS_DIR, 'tmp')
    exam_file = zipfile.ZipFile(join(f, listdir(f)[0]))
    exam_file.extractall(TMP_DIR)

    try:
        EXAM_DIR = get_exam_dir(TMP_DIR)
        NAME_DIR = join(EXAMS_DIR, name)
        shutil.move(EXAM_DIR, NAME_DIR)
        remove_dir_if_exists(f)
    except StopIteration:
        print(f'Error: {name} has no \'{KEY_FILE}\' in exam dir. You should check it yourself.')
        failure_count = failure_count + 1
    except Exception as e:
        print(f'Error: {e}')
        failure_count = failure_count + 1
    finally:
        remove_dir_if_exists('tmp')
    success_count = success_count + 1
    print('Successfully extracted 🎉 \n')

print(f'Success: {success_count} | Failure: {failure_count}')
