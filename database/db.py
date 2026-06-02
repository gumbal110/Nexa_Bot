import sqlite3
import os
from datetime import datetime

DB_PATH = 'data/bot.db'

def init_db():
    """Inicializa la base de datos"""
    os.makedirs('data', exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabla de advertencias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            moderator_id INTEGER NOT NULL,
            reason TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de configuración de gremios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guild_config (
            guild_id INTEGER PRIMARY KEY,
            welcome_channel_id INTEGER,
            welcome_message TEXT,
            dm_message TEXT,
            enabled BOOLEAN DEFAULT 0
        )
    ''')
    
    # Tabla de roles de moderación
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mod_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            UNIQUE(guild_id, role_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada")

def add_warning(guild_id, user_id, moderator_id, reason):
    """Agrega una advertencia"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO warnings (guild_id, user_id, moderator_id, reason)
        VALUES (?, ?, ?, ?)
    ''', (guild_id, user_id, moderator_id, reason))
    
    conn.commit()
    conn.close()

def get_warnings(guild_id, user_id):
    """Obtiene advertencias de un usuario"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM warnings
        WHERE guild_id = ? AND user_id = ?
        ORDER BY date DESC
    ''', (guild_id, user_id))
    
    warnings = cursor.fetchall()
    conn.close()
    
    return warnings

def count_warnings(guild_id, user_id):
    """Cuenta las advertencias de un usuario"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) FROM warnings
        WHERE guild_id = ? AND user_id = ?
    ''', (guild_id, user_id))
    
    count = cursor.fetchone()[0]
    conn.close()
    
    return count

def add_mod_role(guild_id, role_id):
    """Agrega un rol de moderación"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO mod_roles (guild_id, role_id)
        VALUES (?, ?)
    ''', (guild_id, role_id))
    
    conn.commit()
    conn.close()

def remove_mod_role(guild_id, role_id):
    """Remueve un rol de moderación"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM mod_roles
        WHERE guild_id = ? AND role_id = ?
    ''', (guild_id, role_id))
    
    conn.commit()
    conn.close()

def get_mod_roles(guild_id):
    """Obtiene los roles de moderación de un gremio"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT role_id FROM mod_roles
        WHERE guild_id = ?
    ''', (guild_id,))
    
    roles = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return roles

def set_welcome_channel(guild_id, channel_id):
    """Establece el canal de bienvenida"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO guild_config (guild_id, welcome_channel_id, enabled)
        VALUES (?, ?, 1)
    ''', (guild_id, channel_id))
    
    conn.commit()
    conn.close()

def set_welcome_message(guild_id, message):
    """Establece el mensaje de bienvenida"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO guild_config (guild_id) VALUES (?)
    ''', (guild_id,))
    
    cursor.execute('''
        UPDATE guild_config
        SET welcome_message = ?
        WHERE guild_id = ?
    ''', (message, guild_id))
    
    conn.commit()
    conn.close()

def set_dm_message(guild_id, message):
    """Establece el mensaje privado de bienvenida"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO guild_config (guild_id) VALUES (?)
    ''', (guild_id,))
    
    cursor.execute('''
        UPDATE guild_config
        SET dm_message = ?
        WHERE guild_id = ?
    ''', (message, guild_id))
    
    conn.commit()
    conn.close()

def get_guild_config(guild_id):
    """Obtiene la configuración de un gremio"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM guild_config
        WHERE guild_id = ?
    ''', (guild_id,))
    
    config = cursor.fetchone()
    conn.close()
    
    return config
