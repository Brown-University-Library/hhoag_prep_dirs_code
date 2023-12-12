"""
Creates all directories necessary for the project, as well as the item-mods.xml files.

Usage:
(venv) $ export PREP_DIRS__LOGLEVEL="INFO"  # optional; default is DEBUG
(venv) $ python ./make_dirs.py --org_image_dir "/path/to/org_imagages_dir" --output_dir "/path/to/output/dir"
"""

import argparse, datetime, logging, os, pathlib, pprint
from item_mods_maker import ItemModsMaker


lglvl: str = os.environ.get( 'PREP_DIRS__LOGLEVEL', 'DEBUG' )
lglvldct = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO }
logging.basicConfig(
    level=lglvldct[lglvl],  # assigns the level-object to the level-key loaded from the envar
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger( __name__ )
log.debug( 'logging working' )


## manager function -------------------------------------------------


def prep_org_processing_dirs( 
        org_ids_list: list, 
        processing_output_dir_root: str, 
        org_mods_files_dir_path: str, 
        org_image_dirs_root: str 
        ) -> None:
    """ Creates all directories necessary for each organization, as well as the item-mods.xml files.
        Called by dundermain. """
    log.debug( 'starting prep_org_processing_dirs()' )
    log.debug( f'org_ids_list, ``{org_ids_list}``' )
    log.debug( f'processing_output_dir_root, ``{processing_output_dir_root}``' )
    log.debug( f'org_mods_files_path, ``{org_mods_files_dir_path}``' )
    ## validate paths -----------------------------------------------
    validate_paths( processing_output_dir_root, org_mods_files_dir_path, org_image_dirs_root )  # will raise Exception on validation-failures
    validate_org_ids( org_ids_list )  # will raise Exception on validation-failures
    validate_image_dirs( org_ids_list, org_image_dirs_root )  # will raise Exception on validation-failures
    ## create org output dirs ---------------------------------------
    org_output_dir_paths: list = create_org_output_dirs( org_ids_list, processing_output_dir_root )
    assert type( org_output_dir_paths[0] ) == pathlib.PosixPath
    ## createitem output dirs ---------------------------------------
    item_output_dirs: list = create_item_output_dirs( org_image_dirs_root, org_output_dir_paths )
    assert type( item_output_dirs[0] ) == pathlib.PosixPath
    ## create item-mods ---------------------------------------------
    item_mods_maker = ItemModsMaker()
    item_mods_maker.create_item_mods( org_ids_list, org_mods_files_dir_path, item_output_dirs )
    return


## helper functions -------------------------------------------------


def create_item_output_dirs( org_image_dirs_root: str, org_output_dir_paths: list ) -> list:
    """ Creates the item-output-dirs.
        For each org in org_output_dir_paths...
        - gets the org-id
        - uses the org-id to get the org-image-dir-path
        - gets a list of the image-filenames in the org-image-dir
        - creates an item-output-dir for each image-filename
        Retuns back a list of all the item-output-dirs.
        Called by prep_org_processing_dirs() """
    log.debug( 'starting create_item_output_dirs()' )
    log.debug( f'org_output_dir_paths, ``{org_output_dir_paths}``' )
    item_output_dir_paths = []
    for org_output_dir_path in org_output_dir_paths:
        assert type( org_output_dir_path ) == pathlib.PosixPath
        org_id = org_output_dir_path.name
        log.debug( f'org_id, ``{org_id}``' )
        org_image_dir_path = pathlib.Path( org_image_dirs_root, org_id )
        org_image_filenames = os.listdir( org_image_dir_path )
        for org_image_filename in org_image_filenames:
            org_image_root_filename = pathlib.Path( org_image_filename ).stem
            item_output_dir_path = pathlib.Path( org_output_dir_path, org_image_root_filename )
            item_output_dir_paths.append( item_output_dir_path )
            if not item_output_dir_path.exists():
                os.makedirs( item_output_dir_path )
                log.debug( f'created item_output_dir_path, ``{item_output_dir_path}``' )
            else:
                log.debug( f'item_output_dir_path, ``{item_output_dir_path}`` already exists' )
    log.debug( f'item_output_dir_paths, ``{pprint.pformat(item_output_dir_paths)}``' )
    log.info( 'all item-output-dirs created' )
    return item_output_dir_paths


def create_org_output_dirs( org_ids_list, processing_output_dir_root ) -> list:
    """ Creates the org-output-dirs and returns list of paths.
        Called by prep_org_processing_dirs() """
    org_output_dir_paths = []
    for org_id in org_ids_list:
        org_output_dir_path = pathlib.Path( processing_output_dir_root, org_id )
        org_output_dir_paths.append( org_output_dir_path )
        if not org_output_dir_path.exists():
            os.makedirs( org_output_dir_path )
            log.debug( f'created output_dir_path, ``{org_output_dir_path}``' )
        else:
            log.debug( f'output_dir_path, ``{org_output_dir_path}`` already exists' )
    log.info( 'all output-dirs created' )
    return org_output_dir_paths


def validate_image_dirs( org_ids_list: list, org_image_dirs_root: str ) -> None:
    """ Ensures that each image-directory exists, and contain items.
        Called by prep_org_processing_dirs() """
    log.debug( 'starting validate_image_dirs()' )
    log.debug( f'org_ids_list, ``{org_ids_list}``' )
    log.debug( f'org_image_dirs_root, ``{org_image_dirs_root}``' )
    ## check that each org-image-dir exists -------------------------
    for org_id in org_ids_list:
        org_image_dir_path = pathlib.Path( org_image_dirs_root, org_id )
        if not org_image_dir_path.exists():
            msg = f'org-image-dir, ``{org_image_dir_path}`` does not exist; exiting'
            log.error( msg )
            raise Exception( msg )
        if not org_image_dir_path.is_dir():
            msg = f'org-image-dir, ``{org_image_dir_path}`` is not a directory; exiting'
            log.error( msg )
            raise Exception( msg )
        ## check that each org-image-dir contains items ----------------
        org_image_dir_contents = os.listdir( org_image_dir_path )
        if len( org_image_dir_contents ) == 0:
            msg = f'org-image-dir, ``{org_image_dir_path}`` is empty; exiting'
            log.error( msg )
            raise Exception( msg )
    log.info( 'all org-image-dirs are valid, and contain items' )
    return


def validate_org_ids( org_ids_list: list ) -> None:
    """ Checks that the org_ids are valid.
        Called by prep_org_processing_dirs() """
    log.debug( 'starting validate_org_ids()' )
    log.debug( f'org_ids_list, ``{org_ids_list}``' )
    source_org_ids = [ 'HH020005', 'HH024889' ]  # 'American Mercury', 'Christian Coalition'
    ## get list of mods files ----------------------------------------
    mods_files: list = os.listdir( org_mods_files_dir_path )
    if len( mods_files ) == 0:
        msg = f'no mods files found in ``{org_mods_files_dir_path}``; exiting'
        log.error( msg )
        raise Exception( msg )
    ## make list of org-ids from mods filenames ---------------------
    mods_org_ids: list = []
    for mods_file in mods_files:  # assumes filename like 'HH123456_mods.xml'
        root_filename = pathlib.Path( mods_file ).stem
        mods_org_id = root_filename.split( '_' )[0]
        mods_org_ids.append( mods_org_id )
    ## check that source org_ids are valid -------------------------------
    for source_org_id in source_org_ids:
        if source_org_id not in mods_org_ids:
            msg = f'source org_id, ``{source_org_id}`` is not in mods_org_ids; exiting'
            log.error( msg )
            raise Exception( msg )
    log.info( 'all source org_ids are valid' )
    return


def validate_paths( processing_output_dir_root: str, 
                   org_mods_files_dir_path: str, 
                   org_image_dirs_root: str 
                   ) -> None:
    """ Checks that the paths exist, and are directories.
        Called by prep_org_processing_dirs() """
    log.debug( 'starting validate_paths()' )
    log.debug( f'processing_output_dir_root, ``{processing_output_dir_root}``' )
    log.debug( f'org_mods_files_path, ``{org_mods_files_dir_path}``' )
    ## check processing_output_dir_root -----------------------------
    if not os.path.exists( processing_output_dir_root ):
        msg = f'shared-mount for processed-files_dir, ``{processing_output_dir_root}`` does not exist; exiting'
        log.error( msg )
        raise Exception( msg )
    if not os.path.isdir( processing_output_dir_root ):
        msg = f'shared-mount for processed-files_dir, ``{processing_output_dir_root}`` is not a directory; exiting'
        log.error( msg )
        raise Exception( msg )
    ## -- check org_mods_files_dir_path -----------------------------
    if not os.path.exists( org_mods_files_dir_path ):
        msg = f'org_mods_files_path, ``{org_mods_files_dir_path}`` does not exist; exiting'
        log.error( msg )
        raise Exception( msg )
    if not os.path.isdir( org_mods_files_dir_path ):
        msg = f'org_mods_files_path, ``{org_mods_files_dir_path}`` is not a directory; exiting'
        log.error( msg )
        raise Exception( msg )
    ## -- check org_image_dirs_root ---------------------------------
    if not os.path.exists( org_image_dirs_root ):
        msg = f'org_image_dirs_root, ``{org_image_dirs_root}`` does not exist; exiting'
        log.error( msg )
        raise Exception( msg )
    if not os.path.isdir( org_image_dirs_root ):
        msg = f'org_image_dirs_root, ``{org_image_dirs_root}`` is not a directory; exiting'
        log.error( msg )
        raise Exception( msg )
    log.info( 'the shared-mount for processed-files-directory and the org-mods-files-directory paths are valid' )
    return


## dunndermain ------------------------------------------------------


if __name__ == '__main__':
    ## set up argparser ---------------------------------------------
    log.debug( '\n\nstarting processing' )
    start_time = datetime.datetime.now()
    parser = argparse.ArgumentParser(description='Creates all directories necessary for the project, as well as the item-mods.xml files.')
    parser.add_argument('--org_IDs', type=str, help='comma-separated list of org IDs')
    args = parser.parse_args()
    log.debug( f'args: {args}' )
    ## get org IDs --------------------------------------------------
    org_ids_string = args.org_image_dir if args.org_IDs else 'HH020005,HH024889'  # 'American Mercury', 'Christian Coalition'
    log.debug( f'org_ids_string: {org_ids_string}' )
    org_ids_list = org_ids_string.split( ',' )
    cleaned_org_ids_list = [ org_id.strip() for org_id in org_ids_list ]
    log.debug( f'cleaned_org_ids_list, ``{cleaned_org_ids_list}``' )
    ## get output dir -----------------------------------------------
    processing_output_dir_root = os.getenv( 'PREP_DIRS__PROCESSING_OUTPUT_DIR', '../output_dir' )
    log.debug( f'processing_output_dir_root, ``{processing_output_dir_root}``' )
    ## get org_mods_files path --------------------------------------
    org_mods_files_dir_path = os.getenv( 'PREP_DIRS__ORG_MODS_FILES_PATH', '../org_mods_files' )
    log.debug( f'org_mods_files_path, ``{org_mods_files_dir_path}``')
    ## get dir containing org-image-dirs ---------------------------
    org_image_dirs_root = os.getenv( 'PREP_DIRS__ORG_IMAGE_DIRS_ROOT', '../org_image_dirs' )
    log.debug( f'org_image_dirs_root, ``{org_image_dirs_root}``' )
    ## get to work --------------------------------------------------
    prep_org_processing_dirs( cleaned_org_ids_list, processing_output_dir_root, org_mods_files_dir_path, org_image_dirs_root )
    ## end ----------------------------------------------------------
    elapsed_time = datetime.datetime.now() - start_time
    log.debug( f'done processing; elapsed processing time, ``{elapsed_time}``' )
