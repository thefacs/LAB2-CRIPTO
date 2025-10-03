# LAB2-CRIPTO

aboratorio 2 - Ataques de Fuerza Bruta en DVWA
Descripción

Este proyecto documenta un análisis de seguridad realizado sobre la aplicación web vulnerable DVWA (Damn Vulnerable Web App), enfocado en ataques de fuerza bruta al formulario de autenticación. El laboratorio incluye el despliegue del entorno, ejecución de ataques con diversas herramientas y análisis comparativo de resultados.

🛠️ Herramientas Utilizadas

DVWA - Aplicación web vulnerable para pruebas

Docker - Contenerización de la aplicación

Burp Suite - Interceptación y análisis de tráfico HTTP

Hydra - Herramienta de fuerza bruta

cURL - Cliente HTTP para línea de comandos

Python - Script personalizado de fuerza bruta

📋 Actividades Realizadas

Despliegue de DVWA con Docker

Configuración de contenedores Docker para la aplicación

Redirección de puertos (4280:80)

Verificación del funcionamiento

Ataque con Burp Suite

Interceptación de tráfico HTTP

Configuración de Intruder para fuerza bruta

Identificación de campos vulnerables (username/password)

Obtención de credenciales válidas

Análisis con cURL

Replicación de peticiones HTTP desde terminal

Comparación de respuestas válidas vs inválidas

Identificación de diferencias en contenido y cabeceras

Ataque con Hydra

Configuración de parámetros de ataque

Uso de diccionarios personalizados

Automatización del proceso de fuerza bruta

Script Personalizado en Python

Desarrollo de herramienta propia usando librería requests

Implementación de concurrencia para mejor rendimiento

Detección automática de credenciales válidas

🔍 Resultados Obtenidos

Credenciales Encontradas

admin:password

pablo:letmein

1337:charley

gordonb:abc123


Comparativa de Rendimiento

Herramienta	Tiempo Ejecución (1,932 combinaciones)
Burp Suite	~12-13 horas
Hydra	~30 segundos
Python Script	~2.4 segundos

📊 Diferencias Detectadas en Respuestas

Acceso Válido vs Inválido

Mensaje de bienvenida vs mensaje de error

Presencia de imagen de perfil en respuestas válidas

Content-Length diferente (4740 vs 4702 bytes)

Nombre de usuario aparece en HTML de respuestas válidas

🛡️ Métodos de Mitigación Investigados

Limitación de intentos de login - Bloqueo temporal tras múltiples fallos

Implementación de CAPTCHA - Diferenciación humano/bot

Bloqueo por IP/geolocalización - Restricción de acceso sospechoso

Autenticación Multifactor (MFA) - Capa adicional de seguridad
