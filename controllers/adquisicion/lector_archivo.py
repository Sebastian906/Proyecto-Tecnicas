import csv
import json
import os
from models.libro import Libro

class LectorArchivo:
    """
    Clase encargada de cargar los datos de los libros desde un .csv o un .json
    """

    @staticmethod
    def cargar_csv(ruta_archivo: str):
        """
        Método para cargar libros desde un archivo CSV.

        El archivo CSV debe tener los mismos atributos que la clase libro.py

        Args:
            ruta_archivo (str): Ruta del archivo CSV a cargar.

        Returns:
            list: Lista de objetos Libro cargados desde el archivo CSV.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si el formato del archivo no coincide.
        """
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")
        
        libros = []

        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)

            for linea_num, fila in enumerate(lector, start=2):
                try:
                    libro = Libro(
                        isbn=fila['isbn'].strip(),
                        titulo=fila['titulo'].strip(),
                        autor=fila['autor'].strip(),
                        peso=float(fila['peso']),
                        valor=float(fila['valor']),
                        genero=fila['genero'].strip(),
                        cantidad_disponible=int(fila.get('cantidad_disponible', 1)),
                        cantidad_total=int(fila.get('cantidad_total', 1))
                    )
                    libros.append(libro)

                except KeyError as e:
                    raise ValueError(f"Columna faltante en línea {linea_num}: {e}"
                    )
                except ValueError as e:
                    raise ValueError(f"Error en línea {linea_num}: {e}"
                    )
        print(f"Se cargaron {len(libros)} libros desde {ruta_archivo}")
        return libros
    
    @staticmethod
    def cargar_json(ruta_archivo: str):
        """
        Método para cargar libros desde un archivo JSON.

        El archivo JSON debe tener los mismos atributos que la clase libro.py

        Args:
            ruta_archivo (str): Ruta del archivo JSON a cargar.

        Returns:
            list: Lista de objetos Libro cargados desde el archivo JSON.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si el formato del archivo no coincide.
        """
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"El archivo {ruta_archivo} no existe")
        
        libros = []

        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

            if not isinstance(datos, list):
                raise ValueError("El archivo JSON debe contener un arreglo de libros")
            
            for idx, item in enumerate(datos):
                try:
                    libro = Libro(
                        isbn=item['isbn'],
                        titulo=item['titulo'],
                        autor=item['autor'],
                        peso=float(item['peso']),
                        valor=float(item['valor']),
                        genero=item['genero'],
                        cantidad_disponible=int(item.get('cantidad_disponible', 1)),
                        cantidad_total=int(item.get('cantidad_total', 1))
                    )
                    libros.append(libro)

                except KeyError as e:
                    raise ValueError(f"Falta una propiedad en {idx}: {e}")
                except ValueError as e:
                    raise ValueError(f"Error en el elemento {idx}: {e}")
        print(f"Se cargaron {len(libros)} libros desde {ruta_archivo}")
        return libros
    
    @staticmethod
    def cargar_libros(ruta_archivo: str):
        """
        Método para detectar automáticamente el formato del archivo.

        Detecta el tipo del archivo por su extensión y llama al método correspondiente.

        Args:
            ruta_archivo (str): Ruta del archivo a cargar.

        Returns:
            list: Lista de objetos Libro cargados desde el archivo.

        Raises:
            ValueError: Si el formato del archivo no es soportado.
        """
        extension = os.path.splitext(ruta_archivo)[1].lower()
        if extension == '.csv':
            return LectorArchivo.cargar_csv(ruta_archivo)
        elif extension == '.json':
            return LectorArchivo.cargar_json(ruta_archivo)
        else:
            raise ValueError(
                f"Formato de archivo no soportado: {extension}. "
                "Solo se soportan .csv y .json"
            )
        
    @staticmethod
    def guardar_csv(libros: list, ruta_archivo: str):
        """
        Guarda una lista de libros en formato CSV.

        Args:
            libros (list): Lista de objetos libro a guardar.
            ruta_archivo (str): Ruta donde guardar el archivo CSV.
        """
        with open(ruta_archivo, 'w', encoding='utf-8', newline='') as archivo:
            campos = [
                'isbn', 'titulo', 'autor', 'peso', 
                'valor', 'genero', 'cantidad_disponible', 'cantidad_total', 'estante_id'
            ]
            escritor = csv.DictWriter(archivo, fieldnames=campos)

            escritor.writeheader()
            for libro in libros:
                escritor.writerow({
                    'isbn': libro.isbn,
                    'titulo': libro.titulo,
                    'autor': libro.autor,
                    'peso': libro.peso,
                    'valor': libro.valor,
                    'genero': libro.genero,
                    'cantidad_disponible': libro.cantidad_disponible,
                    'cantidad_total': libro.cantidad_total,
                    'estante_id': libro.estante_id
                })
        print(f"Se guardaron {len(libros)} libros en {ruta_archivo}")

    @staticmethod
    def guardar_json(libros: list, ruta_archivo: str):
        """
        Guarda una lista de libros en formato JSON.

        Args:
            libros (list): Lista de objetos libro a guardar.
            ruta_archivo (str): Ruta donde guardar el archivo JSON.
        """
        datos = []
        for libro in libros:
            datos.append({
                'isbn': libro.isbn,
                'titulo': libro.titulo,
                'autor': libro.autor,
                'peso': libro.peso,
                'valor': libro.valor,
                'genero': libro.genero,
                'cantidad_disponible': libro.cantidad_disponible,
                'cantidad_total': libro.cantidad_total,
                'estante_id': libro.estante_id
            })
        
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
        print(f"Se guardaron {len(libros)} libros en {ruta_archivo}")