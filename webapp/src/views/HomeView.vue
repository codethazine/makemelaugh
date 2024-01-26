<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <router-link to="/game">
      <button class="btn-8bit">START</button>
    </router-link>
  </div>
</template>

<style scoped>
.home {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.btn-8bit {
  font-family: 'Press Start 2P'; /* This is a commonly used 8-bit style font */
  font-size: 16px;
  color: #fff;
  background-color: #333;
  border: 3px solid #555;
  border-radius: 5px;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  margin: 4px 2px;
  cursor: pointer;
  -webkit-transition-duration: 0.4s; /* Safari */
  transition-duration: 0.4s;
  text-shadow: 0 0 3px #000;
  box-shadow: 0 9px #999;
}

.btn-8bit:hover {
  background-color: #555;
  color: white;
  box-shadow: 0 5px #666;
  transform: translateY(4px);
}

@font-face {
  font-family: 'Press Start 2P';
  src: url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
}
</style>
