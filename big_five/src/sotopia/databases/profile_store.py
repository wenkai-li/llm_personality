import io
import json
import os
import uuid
from typing import Dict, Any
from tinydb import TinyDB, Query, JSONStorage

class IndentedJSONStorage(JSONStorage):
    def write(self, data: Dict[str, Dict[str, Any]]):
        # Move the cursor to the beginning of the file just in case
        self._handle.seek(0)

        # Serialize the database state using the user-provided arguments
        serialized = json.dumps(data, indent=2, **self.kwargs)

        # Write the serialized data to the file
        try:
            self._handle.write(serialized)
        except io.UnsupportedOperation:
            raise IOError('Cannot write to the database. Access mode is "{0}"'.format(self._mode))

        # Ensure the file has been written
        self._handle.flush()
        os.fsync(self._handle.fileno())

        # Remove data that is behind the new cursor in case the file has
        # gotten shorter
        self._handle.truncate()

class ProfileStore:
    def __init__(self, args, database_name):
        database_file = args.database_folder.format(database_name=database_name)
        self.db = TinyDB(database_file, storage=IndentedJSONStorage)
    
    def insert(self, profile: dict):
        # profile_id = str(uuid.uuid4())
        # profile['pk'] = profile_id
        self.db.insert(profile)

    def build_query(self, **kwargs):
        User = Query()
        query = None
        for key, val in kwargs.items():
            if query is None:
                query = (User[key] == val)
            else:
                query = query & (User[key] == val)
        return query
    
    def get(self, **kwargs):
        return self.db.get(cond=self.build_query(**kwargs))
    
    def get_pk(self, pk: str):
        return self.db.get(doc_id=int(pk))
    
    def search(self, **kwargs):
        return self.db.search(cond=self.build_query(**kwargs))
    
    def contains(self, **kwargs):
        return self.db.contains(cond=self.build_query(**kwargs))
    
    def insert_unique(self, profile: dict):
        if self.contains(**profile):
            return
        else:
            self.insert(profile)
    
    def all(self):
        return self.db.all()

    def all_pks(self):
        return [str(doc.doc_id) for doc in self.all()]