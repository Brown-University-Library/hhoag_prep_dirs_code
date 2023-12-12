import logging, pathlib, os, pprint

from bs4 import BeautifulSoup


log = logging.getLogger( __name__ )
log.debug( 'mods-maker logging working' )


class ItemModsMaker:
    """ Creates the item_mods for the given source_org_ids. """
    def __init__(self):
        self.relevant_mods_paths = []

    ## manager function ---------------------------------------------

    def create_item_mods( self, org_ids: list, org_mods_files_dir_path: str, item_output_dirs: list ):
        """ Manages item-mods creation. 
            Called by make_dirs.prep_org_processing_dirs() """
        ## get mods-xml-files list ----------------------------------
        org_mods_files = self.get_org_mods_files( org_ids, org_mods_files_dir_path )
        ## laod mods-docs -------------------------------------------
        org_mods_docs = self.load_org_mods_docs( self.relevant_mods_paths )
        # for org_id in org_ids:
        #     ## get mods-docs for this org ----------------------------
        #     self.orgs_mods_docs = self.get_org_mods_docs( org_id, org_mods_files_dir_path )
            
        return 

    ## helper functions ---------------------------------------------

    def load_org_mods_docs( self, org_mods_paths: list ) -> None:
        """ Returns a list of mods-docs for the given org_mods_paths.
            Using lxml, read each file into an xml-object. 
            Called by create_item_mods() """
        log.debug( f'org_mods_paths, ``{org_mods_paths}``' )
        org_mods_docs = []
        for org_mods_path in org_mods_paths:
            with open( org_mods_path, 'r' ) as f:
                org_mods_docs.append( f.read() )
        log.debug( f'org_mods_docs, ``{org_mods_docs}``' )


    def get_org_mods_files( self, source_org_ids: list, org_mods_files_dir_path: str ) -> None:
        """ Finds the mods-xml-filepaths for the given org_ids.
            Stores them to self.relevant_mods_paths. 
            Called by create_item_mods() """
        log.debug( f'source_org_ids, ``{source_org_ids}``' )
        log.debug( f'org_mods_files_dir_path, ``{org_mods_files_dir_path}``' )
        ## get a list of xml files in org_mods_files_dir_path -------
        org_mods_paths = list( pathlib.Path( org_mods_files_dir_path ).glob( '*.xml' ) )
        log.debug( f'org_mods_paths, ``{pprint.pformat(org_mods_paths)}``' )
        found_org_mods_paths = []
        for source_org_id in source_org_ids:
            ## derive the org_id from the path in org_mods_paths
            for org_mods_path in org_mods_paths:
                filename_org_id = os.path.basename( org_mods_path ).split( '_' )[0]
                if source_org_id == filename_org_id:
                    log.debug( f'source_org_id, ``{source_org_id}`` found in path, ``{org_mods_path}``' )
                    found_org_mods_paths.append( org_mods_path )
        self.relevant_mods_paths = found_org_mods_paths
        log.debug( f'found_org_mods_paths, ``{pprint.pformat(self.relevant_mods_paths)}``' )
        return 
    
    def get_org_mods_docs( self, org_id: str, org_mods_files_dir_path: str ):
        """ Returns the mods-docs for the given org_id. 
            Called by create_item_mods() """
        ## get this org's mods-doc ----------------------------------
        org_mods_files = self.get_org_mods_files( org_id, org_mods_files_dir_path )
        org_mods_docs = self.get_org_mods_docs( org_mods_files )
        return org_mods_docs