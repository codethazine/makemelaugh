<template>
  <div class="game">
    <div class="webcam-container">
      <!-- Assign unique IDs and refs to each webcam element -->
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
        // Assign the stream to both video elements
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
}

.webcam-container {
 position: relative;
 width: 100%;
 height: 100%;
}

#webcam1, #webcam2 {
 position: absolute;
 width: 100%;
 height: 50%;
 object-fit: cover;
 left: 0;
}

#webcam1 {
 top: 0;
}

#webcam2 {
 top: 50%;
}

.divider {
  position: absolute;
  width: 100%;
  height: 2px;
  background-color: white;
  top: 50%; /* Center the divider */
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
