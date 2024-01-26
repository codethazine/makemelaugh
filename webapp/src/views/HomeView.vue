<template>
  <div class="home">
    <img class="logo-home" alt="logo" src="../assets/logo.png">
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
  background-image: url('../assets/home-bg.png'); /* Adding background image */
  background-size: cover, contain; /* Cover the entire background */
  background-position: center; /* Centers the background image */
}

.logo-home{
  width: 40vh;
  height: auto;
  margin-bottom: 20px;
}

@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

.btn-8bit {
  font-family: 'VT323', monospace; /* VT323 font applied */
  font-size: 30px; /* Adjust font size as needed */
  color: #fff;
  background-color: #32CD32; /* Green background */
  border: 3px solid #228B22; /* Darker green border */
  border-radius: 5px;
  padding: 10px 50px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  margin: 4px 2px;
  cursor: pointer;
  -webkit-transition-duration: 0.2s; /* Safari */
  transition-duration: 0.2s;
  text-shadow: 0 0 3px #000;
  box-shadow: 0 9px #006400; /* Deep green shadow for depth */
}

.btn-8bit:hover {
  background-color: #2E8B57; /* Slightly different green on hover */
  color: white;
  box-shadow: 0 5px #006400;
  transform: translateY(4px);
}
</style>
