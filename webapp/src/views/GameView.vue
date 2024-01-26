<template>
  <div class="game">
    <div class="webcam-container">
      <video id="webcam1" ref="webcam1" autoplay playsinline></video>
      <video id="webcam2" ref="webcam2" autoplay playsinline></video>
    </div>
  </div>
</template>

<script>
export default {
  mounted() {
    this.setupWebcam();
  },
  methods: {
    async setupWebcam() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        this.$refs.webcam1.srcObject = stream;
        this.$refs.webcam2.srcObject = stream;
      } catch (error) {
        console.error('Error accessing the webcam:', error);
      }
    },
  },
};
</script>

<style>
.game {
  position: relative;
  width: 30%;
  height: 100vh;
  overflow: hidden;
  display: flex; /* Use flex layout */
  justify-content: center; /* Center horizontally */
  align-items: center; /* Center vertically */
}

.webcam-container {
  display: flex; /* Enable flex layout */
  flex-direction: column; /* Stack children vertically */
  width: 100%;
  height: 100%;
}

#webcam1, #webcam2 {
  width: 100%; /* Set width to 100% of parent */
  height: 50%; /* Each webcam takes half of the container height */
  object-fit: cover;
}

/* Additional styles */
body, html {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

@media screen and (max-width: 768px){
  .game {
    width: 100%;
  }
}
</style>
