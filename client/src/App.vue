<template>
  <div>
    <header>
      <img src="./assets/header.png" class="img-fluid mx-auto d-block" alt="Header">
    </header>
    <router-view/>
  </div>
</template>

<style scoped>
header img {
  padding-top: 10px;
  padding-bottom: 10px;
  border-radius: 20px;
}
header {
  background-color: beige;
}
</style>
