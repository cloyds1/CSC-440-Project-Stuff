'''
    DATABASE FRAMEWORK V1.0
    AUTHOR: SEAN CLOYD
    EMAIL: cloyds1@mymail.nku.edu
    3/17/2023
    
'''

from DBWrapper import *

class UserDBInstance(DBWrapper):
    '''Singleton Class for handling a database.'''

    class User(DBWrapper.Model):
        '''class encapsulating the defintion of a registered user in the database.'''
        
        def __init__(self, name="", active=True, auth_method="cleartext", password="", auth=True, roles=""):
            super().__init__(name)
            self.active = active
            self.auth_method = auth_method
            self.password = password
            self.auth = auth
            self.roles = roles

        def __eq__(self, rh):
            '''Operator override on ==. Will return true if username and password match between two user objects.'''
            return self.name == rh.name and self.password == rh.password

        def to_string(self):
            return "Username: %s, Active: %d, Authentication method: %s, Password: %s, Autheticated: %d, Roles: %s" %(self.identifier, self.active, self.auth_method, self.password, self.auth, self.roles)
            
        
    def __new__(self, db_path, auto_commits):
        '''Ensures only a single instance is ever created. If a new one is created, a reference to the first instance created is returned.'''
        
        if not hasattr(self, 'instance'):
            self.instance = super(UserDBInstance, self).__new__(self)
        return self.instance
     
    def __init__(self, db_path, auto_commits):
        
        super().__init__(db_path, auto_commits)

               
    def get(self, obj):
        '''Method for returning a user based on unique username identifier. Requires a User object initialized with a name to function.'''
         
        result = self.cursor.execute("SELECT * FROM user_data WHERE username='%s';" %(obj.identifier,)).fetchall()

        if len(result) < 1:
            return None
        
        obj.identifier = result[0][0]
        obj.active = result[0][1]
        obj.auth_method = result[0][2]
        obj.password = result[0][3]
        obj.auth = result[0][4]
        obj.roles = result[0][5]

        return obj
        
        #IMPLEMENT ME!!! Add checks to ensure a user was returned. If not, raise exception to be handled externally.
    
    @DBWrapper.auto_commit   
    def delete(self, obj):
        '''Delete a user entry in the database. Requires a User object initialized with a username to function.'''

        self.cursor.execute(f"DELETE FROM user_data WHERE username = %s" %(obj.name,))
        
    @DBWrapper.auto_commit 
    def edit(self, obj):
        '''Edit a user entry in the database. Requires a completely initialized User object to function.'''
        pass
        #self.cursor.execute(f"UPDATE INTO user_data (username, active, auth_method, password, auth, roles) VALUES('%s', %d, '%s', '%s', %d, '%s');" %
                            #(user.name, user.active, user.auth_method, user.password, user.auth, user.roles,))
            
    @DBWrapper.auto_commit 
    def add(self, obj):
        pass
        '''Adds a user to the database. Needs a completely initialized User object to function.'''

        self.cursor.execute(f"INSERT INTO user_data (username, active, auth_method, password, auth, roles) VALUES('%s', %d, '%s', '%s', %d, '%s');" %
                            (obj.identifier, obj.active, obj.auth_method, obj.password, obj.auth, obj.roles,))

    def exists(self, obj):
        '''Returns if a user exists in the database.'''
        if not self.get(obj.identifier):
            return False
        return True


if __name__ == "__main__":
    test = UserDBInstance("users.db", auto_commits=True)
    
    user = test.get(UserDBInstance.User("cloyds1"))
    print(user.to_string())
    
    #test.add(UserDBInstance.User("another user", password="hello"))

    user = test.get(UserDBInstance.User("another user"))
             
    print(user.to_string())
