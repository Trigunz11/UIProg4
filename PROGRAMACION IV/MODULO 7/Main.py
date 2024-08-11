import budget_manager

def display_menu():
    print("1. Crear un nuevo artículo")
    print("2. Mostrar todos los artículos")
    print("3. Editar un artículo")
    print("4. Eliminar un artículo")
    print("5. Salir")

def main():
    while True:
        display_menu()
        choice = input("Selecciona una opción: ")

        if choice == "1":
            description = input("Descripción del artículo: ")
            amount = float(input("Monto del artículo: "))
            item = budget_manager.create_item(description, amount)
            print(f"Artículo creado: {item}")
        
        elif choice == "2":
            items = budget_manager.read_items()
            if items:
                for item in items:
                    print(f"ID: {item['id']}, Descripción: {item['description']}, Monto: {item['amount']}")
            else:
                print("No hay artículos registrados.")
        
        elif choice == "3":
            item_id = int(input("ID del artículo a editar: "))
            description = input("Nueva descripción (dejar en blanco para no cambiar): ")
            amount = input("Nuevo monto (dejar en blanco para no cambiar): ")
            amount = float(amount) if amount else None
            updated_item = budget_manager.update_item(item_id, description, amount)
            if updated_item:
                print(f"Artículo actualizado: {updated_item}")
            else:
                print("Artículo no encontrado.")
        
        elif choice == "4":
            item_id = int(input("ID del artículo a eliminar: "))
            updated_data = budget_manager.delete_item(item_id)
            print(f"Artículo eliminado. Artículos restantes: {updated_data}")
        
        elif choice == "5":
            print("Saliendo de la aplicación.")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()


