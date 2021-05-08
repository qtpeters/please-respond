from importlib_resources import files

def _get_data( json_file ):
    return files( "test.data" ) \
    .joinpath( json_file ) \
    .read_text()