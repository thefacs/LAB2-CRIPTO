# LAB2-CRIPTO — Laboratorio 2: Ataques de Fuerza Bruta en DVWA

## 📘 Descripción
Este proyecto documenta un análisis de seguridad realizado sobre la aplicación web vulnerable **DVWA (Damn Vulnerable Web App)**, enfocado en ataques de fuerza bruta al formulario de autenticación. El laboratorio incluye el despliegue del entorno, ejecución de ataques con diversas herramientas y un análisis comparativo de resultados.

---

## 🛠️ Herramientas utilizadas
- **DVWA** — Aplicación web vulnerable para pruebas  
- **Docker / Docker Compose** — Contenerización de la aplicación  
- **Burp Suite** — Interceptación y análisis de tráfico HTTP  
- **Hydra** — Herramienta de fuerza bruta  
- **cURL** — Cliente HTTP desde la línea de comandos  
- **Python** — Script personalizado de fuerza bruta (requests, concurrencia)

---

## 📋 Actividades realizadas

### 1. Despliegue de DVWA con Docker
- Configuración de contenedores Docker para la aplicación.  
- Redirección de puertos (`4280:80`).  
- Verificación del funcionamiento.

### 2. Ataque con Burp Suite
- Interceptación de tráfico HTTP.  
- Configuración de **Intruder** para fuerza bruta.  
- Identificación de campos vulnerables (`username` / `password`).  
- Obtención de credenciales válidas.

### 3. Análisis con cURL
- Replicación de peticiones HTTP desde terminal.  
- Comparación de respuestas válidas vs inválidas.  
- Identificación de diferencias en contenido y cabeceras.

### 4. Ataque con Hydra
- Configuración de parámetros de ataque.  
- Uso de diccionarios personalizados.  
- Automatización del proceso de fuerza bruta.

### 5. Script personalizado en Python
- Desarrollo de herramienta propia usando la librería `requests`.  
- Implementación de concurrencia para mejor rendimiento.  
- Detección automática de credenciales válidas y guardado de resultados.

---

## 🔍 Resultados obtenidos

### Credenciales encontradas
