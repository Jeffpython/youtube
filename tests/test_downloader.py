from youtube.downloader import remove_original_file


def test__remove_original_file__do_nothing_if_empty_filepath(os_remove_mock):
    remove_original_file('')
    assert os_remove_mock.call_count == 0


def test__remove_original_file__do_not_try_to_remove_not_existing_file(os_path_exists_mock, file_path, os_remove_mock):
    os_path_exists_mock.return_value = False
    remove_original_file(file_path)
    args = os_path_exists_mock.call_args.args

    assert os_path_exists_mock.call_count == 1
    assert args[0] == file_path
    assert os_remove_mock.call_count == 0


def test__remove_original_file__deletes_file(os_path_exists_mock, file_path, os_remove_mock):
    os_path_exists_mock.return_value = True
    remove_original_file(file_path)
    args = os_remove_mock.call_args.args

    assert os_path_exists_mock.call_count == 1
    assert os_remove_mock.call_count == 1
    assert args[0] == file_path
