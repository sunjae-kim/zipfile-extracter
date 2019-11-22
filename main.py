from os import listdir, getcwd, makedirs, chdir
from os.path import join, isdir, exists
import zipfile
import shutil

KEY_FILE = 'manage.py'              # 교육생 제출파일에서 해당파일이 있는 폴더들만 모아준다.
DJANGO_APP_DIR_PATH = 'articles'    # Django 에서 test.py 파일이 들어갈 app 이름을 작성한다.

TEST_FILE_PATH = join(getcwd(), 'tests.py')
HAS_TEST_FILE = exists(TEST_FILE_PATH)

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

        if HAS_TEST_FILE:
            shutil.copyfile(TEST_FILE_PATH, join(EXAM_DIR, DJANGO_APP_DIR_PATH, 'tests.py'))

        shutil.move(EXAM_DIR, NAME_DIR)
        remove_dir_if_exists(f)
        success_count = success_count + 1
        print('Successfully extracted 🎉 \n')
    except StopIteration:
        print(f'Error: {name} has no \'{KEY_FILE}\' in exam dir. You should check it yourself.')
        failure_count = failure_count + 1
    except Exception as e:
        print(f'Error: {e}. You should check it yourself.')
        failure_count = failure_count + 1
    finally:
        remove_dir_if_exists('tmp')

if not HAS_TEST_FILE:
    print('Warning: The test file does not exits. Please add the test file and try again.')
print(f'Success: {success_count} | Failure: {failure_count}')
