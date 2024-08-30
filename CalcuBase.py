from sumar import sumar;
from resta import restar;
from dividir import dividir;
from multiplicar import multiplicar;


def calculadora():
    print("Bienvenido a la calculadora básica.")
    
    while True:
        # Solicitar los dos números al usuario
        num1 = float(input("\nIngrese el primer número: "))
        num2 = float(input("Ingrese el segundo número: "))
        
        # Mostrar el menú de operaciones
        print("\nSeleccione la operación que desea realizar:")
        print("1. Sumar")
        print("2. Restar")
        print("3. Multiplicar")
        print("4. Dividir")
        print("5. Salir")
        
        # Solicitar la operación al usuario
        opcion = input("\nIngrese el número de la operación (1/2/3/4/5): ")
        
        # Realizar la operación seleccionada
        if opcion == '1':
            print(f"\nEl resultado de sumar {num1} y {num2} es: {sumar(num1, num2)}")
        elif opcion == '2':
            print(f"\nEl resultado de restar {num1} y {num2} es: {restar(num1, num2)}")
        elif opcion == '3':
            print(f"\nEl resultado de multiplicar {num1} y {num2} es: {multiplicar(num1, num2)}")
        elif opcion == '4':
            print(f"\nEl resultado de dividir {num1} entre {num2} es: {dividir(num1, num2)}")
        elif opcion == '5':
            print("\nGracias por usar la calculadora. ¡Adiós!")
            break
        else:
            print("\nOpción no válida. Por favor, seleccione una operación válida.")

# Ejecutar la calculadora
calculadora()