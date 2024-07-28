# Prácticas de Seguridad Implementadas

A continuación algunas prácticas de seguridad aplicadas en el desarrollo de la solución:

## Cifrado de Datos Sensibles

Estándar Aplicado: PCI DSS (Payment Card Industry Data Security Standard), NIST (National Institute of Standards and Technology).

**Descripción:**

- **PCI DSS**: Requiere que los datos del titular de la tarjeta, como el número de tarjeta de crédito, se cifren en reposo.
- **NIST**: Requiere que los datos sensibles se protejan mediante cifrado tanto en tránsito como en reposo.

**Implementación en el Código:**

- Se usó la biblioteca cryptography para cifrar datos sensibles antes de almacenarlos en la base de datos.
- Ejemplo:

    ```python
    from cryptography.fernet import Fernet

    # Generar una clave para el cifrado (almacenar esta clave de manera segura)
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    # Cifrar datos sensibles
    def encrypt_data(data):
        return cipher_suite.encrypt(data.encode())
    ```

## Cifrado en Reposo

Estándar Aplicado: PCI DSS

**Descripción:**

- **PCI DSS**: Requiere que los datos del titular de la tarjeta se cifren en reposo.

    En este caso los datos están siendo encriptados en reposo gracias a AWS RDS + KMS CMK.

## Validación y Sanitización de Entradas

Estándar Aplicado: NIST, OWASP (Open Web Application Security Project)

**Descripción:**

- **NIST**: Recomienda validar y sanitizar todas las entradas para evitar ataques de inyección y otras vulnerabilidades.
- **OWASP**: Proporciona directrices para la validación de entradas para protegerse contra vulnerabilidades comunes como la inyección SQL.

**Implementación en el Código:**

- Se valida y se convierten las fechas recibidas de la API para asegurarnos de que sean correctas y seguras antes de almacenarlas en la base de datos.
- Ejemplo:
    ```python
    def convert_datetime_format(date_str):
    try:
        dt = parser.parse(date_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ParserError, ValueError) as e:
        print(f"Error parsing date: {date_str} - {e}")
        return None
    ```

## Resumen
El código de esta solución aplica varios estándares de seguridad para proteger los datos sensibles:

1. Cifrado de Datos Sensibles: Utilizamos cryptography para cifrar datos sensibles, cumpliendo con PCI DSS y NIST.
2. Cifrado en Reposo: Se habilitó desde AWS RDS haciendo uso de una CMK.
3. Validación y Sanitización de Entradas: Validamos y sanitizamos las entradas para protegernos contra vulnerabilidades, cumpliendo con NIST y OWASP.
