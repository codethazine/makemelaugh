<template>
  <main class="home">
    <div class="brand-container">
      <img class="logo-home" alt="logo" src="../assets/logo.png">
      <h2 class="text">Try not to laugh</h2>
    </div>
    <img style="height: 35%; object-fit: contain;" src="../assets/cat.png">
    <div class="text-container">
    </div>
    <div class="cta-container">
      <form class="join-form" @submit="joinWithName">
        <div class="name-container">
          <!--
          <label for="name">Your name</label>
          <input id="name" v-model="name" type="text" required />
          <label for="name">Daily URL</label>
          <input
            id="url"
            v-model="url"
            type="text"
            placeholder="https://your-daily-domain.daily.co/room-name"
            required
          />
          -->
        </div>
        <button class="btn-8bit">Start the battle</button>
      </form>
    </div>
  </main>
</template>
<script>
export default {
  name: "HomeScreen",
  props: {
    joinCall: {
      type: Function,
      required: true,
    },
  },
  data() {
    return {
      name: "X",
      url: "https://makemelaugh.daily.co/" + process.env.VUE_APP_ROOM_ID || 'O8EvAKGhOPHpYuqfBHog';
    };
  },
  methods: {
    // Submit form with prop method defined in App.vue
    joinWithName() {
      this.joinCall(this.name, this.url);
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

.home {
  height: 100vh;
  background-image: url('../assets/bg-home-new.png');
  background-size: cover;
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
  font-size: 200%;
  /* Add shadow to text */
  text-shadow: 2px 2px 0 #000;
}

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
  border-radius: 5px;
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
