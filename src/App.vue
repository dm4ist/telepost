<template>
  <div id="app">
    <nav>
      <router-link to="/">Dashboard</router-link> |
      <router-link to="/templates">Templates</router-link> |
      <router-link to="/posts">Posts</router-link> |
      <router-link to="/channels">Channels</router-link> |
      <router-link to="/statistics">Statistics</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
nav {
  padding: 30px;
}
nav a {
  font-weight: bold;
  color: #2c3e50;
}
nav a.router-link-exact-active {
  color: #42b983;
}
</style>