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
  width: 70vh; /* Width relative to the viewport height */
  height: 100vh; /* Full viewport height */
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.webcam-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

#webcam1, #webcam2 {
  width: 100%;
  height: 50%;
  object-fit: cover;
}

/* Ensures the body takes full height of the viewport */
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  display: flex; /* Enables flexbox layout */
  justify-content: center; /* Centers content horizontally */
  align-items: center; /* Centers content vertically */
}

@media screen and (max-width: 768px) {
  .game {
    width: 100%; /* Full width on smaller screens */
  }

  body, html {
    display: block;
  }
}
</style>
