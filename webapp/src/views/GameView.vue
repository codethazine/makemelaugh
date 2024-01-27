<template>
  <div class="game">
    <div class="webcam-container">
      <video id="localVideo" ref="localVideo" autoplay playsinline></video>
      <video id="remoteVideo" ref="remoteVideo" autoplay playsinline></video>
    </div>
  </div>
</template>

<script>
import io from 'socket.io-client';
const socket = io('http://localhost:3000');

export default {
  data() {
    return {
      localStream: null,
      peerConnection: null,
      roomId: 'unique-room-id', // This should be dynamically generated or passed
    };
  },
  mounted() {
    this.setupWebcam();
    this.joinNextAvailableRoom();
  },
  methods: {
    async setupWebcam() {
      try {
        this.localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        this.$refs.localVideo.srcObject = this.localStream;
      } catch (error) {
        console.error('Error accessing the webcam:', error);
      }
    },
    joinNextAvailableRoom() {
      socket.emit('joinNextAvailableRoom');
      this.setupSocketListeners();
    },
    setupSocketListeners() {
      socket.on('joinedRoom', roomId => {
        this.roomId = roomId;
        this.updateUrlWithRoomId(roomId);
      });
      socket.on('signal', data => {
        if (data.type === 'offer') {
          this.handleOffer(data.offer);
        } else if (data.type === 'answer') {
          this.handleAnswer(data.answer);
        } else if (data.type === 'candidate') {
          this.handleCandidate(data.candidate);
        }
      });
    },
    updateUrlWithRoomId(roomId) {
      if (history.pushState) {
        const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?roomId=' + roomId;
        window.history.pushState({ path: newUrl }, '', newUrl);
      }
    },
    async createOffer() {
      this.peerConnection = new RTCPeerConnection();
      this.localStream.getTracks().forEach(track => {
        this.peerConnection.addTrack(track, this.localStream);
      });

      this.peerConnection.onicecandidate = event => {
        if (event.candidate) {
          socket.emit('signal', { roomId: this.roomId, type: 'candidate', candidate: event.candidate });
        }
      };

      this.peerConnection.ontrack = event => {
        this.$refs.remoteVideo.srcObject = event.streams[0];
      };

      const offer = await this.peerConnection.createOffer();
      await this.peerConnection.setLocalDescription(offer);
      socket.emit('signal', { roomId: this.roomId, type: 'offer', offer });
    },
    async handleOffer(offer) {
      this.peerConnection = new RTCPeerConnection();
      this.peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
      this.localStream.getTracks().forEach(track => {
        this.peerConnection.addTrack(track, this.localStream);
      });

      this.peerConnection.onicecandidate = event => {
        if (event.candidate) {
          socket.emit('signal', { roomId: this.roomId, type: 'candidate', candidate: event.candidate });
        }
      };

      this.peerConnection.ontrack = event => {
        this.$refs.remoteVideo.srcObject = event.streams[0];
      };

      const answer = await this.peerConnection.createAnswer();
      await this.peerConnection.setLocalDescription(answer);
      socket.emit('signal', { roomId: this.roomId, type: 'answer', answer });
    },
    async handleAnswer(answer) {
      await this.peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
    },
    handleCandidate(candidate) {
      this.peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
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
