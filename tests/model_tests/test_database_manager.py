import pytest
from src.model.managers.database_manager import DatabaseManager

@pytest.fixture
def db_manager():
    # Create an in-memory SQLite database for testing
    db_path = ":memory:"
    manager = DatabaseManager.get_instance(db_path)

    # Set up the in-memory database schema and populate it with test data
    manager.connect()
    cursor = manager.connection.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE items (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        target TEXT,
        one_time_item INTEGER,
        effect_min INTEGER,
        effect_max INTEGER,
        buff_type TEXT
    )''')

    cursor.execute('''CREATE TABLE rooms (
        doors TEXT,
        image_path TEXT,
        rotation INTEGER
    )''')

    cursor.execute('''CREATE TABLE monsters (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        max_HP INTEGER,
        attack_speed INTEGER,
        chance_to_hit REAL,
        attack_damage_min INTEGER,
        attack_damage_max INTEGER,
        chance_to_heal REAL,
        heal_range_min INTEGER,
        heal_range_max INTEGER
    )''')

    cursor.execute('''CREATE TABLE adventurers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        max_hp INTEGER,
        attack_speed INTEGER,
        chance_to_hit REAL,
        attack_damage_min INTEGER,
        attack_damage_max INTEGER,
        chance_to_block REAL,
        special_attack TEXT
    )''')

    # Insert test data, ideas for potential future updates
    cursor.executemany('''INSERT INTO items (id, name, description, target, one_time_item, effect_min, effect_max, buff_type) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      [(1, 'Sword', 'A sharp blade', 'enemy', 1, 10, 15, 'damage'),
                       (2, 'Shield', 'Protects the user', 'self', 0, 5, 10, 'defense')])

    cursor.executemany('''INSERT INTO rooms (doors, image_path, rotation) 
                          VALUES (?, ?, ?)''',
                      [('TTFF', '/images/room1.png', 90),
                       ('FFFT', '/images/room2.png', 0)])

    cursor.executemany('''INSERT INTO monsters (id, name, type, max_HP, attack_speed, chance_to_hit, 
                                                attack_damage_min, attack_damage_max, chance_to_heal, 
                                                heal_range_min, heal_range_max) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      [(1, 'Hound', 'normal', 30, 2, 0.8, 5, 10, 0.1, 3, 5),
                       (2, 'Teacher', 'elite', 200, 1, 0.9, 20, 50, 0.2, 10, 30)])

    cursor.executemany('''INSERT INTO adventurers (id, name, type, max_hp, attack_speed, chance_to_hit, 
                                                   attack_damage_min, attack_damage_max, chance_to_block, special_attack) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      [(1, 'Knight', 'melee', 100, 3, 0.7, 15, 20, 0.3, 'Shield Bash'),
                       (2, 'Wizard', 'magic', 80, 2, 0.6, 10, 25, 0.1, 'Fireball')])

    manager.connection.commit()
    yield manager

    # Clean up: Close connection after each test
    manager.close_connection()

def test_fetch_items(db_manager):
    items = db_manager.fetch_items()
    assert len(items) == 2
    assert items[0][1] == 'Sword'
    assert items[1][1] == 'Shield'

def test_fetch_rooms(db_manager):
    rooms = db_manager.fetch_rooms()
    assert len(rooms) == 2
    assert rooms[0][1] == '/images/room1.png'

def test_fetch_monsters(db_manager):
    monsters = db_manager.fetch_monsters()
    assert len(monsters) == 2
    assert monsters[0][1] == 'Hound'
    assert monsters[1][1] == 'Teacher'

def test_fetch_adventurers(db_manager):
    adventurers = db_manager.fetch_adventurers()
    assert len(adventurers) == 2
    assert adventurers[0][1] == 'Knight'
    assert adventurers[1][1] == 'Wizard'

def test_empty_tables(db_manager):
    db_manager.connection.execute("DELETE FROM items")
    db_manager.connection.execute("DELETE FROM rooms")
    db_manager.connection.execute("DELETE FROM monsters")
    db_manager.connection.execute("DELETE FROM adventurers")
    db_manager.connection.commit()

    assert db_manager.fetch_items() == []
    assert db_manager.fetch_rooms() == []
    assert db_manager.fetch_monsters() == []
    assert db_manager.fetch_adventurers() == []

def test_missing_tables(db_manager):
    # Drop the rooms table
    db_manager.connection.execute("DROP TABLE rooms")
    db_manager.connection.commit()

    # Attempt to fetch rooms, expecting an empty list or an error based on implementation
    result = db_manager.fetch_rooms()
    assert result == []  # Expect empty result as the method handles missing tables gracefully

def test_invalid_query(db_manager):
    invalid_query = "SELECT * FROM non_existing_table"
    result = db_manager.execute_query(invalid_query)
    assert result == []  # Expect an empty result due to error handling

def test_data_consistency(db_manager):
    items = db_manager.fetch_items()
    assert len(items) > 0
    for item in items:
        assert len(item) == 8  # Ensure all columns are returned
        assert isinstance(item[0], int)  # ID
        assert isinstance(item[1], str)  # Name
        assert isinstance(item[2], str)  # Description

def test_singleton_behavior():
    instance1 = DatabaseManager.get_instance(":memory:")
    instance2 = DatabaseManager.get_instance(":memory:")
    assert instance1 is instance2  # Both should be the same instance

def test_edge_case_data(db_manager):
    db_manager.connection.execute("INSERT INTO items VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                  (3, '', '', 'enemy', 0, -10, -15, None))
    db_manager.connection.commit()
    items = db_manager.fetch_items()
    assert len(items) == 3  # Include edge case item
    assert items[-1][1] == ''  # Check empty name
    assert items[-1][5] == -10  # Check negative effect_min

def test_sql_injection(db_manager):
    malicious_input = "1; DROP TABLE items"
    result = db_manager.execute_query("SELECT * FROM items WHERE id = ?", (malicious_input,))
    assert result == []  # No data should match