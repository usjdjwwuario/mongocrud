let productos = []
let categorias = []
let mensajesValidarDatos = null
let base64URL = null


function login() {
    const usuario = document.getElementById('correo');
    const password = document.getElementById('contraseña');
    if (!usuario.value || !password.value) {
        swal.fire('Iniciar sesión', 'Por favor, complete todos los campos', 'warning');
        return;     }
    const user = {
        usuario: correo.value,
        password: contraseña.value
    };
    const url = '/'; 
    fetch(url, {
        method: 'POST',
        body: JSON.stringify(user),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(respuesta => {
        if (!respuesta.ok) {
            throw new Error('Error en la solicitud');
        }
        return respuesta.json();
    })
    .then(result => {
        console.log(result);
        if (result.estado) {
            location.href = '/listaProductos';
        } else {
            swal.fire('Iniciar sesión', result.mensaje, 'warning');
        }
    })
    .catch(error => {
        console.error('Error:', error.message);
        swal.fire('Iniciar sesión', 'Se produjo un error al intentar iniciar sesión', 'error');
    });
}


// async function visualizarFoto(evento) {
//     const files = evento.target.files;
//     const archivo = files[0];
//     let filename = archivo.name;
//     let extension = filename.split(".").pop();
//     extension = extension.tolowerCase();
//     if (extension !== "jpg") {
//       evento.target.value = "";
//       swal.fire("Seleccionar", "La imagen debe ser en formato JPG", "warning");
//     } else {
//       const objectURL = URL.createObjectURL(archivo);
//       imagenProducto.setAttribute("src", objectURL);
//     }
//   }