<template>
  <div>
    <button @click="$auth.loginWith('github')">Login github</button>
    <button @click="$auth.logout()">logout</button>
  </div>
</template>
