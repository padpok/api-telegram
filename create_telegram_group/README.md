# Creación de Strings de Sesión y Grupos en Telegram

Este proyecto permite crear grupos de Telegram de manera automática utilizando la librería **Telethon**.

---

## 1. Configurar el entorno virtual e instalar dependencias

Este proyecto incluye un archivo `requirements.txt` con las librerías necesarias para su ejecución.

### **Paso 1: Crear un entorno virtual**
Ejecutar el siguiente comando para crear un entorno virtual en Python:

```bash
python3 -m venv nombre_del_entorno
```

### **Paso 2: Activar el entorno virtual**
- En **Linux/macOS**:
  ```bash
  source nombre_del_entorno/bin/activate
  ```
- En **Windows**:
  ```bash
  nombre_del_entorno\Scripts\activate
  ```

### **Paso 3: Instalar las dependencias**
Ejecutar el siguiente comando para instalar los paquetes desde `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 2. Crear el String de Sesión

Antes de poder lanzar el servidor para crear grupos, es necesario generar un **String de sesión**.

### **Paso 1: Definir las constantes en `constants.py`**
En el archivo `constants.py`, definir las siguientes variables:

```python
TELEGRAM_API_ID = "TU_API_ID"
TELEGRAM_API_HASH = "TU_API_HASH"
TELEGRAM_SESSION_FILE = "session.txt"  # Nombre del archivo donde se guardará la sesión
```

### **Paso 2: Ejecutar `generate_session.py`**
Ejecutar el siguiente comando para generar el String de sesión:

```bash
python3 generate_session.py
```

Este script pedirá el número de teléfono y el código de verificación de Telegram para autenticar la sesión.

---

## 3. Lanzar el servidor para crear grupos

Una vez generado el **String de sesión**, se puede iniciar el servidor encargado de crear grupos en Telegram.

### **Paso 1: Definir las constantes en `constants.py`**
Asegurarse de que `constants.py` contiene los siguientes valores:

```python
TELEGRAM_API_ID = "TU_API_ID"
TELEGRAM_API_HASH = "TU_API_HASH"
TELEGRAM_SESSION_FILE = "session.txt"  # Archivo con el String de sesión generado
```

### **Paso 2: Ejecutar el servidor**
Ejecutar el siguiente comando para iniciar el servidor:

```bash
python3 create_groups.py
```

Esto iniciará un servidor basado en **Quart** que escucha peticiones para crear grupos.

---

## 4. Probar la creación de un grupo

Para probar la funcionalidad, se puede enviar una petición `POST` al servidor:

```bash
curl -X POST http://127.0.0.1:5000/create_group \  
     -H "Content-Type: application/json" \  
     -d '{"group_name": "Padpok group test"}'
```

Si todo funciona correctamente, la respuesta incluirá el **ID del grupo** y un **enlace de invitación**.

---

## Notas
- Asegurarse de que el **archivo de sesión** generado (`session.txt`) se encuentra en la misma carpeta que `create_groups.py`.
- Es recomendable ejecutar el servidor dentro del **entorno virtual** para evitar conflictos con otras versiones de paquetes instalados en el sistema.

