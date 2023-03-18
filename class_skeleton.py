import sqlite3
import os

class DBWrapper(object):
    '''Wrapper class for handling an SQLite3 database. Convenience exceptions for handling erros included. Should inherit if additional functionality is needed.'''
    
    class MissingDBException(Exception):
        '''Exception raised when database file is missing from its home directory.'''
        
        def __init__(self):
            super().__init__("Missing database file. Note that this file should be manually added for data integrity, and a backup should be called upon should this file go missing.")

            
    class MissingTableException(Exception):
        '''Exception raised when table is missing from its home file.'''
        
        def __init__(self):
            super().__init__('''Missing table from database file. Missing database integrity, recommend that a backup be applied or a rollback done.''')

    
    def __init__(self, db_path="", auto_commits=""):
        '''Generic constructor for the class. Initializes database connection and ensures that at least one table exists.'''
        
        self.db_path = db_path
        self.auto_commits = auto_commits
        
        self.create_db()
        self.verify_integrity()


    def create_db(self):
        '''Helper method for connecting to a premade database.'''
        
        if not os.path.exists(self.db_path):
            raise DBWrapper.MissingDBException()
        
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

        
    def verify_integrity(self):
        '''Method for ensuring database table integrity. Should a table not meet standards, a warning is issued. Should be overidden if additional checks are required.'''
        
        if len(self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_data';").fetchall()) < 1:
            raise DBWrapper.MissingTableException()

        

class DBInstance(DBWrapper):
    '''Singleton Class for handling a database.'''

    class User():
        '''class encapsulating the defintion of a registered user in the database. Should inherit this when additional functionality is needed.'''
        
        def __init__(self, name="", active=True, auth_method="cleartext", password="", auth=True, roles=""):
            self.name = name
            self.active = active
            self.auth_method = auth_method
            self.password = password
            self.auth = auth
            self.roles = roles

        def __eq__(self, rh):
            '''Operator override on ==. Will return true if username and password match between two user objects.'''
            return self.name == rh.name and self.password == rh.password

        def to_string(self):
            return "username: %s, active: %d, authentication method: %s, password: %s, autheticated: %d, roles: %s" %(self.name, self.active, self.auth_method, self.password, self.auth, self.roles)
            
        
    def __new__(self, db_path, auto_commits):
        '''Ensures only a single instance is ever created. If a new one is created, a reference to the first instance created is returned.'''
        
        if not hasattr(self, 'instance'):
            self.instance = super(DBInstance, self).__new__(self)
        return self.instance
     
    def __init__(self, db_path, auto_commits):
        super().__init__(db_path, auto_commits)
        
                      
    def get_user(self, user):
        '''Method for returning a user based on unique username identifier. Requires a User object initialized with a name to function.'''
         
        result = self.cursor.execute("SELECT * FROM user_data WHERE username='%s';" %(user.name,)).fetchall()

        if len(result) < 1:
            return None
        
        user.name = result[0][0]
        user.active = result[0][1]
        user.auth_method = result[0][2]
        user.password = result[0][3]
        user.auth = result[0][4]
        user.roles = result[0][5]

        return user
        
        #IMPLEMENT ME!!! Add checks to ensure a user was returned. If not, raise exception to be handled externally.
        
    def delete_user(self, user):
        '''Delete a user entry in the database. Requires a User object initialized with a username to function.'''
        #IMPLEMENT ME!!!
        self.cursor.execute(f"INSERT INTO user_data (username, active, auth_method, password, auth, roles) VALUES('%s', %d, '%s', '%s', %d, '%s');" %
                            (user.name, user.active, user.auth_method, user.password, user.auth, user.roles,))
        if self.auto_commits:
            self.connection.commit()

    def edit_user(self, user):
        '''Edit a user entry in the database. Requires a completely initialized User object to function.'''
        #IMPLEMENT ME!!!
        self.cursor.execute(f"INSERT INTO user_data (username, active, auth_method, password, auth, roles) VALUES('%s', %d, '%s', '%s', %d, '%s');" %
                            (user.name, user.active, user.auth_method, user.password, user.auth, user.roles,))
        if self.auto_commits:
            self.connection.commit()
        
    def add_user(self, user):
        '''Adds a user to the database. Needs a completely initialized User object to function.'''

        self.cursor.execute(f"INSERT INTO user_data (username, active, auth_method, password, auth, roles) VALUES('%s', %d, '%s', '%s', %d, '%s');" %
                            (user.name, user.active, user.auth_method, user.password, user.auth, user.roles,))
        if self.auto_commits:
            self.connection.commit()

    def search_by(self, **kwargs):
        '''Returns a list of entries from the database based on key search parameters.'''
        #IMPLEMENT ME!!!
        
        if "order" in kwargs:
            pass #return results as a list of ordered users.
        if "column" in kwargs:
            pass #return results containing a certain attribute value.
        if "top" in kwargs:
            pass #return top-# of results in the given order and given selection.
        if "bottom" in kwargs:
            pass #return bottom-# of results in the given order and given selection.
        if "median" in kwargs:
            pass #return the median of results in the given order and given selection.
        else:
            raise ValueError("Invalid token in **kwargs.")
                             
        return user

    def exists(self, user):
        '''Returns if a user exists in the database.'''
        if not self.get_user(user.name):
            return False
        return True

    def commit(self):
        '''Manual commit of all transactions since previous commit.'''
        self.connection.commit()

    def rollback(self):
        '''Manual rollback of all transactions since previous commit.'''
        self.connection.rollback()

        
if __name__ == "__main__":
    test = DBInstance(db_path="users.db", global_commits=False)
    #test.add_user(DBInstance.User("cloyds1"))
    user = test.exists(DBInstance.User("cloyds1"))
    print(user)
