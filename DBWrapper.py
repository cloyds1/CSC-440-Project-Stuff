'''
    DATABASE FRAMEWORK V1.0
    AUTHOR: SEAN CLOYD
    EMAIL: cloyds1@mymail.nku.edu
    3/17/2023
    
'''
import sqlite3
import os

class DBWrapper(object):
    '''Wrapper class for handling an SQLite3 database. Convenience exceptions for handling erros included. Should inherit if additional functionality is needed.'''

    connection = None
    
    class Model:
        '''Generic Model for creating database schemas. Inherit for additional functionality'''
        
        def __init__(self, identifier):
            self.identifier = identifier

        def __eq__(self, rh):
            '''Operator override on ==. Will return true if username and password match between two user objects.'''
            return self.identifier == rh.identifier

        def to_string(self):
            return "Identifier: " + self.identifier
    
    class MissingDBException(Exception):
        '''Exception raised when database file is missing from its home directory.'''
        
        def __init__(self):
            super().__init__("Missing database file. Note that this file should be manually added for data integrity, and a backup should be called upon should this file go missing.")

            
    class MissingTableException(Exception):
        '''Exception raised when table is missing from its home file.'''
        
        def __init__(self):
            super().__init__('''Missing table from database file. Missing database integrity, recommend that a backup be applied or a rollback done.''')

    class MissingImplementationException(Exception):
        '''Exception raised when a method is missing its implementation.'''
        
        def __init__(self, func):
            super().__init__('''Missing implementation of ''' + func + "().")

    
    def __init__(self, db_path="", auto_commits=""):
        '''Generic constructor for the class. Initializes database connection and ensures that at least one table exists.'''
        
        self.db_path = db_path
        self.auto_commits = auto_commits
        
        self.connect_db()
        self.verify_integrity()

    def connect_db(self):
        '''Helper method for connecting to a premade database.'''
        
        if not os.path.exists(self.db_path):
            raise DBWrapper.MissingDBException()

        if DBWrapper.connection == None:
            DBWrapper.connection = sqlite3.connect(self.db_path)
            
        self.cursor = self.connection.cursor()

    def verify_integrity(self):
        '''Method for ensuring database table integrity. Should a table not meet standards, a warning is issued. Should be overidden if additional checks are required.'''
        
        if len(self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_data';").fetchall()) < 1:
            raise DBWrapper.MissingTableException()

    def commit(self):
        '''Manual commit of all transactions since previous commit.'''
        self.connection.commit()

    def rollback(self):
        '''Manual rollback of all transactions since previous commit.'''
        self.connection.rollback()

    def add(self, obj):
        '''Abstract method for adding an entity to a generic database.'''
        raise DBWrapper.MissingImplementationException(DBWrapper.add.__name__)
    
    def exists(self, obj):
        '''Abstract method for adding an entity to a generic database.'''
        raise DBWrapper.MissingImplementationException(DBWrapper.exists.__name__)

    def get(self, obj):
        '''Abstract method for adding an entity to a generic database.'''
        raise DBWrapper.MissingImplementationException(DBWrapper.get.__name__)

    def delete(self, obj):
        '''Abstract method for adding an entity to a generic database.'''
        raise DBWrapper.MissingImplementationException(DBWrapper.delete.__name__)

    def edit(self, obj):
        '''Abstract method for adding an entity to a generic database.'''
        raise DBWrapper.MissingImplementationException(DBWrapper.edit.__name__)

    def search(self, **kwargs):
        '''Abstract method for adding an entity to a generic database.'''
        raise DBWrapper.MissingImplementationException(DBWrapper.search.__name__)

    def auto_commit(func):
        '''Decorator for methods that modify a database, allowing rollback and commit support.'''
        def wrap(self, obj):
            func(self, obj)
            if self.auto_commits:
                self.connection.commit()
        return wrap


if __name__ == "__main__":
    pass
