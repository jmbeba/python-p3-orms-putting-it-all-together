import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    all = []
    
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        CURSOR.execute('''DROP TABLE IF EXISTS dogs''')
        
        sql = '''CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )'''
        
        CURSOR.execute(sql)
        
    @classmethod
    def drop_table(cls):
        CURSOR.execute('DROP TABLE IF EXISTS dogs')
        
    def save(self):
        sql = ''' INSERT INTO dogs (name, breed) VALUES (?,?)'''
        
        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.execute('SELECT last_insert_rowid() FROM dogs').fetchone()[0]
        
    @classmethod    
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def get_all(cls):
        all = CURSOR.execute('SELECT * FROM dogs').fetchall()
        
        cls.all = [cls.new_from_db(dog) for dog in all]
        return cls.all
        
    @classmethod
    def find_by_name(cls, name):
        sql = '''SELECT * FROM dogs WHERE name = ? LIMIT 1'''
        
        dog = CURSOR.execute(sql, (name,)).fetchone()
        
        if not dog:
            return None
           
        return Dog.new_from_db(dog)
        
    @classmethod
    def find_by_id(cls, id):
        sql = '''SELECT * FROM dogs WHERE id = ? LIMIT 1'''
        
        dog = CURSOR.execute(sql,(id,)).fetchone()
        return Dog.new_from_db(dog)
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = '''SELECT * FROM dogs WHERE name = ? AND breed = ? LIMIT 1'''
        
        dog = CURSOR.execute(sql, (name, breed)).fetchone()
        
        if not dog:
             return cls.create(name, breed)
            
        return Dog.new_from_db(dog)
    
    def update(self):
        sql = '''UPDATE dogs SET name = ?'''
        
        CURSOR.execute(sql, (self.name,))