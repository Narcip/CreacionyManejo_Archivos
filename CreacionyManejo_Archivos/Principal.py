import requests
import json
import pandas as pd

class LigaDeFutbol:
    DATA_FILE = 'data_base.json'

    def __init__(self):
        self.data = self._load_or_update_data()

    def _load_or_update_data(self):
        while True:
            try:
                # Abrir el archivo 'ligas_urls.txt' que contiene nombres y URLs de ligas
                with open('ligas_urls.txt', 'r', encoding='utf-8') as archivo_txt:
                    # Leer líneas del archivo y eliminar espacios en blanco alrededor
                    lines = [line.strip() for line in archivo_txt if line.strip()]

                    # Mostrar las ligas disponibles para que el usuario seleccione
                    for index, line in enumerate(lines, start=1):
                        name, url = map(str.strip, line.split(': '))
                        print(f"{index}. {name}")

                    # Solicitar al usuario que elija una liga por su número
                    selection = int(input("\nSeleccione una liga por su número: "))
                    
                    # Verificar que la selección esté dentro del rango válido
                    if 1 <= selection <= len(lines):
                        selected = lines[selection - 1]
                        name, url = map(str.strip, selected.split(': '))
                        print(f"\nLiga seleccionada: {name}")

                        # Realizar una solicitud HTTP a la URL seleccionada y verifica si fue exitosa
                        response = requests.get(url)
                        response.raise_for_status()

                        # Obtener los datos JSON y guardarlos en el archivo 'data_base.json'
                        data = response.json()
                        with open(LigaDeFutbol.DATA_FILE, 'w', encoding='utf-8') as file:
                            json.dump(data, file, ensure_ascii=False, indent=2)
                            print("Datos cargados en data_base.json")
                        # Devuelve los datos obtenidos después de cargar o actualizar la información de la liga.
                        return data
                    else:
                        print("Número fuera de rango. Intente de nuevo.")
            except ValueError:
                print("Ingrese un número válido.")
            except FileNotFoundError as e:
                print(f"Error: {e}")
                return None

    def _load_data(self):
        try:
            # Leer los datos del archivo 'data_base.json'
            with open(self.DATA_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"El archivo '{self.DATA_FILE}' no encontrado.")
            return None

    def obtener_cantidad_equipos(self):
        data = self._load_data()
        if data:
            # Verificar que los datos sean un diccionario y contengan la clave "clubs"
            if isinstance(data, dict) and "clubs" in data:
                teams = data["clubs"]
                num_teams = len(teams)
                print(f"\nNúmero de equipos: {num_teams} Equipos.")
            else:
                print("El archivo JSON no tiene el formato esperado.")

    def _create_dataframe(self):
        data = self._load_data()
        if data and isinstance(data, dict) and "clubs" in data:
            teams = data["clubs"]
            # Crear un DataFrame de Pandas con los datos de los equipos
            df = pd.DataFrame(teams, columns=["name", "code"]).fillna('')
            df.index = df.index + 1
            return df
        return None

    def obtener_nombres_y_codigos(self):
        df = self._create_dataframe()
        if df is not None:
            # Mostrar el DataFrame con nombres y códigos de los equipos
            print(df.to_string(col_space=0, justify='center'))
        else:
            print("El archivo está mal leído.")

    def crear_txt(self):
        data = self._load_data()
        if data and isinstance(data, dict) and "clubs" in data:
            teams = data["clubs"]
            # Crear un archivo de texto con información sobre la liga y los equipos
            file_name = data.get("name", "informacion").replace("/", "_").replace(' ','') + ".txt"
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(f"Nombre de la Liga: {data.get('name', 'N/A')}\n\n")
                for team in teams:
                    name = team.get("name", "N/A")
                    code = team.get("code", "N/A")
                    city = team.get("country", "N/A")
                    file.write(f"Equipo: {name}\nCódigo: {code}\nCiudad: {city}\n\n")
                print(f"Información guardada en {file_name}")
        else:
            print("El archivo 'data_base.json' no encontrado.")

# Menú principal
def main():
    while True:
        print("\n--- Menú ---")
        print("1. Crear Liga")  # Opción para cargar datos de una nueva liga
        print("2. Salir")       # Opción para salir del programa

        try:
            # Solicitar al usuario que ingrese un número para seleccionar una opción del menú
            option = int(input("Seleccione una opción: "))
        except ValueError:
            # Manejar la excepción en caso de que el usuario no ingrese un número válido
            print("Ingrese un número válido.")
            continue

        if option == 1:
            # Si la opción seleccionada es 1, crear una nueva instancia de la clase LigaDeFutbol
            new_league = LigaDeFutbol()
            while True:
                print("\n--- Menú ---")
                print("1. Contar Equipos")            
                print("2. Equipos que Participan")    
                print("3. Crear Txt")                 
                print("4. Salir")                     

                try:
                    # Solicitar al usuario que ingrese un número para seleccionar una opción del submenú
                    option = int(input("Seleccione una opción: "))
                except ValueError:
                    # Manejar la excepción en caso de que el usuario no ingrese un número válido
                    print("Ingrese un número válido.")
                    continue

                if option == 1:
                    new_league.obtener_cantidad_equipos()
                elif option == 2:
                    new_league.obtener_nombres_y_codigos()
                elif option == 3:
                    new_league.crear_txt()
                elif option == 4:
                    break
                else:
                    print("Ingresa un índice válido.")
        elif option == 2:
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
