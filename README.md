# 🎓 Profe Números - Tutor de Matemáticas para Niños

Aplicación web para practicar operaciones matemáticas básicas (+, -, ×, ÷) para niños de 6-11 años.

## 📋 Características

- ✨ Interfaz amigable para niños
- 🎯 3 niveles de dificultad (Grados 1-2, 2-3, 4-5)
- 📊 Seguimiento de estadísticas (correctas, total, racha)
- 💾 Conexión opcional a Supabase para guardar progreso
- 🇪🇸 Completamente en español

## 🚀 Instalación Local

### Prerrequisitos
- Python 3.11+
- Git

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/TU_USUARIO/profe-numeros.git
cd profe-numeros
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno (opcional)**
Crea un archivo `.env`:
```
SUPABASE_URL=https://mcstlsbzhzrmsktawblw.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1jc3Rsc2J6aHpybXNrdGF3Ymx3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIzMzk5OTAsImV4cCI6MjA3NzkxNTk5MH0.5a0AflusOiYhHSXBpap3bwOdqQUwH1m88uixRMZi-sU
```

5. **Ejecutar la aplicación**
```bash
python app.py
```

Abre tu navegador en `http://localhost:5000`

## 📦 Configurar Supabase (Opcional)

1. Crea una cuenta en [supabase.com](https://supabase.com)
2. Crea un nuevo proyecto
3. En el SQL Editor, ejecuta:

```sql
-- Tabla para problemas generados
CREATE TABLE problemas (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  grade_band TEXT,
  problema JSONB,
  hint TEXT
);

-- Tabla para respuestas de estudiantes
CREATE TABLE respuestas (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  problema JSONB,
  respuesta_usuario INTEGER,
  respuesta_correcta INTEGER,
  es_correcta BOOLEAN
);

-- Habilitar Row Level Security
ALTER TABLE problemas ENABLE ROW LEVEL SECURITY;
ALTER TABLE respuestas ENABLE ROW LEVEL SECURITY;

-- Política para permitir inserciones
CREATE POLICY "Permitir insertar problemas" ON problemas
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Permitir insertar respuestas" ON respuestas
  FOR INSERT WITH CHECK (true);
```

4. Obtén tu URL y API Key desde Settings → API
5. Agrégalas a tu archivo `.env`

## 🌐 Desplegar en Netlify

### Método 1: Desde GitHub (Recomendado)

1. **Subir código a GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/profe-numeros.git
git push -u origin main
```

2. **Conectar con Netlify**
   - Ve a [netlify.com](https://netlify.com) y crea una cuenta
   - Click en "Add new site" → "Import an existing project"
   - Conecta tu repositorio de GitHub
   - Netlify detectará automáticamente la configuración desde `netlify.toml`

3. **Configurar variables de entorno**
   - En tu sitio de Netlify: Site settings → Environment variables
   - Agrega:
     - `SUPABASE_URL`: tu URL de Supabase
     - `SUPABASE_KEY`: tu key de Supabase

4. **Desplegar**
   - Click en "Deploy site"
   - Tu app estará disponible en `https://tu-sitio.netlify.app`

### Método 2: Netlify CLI

```bash
npm install -g netlify-cli
netlify login
netlify init
netlify deploy --prod
```

## 📁 Estructura del Proyecto

```
profe-numeros/
├── app.py                    # Aplicación Flask principal
├── requirements.txt          # Dependencias Python
├── runtime.txt              # Versión de Python
├── netlify.toml             # Configuración de Netlify
├── README.md                # Esta guía
├── templates/
│   └── index.html           # Interfaz web
└── netlify/
    └── functions/
        └── app.py           # Función serverless para Netlify
```

## 🎮 Uso de la Aplicación

1. **Selecciona el nivel**: Elige entre Grados 1-2, 2-3 o 4-5
2. **Lee el problema**: Se mostrará una operación matemática
3. **Lee la pista**: Cada problema incluye una ayuda
4. **Escribe tu respuesta**: Ingresa el número en el campo
5. **Comprueba**: Presiona el botón o Enter
6. **Aprende**: Si te equivocas, verás una explicación

## 🔧 Solución de Problemas

### Error: "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### Error: "Port already in use"
```bash
# Cambiar puerto en app.py línea final:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Netlify: Build failed
- Verifica que `runtime.txt` tenga una versión válida de Python
- Revisa los logs en el dashboard de Netlify
- Asegúrate de que `netlify.toml` esté en la raíz

## 📝 Licencia

MIT License - Libre para uso educativo

## 👨‍💻 Autor

Creado con ❤️ para ayudar a los niños a aprender matemáticas

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📧 Soporte

Si tienes preguntas o problemas, abre un issue en GitHub.

---

¡Disfruta enseñando matemáticas! 🎓✨
