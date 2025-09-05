from BeautyAngels.models.user_service import encriptar_contraseña, verificar_contraseña, verificar_contraseña_escrito, verificar_email


password = encriptar_contraseña("mi_contraseña_secreta")
print(f"Contraseña encriptada: {password}")

password_verificada = verificar_contraseña("mi_contraseña_secreta", password)
print(f"Contraseña verificada: {password_verificada}")

print(verificar_contraseña_escrito("Password123!"))  # True
print(verificar_contraseña_escrito("pass"))          # False

print(verificar_email("santisbb2004@gmail.com"))#True
print(verificar_email("email_invalido@com"))# False
print(verificar_email("santiago@uqvirtual.edu.co"))# Dude