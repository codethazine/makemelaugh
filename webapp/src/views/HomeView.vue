<template>
  <div class="home">
    <div class="brand-container">
      <img class="logo-home" alt="logo" src="../assets/logo.png">
      <h2 class="text">Try not to laugh</h2>
    </div>
    <div class="text-container">
    </div>
    <div class="cta-container">
      <router-link to="/game">
        <button class="btn-8bit">Start the battle</button>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.home {
  height: 100vh;
  background-image: url('../assets/home-bg.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center bottom;
  background-color: #9437B7;
  display: flex;
  flex-direction: column;
}

.brand-container {
  height: 35%;
  width: 100%;
  padding-top: 60px;
}

.logo-home {
  width: 80%;
  max-width: 40vh;
  display: inline-block;
  object-fit: contain
}

.text {
  font-family: 'VT323', monospace;
  color: white;
  font-size: 30px;
  /* Add shadow to text */
  text-shadow: 2px 2px 0 #000;
}

@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

.cta-container {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  margin-bottom: 60px;
}

.btn-8bit {
  font-family: 'VT323', monospace;
  font-size: 30px;
  color: #fff;
  background-color: #32CD32;
  border: 3px solid #228B22;
  border-radius: 0;
  padding: 10px 50px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  margin: 4px 2px;
  cursor: pointer;
  -webkit-transition-duration: 0.2s;
  transition-duration: 0.2s;
  text-shadow: 0 0 3px #000;
  box-shadow: 0 9px #006400;
}

.btn-8bit:hover {
  background-color: #2E8B57;
  /* Slightly different green on hover */
  color: white;
  box-shadow: 0 5px #006400;
  transform: translateY(4px);
}
</style>
