# PROYECTO-FINAL-

# Manzana Loca 
Manzana Loca es un sistema de gestión para una tienda desarrollado en Python utilizando Programación Orientada a Objetos (POO), Tkinter para la interfaz gráfica y SQLite para la base de datos.

El sistema fue creado con el objetivo de facilitar la administración de productos, usuarios, promociones y alertas dentro de una tienda mediante una interfaz sencilla y fácil de utilizar.

# Descripción general
El programa permite controlar diferentes áreas de una tienda desde un solo sistema. Toda la información se guarda automáticamente en una base de datos SQLite, permitiendo almacenar productos, usuarios y promociones de manera organizada.

La aplicación cuenta con una interfaz gráfica desarrollada con Tkinter, donde el usuario puede navegar entre los diferentes módulos del sistema.

# Inicio de sesión
El sistema cuenta con una ventana de inicio de sesión que valida el acceso de los usuarios registrados.

Existe un usuario administrador predeterminado:

Usuario: admin  
Contraseña: 1234

Cuando el usuario inicia sesión correctamente, el sistema muestra el panel principal.

# Menú principal
El menú principal contiene diferentes módulos organizados mediante tarjetas visuales.

Cada tarjeta permite acceder a una función diferente del sistema:

- Inventario
- Agregar producto
- Usuarios
- Promociones
- Alertas

La interfaz utiliza colores personalizados y botones interactivos para mejorar la experiencia visual del usuario.

# Gestión de inventario
El módulo de inventario permite visualizar todos los productos registrados dentro de la base de datos.

Dentro de este apartado se puede:

- Mostrar productos
- Buscar productos por nombre
- Ver cantidad en stock
- Ver fecha de caducidad
- Ver estado del producto
- Eliminar productos

El estado del producto cambia automáticamente dependiendo de la fecha de caducidad.

Estados disponibles:

- 🟢 Vigente
- 🟠 Por caducar
- 🔴 Caducado

La información se muestra utilizando tablas dinámicas con Treeview de Tkinter.

# Registro de productos
El sistema permite registrar nuevos productos mediante un formulario.

Cada producto almacena:

- Nombre
- Cantidad disponible
- Fecha de caducidad

Al guardar un producto, la información se almacena automáticamente en la base de datos SQLite.

El sistema también valida que algunos campos obligatorios no estén vacíos antes de registrar la información.

# Gestión de usuarios
El módulo de usuarios permite administrar las cuentas del sistema.

Funciones disponibles:

- Registrar usuarios
- Mostrar usuarios registrados

Los usuarios se almacenan en la tabla correspondiente de la base de datos.

# Promociones
El sistema incluye un apartado para administrar promociones de la tienda.

Funciones:

- Crear promociones
- Mostrar promociones activas
- Eliminar promociones

Cada promoción se almacena en la base de datos y puede visualizarse desde la interfaz gráfica.

# Sistema de alertas
El sistema genera alertas automáticas relacionadas con el inventario.

Las alertas aparecen cuando:

- El stock de un producto es bajo
- Un producto está próximo a caducar
- Un producto ya caducó

Esto permite mantener un mejor control de los productos dentro de la tienda.

# Base de datos
La aplicación utiliza SQLite como sistema de almacenamiento.

El archivo de base de datos se genera automáticamente y almacena toda la información relacionada con:

- Usuarios
- Productos
- Promociones

El sistema utiliza consultas SQL para insertar, eliminar y consultar datos.

# Programación Orientada a Objetos
El proyecto fue desarrollado utilizando Programación Orientada a Objetos.

El sistema se divide en diferentes clases, donde cada clase tiene una función específica.

Principales clases del proyecto:

## DatabaseManager
Se encarga de crear la base de datos y administrar las conexiones SQLite.

## USUARIO
Administra el registro, eliminación e inicio de sesión de usuarios.

## PRODUCTO
Administra el registro y eliminación de productos, además de verificar el estado de caducidad.

## INVENTARIO
Permite mostrar y buscar productos registrados.

## ALERTA
Genera alertas automáticas relacionadas con stock bajo y productos caducados.

## PROMOCION
Administra las promociones de la tienda.

## TarjetaModulo
Crea las tarjetas visuales utilizadas en el menú principal.

## SISTEMA
Controla toda la interfaz gráfica y el funcionamiento general del programa.

# Interfaz gráfica
La interfaz fue desarrollada utilizando Tkinter.

Se utilizaron:

- Frames
- Labels
- Buttons
- Entry
- Treeview
- MessageBox
- SimpleDialog

La interfaz está diseñada para ser sencilla, organizada y fácil de entender.

# Objetivo del proyecto
El objetivo principal del proyecto es aplicar los conocimientos de:

- Programación Orientada a Objetos
- Interfaces gráficas
- Bases de datos
- Manejo de clases y métodos
- Gestión de información

Todo esto dentro de una aplicación funcional de escritorio desarrollada en Python.
