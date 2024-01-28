<template>
  <!--<app-header />-->
  <div>
    <home-screen v-if="appState === 'idle'" :join-call="joinCall" />
    <div class="flex-center" v-else-if="appState === 'incall'">
      <call-controls 
        style="position: absolute; z-index: 100; top: 50%; left: 50%; transform: translate(-50%, -50%);"
        :handle-video-click="handleVideoClick"
        :handle-audio-click="handleAudioClick"
        :handle-screenshare-click="handleScreenshareClick"
        :participant="participant"
        :leave-call="leaveCall"
        :disable-screen-share="disableScreenShare"
      />
      <call-tile
        :leave-call="leaveCall"
        :name="name"
        :room-url="roomUrl"
      />
    </div>
  </div>
</template>

<script>
import CallTile from "./CallTile.vue";
import AppHeader from "./AppHeader.vue";
import HomeScreen from "./HomeScreen.vue";
import CallControls from "./CallControls.vue";

export default {
  name: "App",
  components: {
    CallTile,
    AppHeader,
    HomeScreen,
    CallControls,
  },
  mounted() {
    // Ensures audio plays on load in browsers that require user interaction
    const audio = document.getElementById("background-audio");
    audio.play().catch(() => {
      // Handle any errors trying to start playback
    });
  },
  data() {
    return {
      appState: "idle",
      name: "Guest",
      roomUrl: null,
    };
  },
  methods: {
    /**
     * Set name and URL values entered in Home.vue form in data obj
     */
    joinCall(name, url) {
      this.name = name;
      this.roomUrl = url;
      this.appState = "incall";
    },
    // Reset app state to return to the home screen after leaving call
    leaveCall() {
      this.appState = "idle";
    },
  },
};
</script>

<style>
#app {
  font-family: Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
  background-color: #9437B7;
}
a {
  text-decoration: none;
  color: #2c3e50;
  display: flex;
  align-items: center;
}
body {
  margin: 0;
}
html {
  height: 100vh;
  background-color: #9437B7;
}

/* if not on mobile */
@media screen and (min-width: 800px) {
  #app {
    height: 100vh;
  }
}
</style>
