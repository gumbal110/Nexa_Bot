# Nexa Bot - Python Edition 🐍

**Nexa** es un bot de Discord completamente funcional en **Python** con **SQLite**, especializado en moderación y administración de servidores.

## 🎯 Características

✅ **Moderación Completa**
- Ban, Kick, Mute, Unmute
- Sistema de Advertencias
- Limpieza de Mensajes
- Modo Lento
- Lock/Unlock

✅ **Permisos Personalizados**
- Asignar Roles de Moderación
- Sistema Flexible

✅ **Bienvenida Automática**
- Mensajes en Canal
- DM Privados
- Variables Dinámicas

✅ **Base de Datos SQLite**
- Ligera y Rápida
- Persistencia Local

✅ **Comandos Slash** (/comando)
- Fácil de Usar
- 20+ Comandos

## 📋 Stack

- **Python 3.8+**
- **discord.py 2.3.2**
- **SQLite3** (incluido en Python)
- **dotenv** para variables de entorno

## 🚀 Instalación

### 1️⃣ Instalar Python
Descarga desde https://www.python.org (3.8+)

### 2️⃣ Clonar Repositorio
```bash
cd Nexa-Python
```

### 3️⃣ Crear Entorno Virtual (Opcional pero recomendado)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 4️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 5️⃣ Configurar .env
Edita `.env` con tus credenciales:
```env
DISCORD_TOKEN=tu_token_de_discord
CLIENT_ID=tu_client_id
GUILD_ID=tu_guild_id
```

### 6️⃣ Ejecutar Bot
```bash
python main.py
```

## 🎮 Comandos Disponibles

### Moderación
- `/ban @usuario razón` - Banea usuario
- `/unban @usuario razón` - Desbanea
- `/kick @usuario razón` - Expulsa
- `/mute @usuario 60 razón` - Silencia (minutos)
- `/unmute @usuario` - Dessilencia
- `/warn @usuario razón` - Advierte
- `/warnings @usuario` - Ver advertencias
- `/clear 10` - Limpia mensajes
- `/slowmode 5` - Modo lento (segundos)
- `/lock` - Cierra canal
- `/unlock` - Abre canal
- `/nick @usuario NuevoNick` - Cambia apodo

### Permisos
- `/setmodrole @rol` - Agrega rol de mod
- `/removemodrole @rol` - Quita rol
- `/modroles` - Lista roles

### Configuración
- `/setwelcome #canal` - Canal de bienvenida
- `/welcomemessage Hola {username}` - Mensaje
- `/setdmmessage Bienvenido {username}` - DM privado
- `/welcomeinfo` - Ver configuración

### Utilidad
- `/announce #canal título|descripción` - Anuncio
- `/embed #canal título|descripción` - Embed
- `/say #canal mensaje` - Mensaje

## 📊 Estructura

```
Nexa-Python/
├── cogs/                  # Comandos
│   ├── moderation.py      # 12 comandos
│   ├── permissions.py     # 3 comandos
│   ├── config.py          # 4 comandos
│   ├── utility.py         # 3 comandos
│   └── events.py          # Eventos
├── database/
│   └── db.py              # SQLite
├── utils/
│   ├── embeds.py          # Embeds
│   └── validators.py      # Validaciones
├── config/
│   └── config.py          # Configuración
├── main.py                # Punto de entrada
├── requirements.txt       # Dependencias
├── .env                   # Variables
└── README.md              # Documentación
```

## 💾 Base de Datos

SQLite con 3 tablas:
- **warnings** - Historial de advertencias
- **guild_config** - Configuración por servidor
- **mod_roles** - Roles de moderación

Archivo: `data/bot.db`

## 🔐 Seguridad

✅ Validaciones en cada comando
✅ Protección del owner
✅ Protección del bot
✅ Validación de jerarquía
✅ Manejo de errores

## 🎨 Personalización

Edita `config/config.py`:
```python
COLORS = {
    'PRIMARY': 0x00BFFF,      # Tu color azul
    'SECONDARY': 0x8A2BE2,    # Tu color morado
    'SUCCESS': 0x00FF00,
    'ERROR': 0xFF0000,
    'WARNING': 0xFFA500,
}
```

## 🆘 Troubleshooting

### "Token not valid"
- Verifica que DISCORD_TOKEN en Railway o en .env es correcto
- Copia nuevamente desde Discord Developer Portal

### "No module named discord"
```bash
pip install discord.py
```

### "DATABASE ERROR"
- La BD se crea automáticamente en `data/bot.db`
- Si hay error, elimina la carpeta `data` y reinicia

### "Permisos insuficientes"
- El bot necesita permisos en el servidor
- Invítalo con permisos de administrador

## 📞 Soporte

Este bot está completamente funcional. Para problemas:
1. Verifica el .env está correcto
2. Revisa los logs en consola
3. Asegúrate que el bot tiene permisos

## 📄 Licencia

MIT - Libre para usar y modificar

---

**Versión**: 1.0.0  
**Desarrollado por**: AxioLabs  
**Estado**: ✅ Producción
