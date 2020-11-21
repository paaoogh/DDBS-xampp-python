<!DOCTYPE html>
<html>
<head>
</head>

<body>
<div allign="center">
<h1> Consulta de clientes </h1>
<form action="test.py" method=post>
<b>ID: </b>
<input type="integer" placeholder="Clave del cliente" name="id_cliente">
<b>Nombre: </b>
<input type="varchar" placeholder="Escriba el nombre:" name="nombre"><br><br>
<b>Apellido Paterno: </b>
<input type="varchar" placeholder="Apellido Paterno:" name="apellido1"><br><br>
<b>Apellido Materno: </b>
<input type="varchar" placeholder="Apellido Materno:" name="apellido2"><br><br>
<b>RFC: </b>
<input type="varchar" name="rfc"><br><br>
<b>Calle de residencia: </b>
<input type="varchar" placeholder="Escriba la calle de dirección:" name="calle"><br><br>
<b>Número exterior: </b>
<input type="varchar" placeholder="Número de residencia:" name="numero"><br><br>
<b>Colonia: </b>
<input type="varchar" placeholder="Colonia de residencia:" name="colonia"><br><br>
<b>Código postal: </b>
<input type="varchar" name="cp"><br><br>
</form>
<input type="search" value="BUSCAR">


</body>
</html>