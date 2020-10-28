import yaml
import os
import random
import shutil


def load_configs():
    """
    Loads the project configurations.

    Returns
    -------
    configs : dict
        A dictionary containing the configs
    """
    with open('/content/drive/My Drive/Colab Notebooks/no-mask/configs/configs.yml', 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def check_if_dataset_dirs_exist(dirs):
    for f in dirs:
        if not os.path.exists(f):
            os.makedirs(f)


def count_files(path):
    files = os.listdir(path)
    return len(files)


def move_pair_to_train_dir(image_dir, train_dir, rand_pick):
    base = os.path.splitext(rand_pick)[0]
    txt_file = os.path.join(image_dir, base) + ".txt"
    jpg_file = os.path.join(image_dir, rand_pick)
    file_list = [jpg_file, txt_file]
    [shutil.move(os.path.join(image_dir, f), train_dir) for f in file_list]

def move_files_to_val_dir(image_dir, val_dir):
    filenames = os.listdir(image_dir)
    [shutil.move(os.path.join(image_dir, f), val_dir) for f in filenames]


def split_dataset():
    # Load configs
    cfg = load_configs()
    # Get dirs
    image_dir = cfg['data']['images_path']
    train_dir = cfg['data']['train_path']
    val_dir = cfg['data']['val_path']
    # Make list of dir names
    dataset_dirs = [train_dir, val_dir]
    # Check if train and val dirs exist, if not create them
    check_if_dataset_dirs_exist(dataset_dirs)
    # Count files in image dir
    file_count = (count_files(image_dir) / 2)
    print(f'file count: {file_count}')
    # Get train set size
    train_percent = cfg['data']['train_size']
    # Multiply train set size * file_count
    train_size = (train_percent * file_count) - 1
    print(f'train size: {train_size}')
    # For file in enumerate image dir
    for i in range(int(train_size)):
        # While i is < train_size
        if i < train_size:
            file_list = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.JPG'))]
            # Get random file which ends with .jpg from folder
            # if len(file_list) < 1:
            #     print('oops')
            rand_pick = random.choice(file_list)
            file_list.remove(rand_pick)
            move_pair_to_train_dir(image_dir, train_dir, rand_pick)

    move_files_to_val_dir(image_dir, val_dir)
    print(count_files(train_dir))
    print(count_files(val_dir))





