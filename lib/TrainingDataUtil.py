import os
import requests
import sys
import tarfile


class TrainingDataUtil:
    def __init__(self):
        pass

    training_data_dir = '../../../../data/'
    training_data_archive = 'training_data.tar.gz'

    # dataset
    # training_data_xml = 'train_debug.xml'
    # validation_data_xml = 'validation_resized.xml'
    # testing_data_xml = 'test.xml'

    # # resized
    training_data_xml = 'train_resized.xml'
    validation_data_xml = 'validation_resized.xml'
    testing_data_xml = 'test_resized.xml'

    # # original
    # training_data_dir = 'training_data'
    # training_data_archive = 'training_data.tar.gz'
    # training_data_xml = 'training.xml'
    # validation_data_xml = '../../../../data/validation_resized.xml'

    @ staticmethod
    def archive_training_data():
        if os.path.isfile(TrainingDataUtil.training_data_archive):
            if not TrainingDataUtil.__confirm_if_archive():
                return

        try:
            tar = tarfile.open(TrainingDataUtil.training_data_archive, 'w:gz')
            tar.add('training_data')
            tar.close()
        except Exception as e:
            print(e)

    @ staticmethod
    def extract_training_data():
        if not os.path.isdir(TrainingDataUtil.training_data_dir):
            tar = tarfile.open(TrainingDataUtil.training_data_archive, 'r:gz')
            tar.extractall()
            tar.close()

    @ staticmethod
    def download_training_data(url):
        if not TrainingDataUtil.__confirm_if_archive():
            return

        r = requests.get(url, stream=True)
        with open(TrainingDataUtil.training_data_archive, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    @ staticmethod
    def __confirm(question, default="yes"):
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}

        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")

    @ staticmethod
    def __confirm_if_archive():
        message = '{0} already exists, overwrite?'.format(
            TrainingDataUtil.training_data_archive
        )

        return TrainingDataUtil.__confirm(message)
