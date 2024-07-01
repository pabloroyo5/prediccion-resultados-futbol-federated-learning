<template>
  <v-app>
    <v-app-bar color="#7C46DB">
      <v-toolbar-title>PrediccionesApp</v-toolbar-title>
    </v-app-bar>
    <v-main>
      <div class="background-img fill-height">
        <router-view></router-view>
      </div>
    </v-main>
  </v-app>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.background-img {
  background-image: url("./assets/background.png"); /* Ruta a tu imagen de fondo */
  background-size: cover; /* Ajusta el tamaño de la imagen para que cubra todo el contenedor */
  background-repeat: no-repeat; /* Evita que la imagen se repita */
  background-attachment: fixed; /* Hace que la imagen de fondo esté fija al hacer scroll */
  background-position: center; /* Centra la imagen */
  min-height: 80vh; /* Asegura que la altura mínima sea el 100% de la altura de la ventana */
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
