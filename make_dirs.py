"""
Creates all directories necessary for the project, as well as the item-mods.xml files.

Usage:
(venv) $ python ./make_dirs.py --org_image_dir "/path/to/org_imagages_dir" --output_dir "/path/to/output/dir"
"""

import argparse, csv, datetime, json, logging, os, pprint


lglvl: str = os.environ.get( 'LOGLEVEL', 'DEBUG' )
lglvldct = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO }
logging.basicConfig(
    level=lglvldct[lglvl],  # assigns the level-object to the level-key
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger( __name__ )
log.debug( 'logging working' )


def prep_org_processing_dirs( org_ids_list: list, processing_output_dir_root: str, org_mods_files_dir_path: str ) -> None:
    """ Creates all directories necessary for each organization, as well as the item-mods.xml files.
        Called by dundermain. """
    log.debug( 'starting prep_org_processing_dirs()' )
    log.debug( f'org_ids_list, ``{org_ids_list}``' )
    log.debug( f'processing_output_dir_root, ``{processing_output_dir_root}``' )
    log.debug( f'org_mods_files_path, ``{org_mods_files_dir_path}``' )
    validate_paths( processing_output_dir_root, org_mods_files_dir_path )
    pass
    return


def validate_paths( processing_output_dir_root: str, org_mods_files_dir_path: str ) -> None:
    """ Checks that the paths exist.
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
    return


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
    processing_output_dir_root = os.getenv( 'PROCESSING_OUTPUT_DIR', '../output_dir' )
    log.debug( f'processing_output_dir_root, ``{processing_output_dir_root}``' )
    ## get org_mods_files path --------------------------------------
    org_mods_files_dir_path = os.getenv( 'ORG_MODS_FILES_PATH', '../org_mods_files' )
    log.debug( f'org_mods_files_path, ``{org_mods_files_dir_path}``')
    ## get to work
    prep_org_processing_dirs( cleaned_org_ids_list, processing_output_dir_root, org_mods_files_dir_path )
    ## end ----------------------------------------------------------
    elapsed_time = datetime.datetime.now() - start_time
    log.debug( f'done processing; elapsed processing time, ``{elapsed_time}``' )
