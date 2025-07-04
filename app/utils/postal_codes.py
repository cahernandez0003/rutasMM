import json
import os

# Diccionario de provincias por código postal (primeros dos dígitos)
PROVINCIAS = {
    '01': 'Álava', '02': 'Albacete', '03': 'Alicante', '04': 'Almería', '05': 'Ávila',
    '06': 'Badajoz', '07': 'Islas Baleares', '08': 'Barcelona', '09': 'Burgos', '10': 'Cáceres',
    '11': 'Cádiz', '12': 'Castellón', '13': 'Ciudad Real', '14': 'Córdoba', '15': 'La Coruña',
    '16': 'Cuenca', '17': 'Gerona', '18': 'Granada', '19': 'Guadalajara', '20': 'Guipúzcoa',
    '21': 'Huelva', '22': 'Huesca', '23': 'Jaén', '24': 'León', '25': 'Lérida',
    '26': 'La Rioja', '27': 'Lugo', '28': 'Madrid', '29': 'Málaga', '30': 'Murcia',
    '31': 'Navarra', '32': 'Orense', '33': 'Asturias', '34': 'Palencia', '35': 'Las Palmas',
    '36': 'Pontevedra', '37': 'Salamanca', '38': 'Santa Cruz de Tenerife', '39': 'Cantabria',
    '40': 'Segovia', '41': 'Sevilla', '42': 'Soria', '43': 'Tarragona', '44': 'Teruel',
    '45': 'Toledo', '46': 'Valencia', '47': 'Valladolid', '48': 'Vizcaya', '49': 'Zamora',
    '50': 'Zaragoza', '51': 'Ceuta', '52': 'Melilla'
}

def get_location_info(codigo_postal):
    """
    Obtiene información de ubicación basada en el código postal.
    
    Args:
        codigo_postal (str): Código postal español (5 dígitos)
        
    Returns:
        dict: Diccionario con provincia y municipio
    """
    try:
        # Aseguramos que el código postal tenga 5 dígitos
        if not codigo_postal or len(str(codigo_postal)) != 5:
            return {'provincia': '', 'municipio': ''}
        
        # Obtenemos los dos primeros dígitos para la provincia
        provincia_code = str(codigo_postal)[:2]
        provincia = PROVINCIAS.get(provincia_code, '')
        
        # Por ahora, devolvemos solo la provincia
        # El municipio se podría implementar con una base de datos más completa
        return {
            'provincia': provincia,
            'municipio': ''  # Por ahora vacío, se podría expandir en el futuro
        }
    except Exception as e:
        print(f"Error al obtener información del código postal: {e}")
        return {'provincia': '', 'municipio': ''} 