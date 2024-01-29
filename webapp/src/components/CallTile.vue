<template>
  <main style="height: 100vh;">
    <!-- loading is true when the call is in the "joining-meeting" meeting state -->
    <template v-if="loading">
      <div class="loading-spinner"><loading-tile /></div>
    </template>

    <template v-else>
      <div class="wrapper">
        <template v-if="error">
          <p class="error-text">{{ error }}</p>
          <!-- refreshing will leave the call and reset the app state -->
          <button class="error-button" @click="leaveAndCleanUp">Refresh</button>
        </template>

        <template v-if="showPermissionsError">
          <permissions-error-msg :reset="leaveAndCleanUp" />
        </template>

        <template v-else>
          <div
            :class="screen ? 'tile-container' : 'tile-container full-height'"
          >
            <template v-if="screen">
              <screenshare-tile :participant="screen" />
            </template>

            <div v-if="participants" class="participants-container">
              
                <template v-for="p in participants" :key="p.session_id">
                  <div v-if="p.video" style="display: flex;flex-direction: column; width: 50%;">
                    <video-tile
                      :participant="p"
                      :handle-video-click="handleVideoClick"
                      :handle-audio-click="handleAudioClick"
                      :handle-screenshare-click="handleScreenshareClick"
                      :leave-call="leaveAndCleanUp"
                      :disable-screen-share="screen && !screen?.local"
                      :health="p.health"
                      @click="decreaseHealth(p.session_id)"
                    />
                    <div style="display: none;">
                      <div v-if="serverData && serverData[participants.indexOf(p)]" style="">
                        <p>Happiness score: {{ serverData[participants.indexOf(p)] }}</p>
                      </div>
                      <div v-if="serverData && serverData[participants.indexOf(p)]" style="">
                        <p style="margin-top: 0;">Health: {{ participants[participants.indexOf(p)].health }}</p>
                      </div>
                    </div>
                  </div>
                </template>

              <template v-if="count === 1">
                <waiting-card :url="roomUrl" />
              </template>
            </div>
          </div>
        </template>
      </div>
    </template>
  </main>
</template>

<script>
import daily from "@daily-co/daily-js";

import WaitingCard from "./WaitingCard.vue";
// import ChatTile from "./ChatTile.vue";
import VideoTile from "./VideoTile.vue";
import ScreenshareTile from "./ScreenshareTile.vue";
import LoadingTile from "./LoadingTile.vue";
import PermissionsErrorMsg from "./PermissionsErrorMsg.vue";


export default {
  name: "CallTile",
  components: {
    VideoTile,
    WaitingCard,
    // ChatTile,
    ScreenshareTile,
    LoadingTile,
    PermissionsErrorMsg,
  },
  props: ["leaveCall", "name", "roomUrl"],
  data() {
    return {
      callObject: null,
      participants: null,
      count: 0,
      messages: [],
      error: false,
      loading: false,
      showPermissionsError: false,
      screen: null,
      websocket: null,
      serverData: null,
    };
  },
  mounted() {
    this.websocket = new WebSocket("ws://localhost:6789");
    this.websocket.onmessage = (event) => {
      console.log("[WEBSOCKET] ", event.data);
      this.serverData = JSON.parse(event.data);
      // Add health to this.participants
      this.participants.forEach((p) => {
        p.health = p.health - this.serverData[this.participants.indexOf(p)];
        // round to 3 decimal places
        p.health = Math.round((p.health + Number.EPSILON) * 1000) / 1000;
        if (p.health < 0) {
          p.health = 0;
        }
      });
      // If anyone has 0 health, stop updating health
      this.participants.forEach((p) => {
        if (p.health === 0) {
          this.websocket.close();
        }
      });

      // console.log("[PARTICIPANTS] ", this.participants);
    };

    const option = {
      url: this.roomUrl,
    };

    // Create instance of Daily call object
    const co = daily.createCallObject(option);
    // Assign in data obj for future reference
    this.callObject = co;

    // Join the call with the name set in the Home.vue form
    co.join({ userName: this.name });

    // Add call and participant event handler
    // Visit https://docs.daily.co/reference/daily-js/events for more event info
    co.on("joining-meeting", this.handleJoiningMeeting)
      .on("joined-meeting", this.updateParticpants)
      .on("participant-joined", this.updateParticpants)
      .on("participant-updated", this.updateParticpants)
      .on("participant-left", this.updateParticpants)
      .on("error", this.handleError)
      // camera-error = device permissions issue
      .on("camera-error", this.handleDeviceError)
      // app-message handles receiving remote chat messages
      .on("app-message", this.updateMessages);
  },
  unmounted() {
    // Close WebSocket connection
    if (this.websocket) {
      this.websocket.close();
    }

    if (!this.callObject) return;
    // Clean-up event handlers
    this.callObject
      .off("joining-meeting", this.handleJoiningMeeting)
      .off("joined-meeting", this.updateParticpants)
      .off("participant-joined", this.updateParticpants)
      .off("participant-updated", this.updateParticpants)
      .off("participant-left", this.updateParticpants)
      .off("error", this.handleError)
      .off("camera-error", this.handleDeviceError)
      .off("app-message", this.updateMessages);
  },
  methods: {
    decreaseHealth(sessionId) {
      const participant = this.participants.find(p => p.session_id === sessionId);
      if (participant) {
        participant.health = Math.max(participant.health - 10, 0);
      }
    },
    /**
     * This is called any time a participant update registers.
     * In large calls, this should be optimized to avoid re-renders.
     * For example, track-started and track-stopped can be used
     * to register only video/audio/screen track changes.
     */
    updateParticpants(e) {
      console.log("[EVENT] ", e);
      if (!this.callObject) return;

      const p = this.callObject.participants();
      this.count = Object.values(p).length;
      this.participants = Object.values(p);

      // Add health to this.participants
      this.participants.forEach((p) => {
        p.health = 100;
      });

      console.log("[PARTICIPANTS] ", this.participants);

      const screen = this.participants.filter((p) => p.screenVideoTrack);
      if (screen?.length && !this.screen) {
        console.log("[SCREEN]", screen);
        this.screen = screen[0];
      } else if (!screen?.length && this.screen) {
        this.screen = null;
      }
      this.loading = false;
    },
    // Add chat message to local message array
    updateMessages(e) {
      console.log("[MESSAGE] ", e.data);
      this.messages.push(e?.data);
    },
    // Show local error in UI when daily-js reports an error
    handleError(e) {
      console.log("[ERROR] ", e);
      this.error = e?.errorMsg;
      this.loading = false;
    },
    // Temporary show loading view while joining the call
    handleJoiningMeeting() {
      this.loading = true;
    },
    // Toggle local microphone in use (on/off)
    handleAudioClick() {
      const audioOn = this.callObject.localAudio();
      this.callObject.setLocalAudio(!audioOn);
    },
    // Toggle local camera in use (on/off)
    handleVideoClick() {
      const videoOn = this.callObject.localVideo();
      this.callObject.setLocalVideo(!videoOn);
    },
    // Show permissions error in UI to alert local participant
    handleDeviceError() {
      this.showPermissionsError = true;
    },
    // Toggle screen share
    handleScreenshareClick() {
      if (this.screen?.local) {
        this.callObject.stopScreenShare();
        this.screen = null;
      } else {
        this.callObject.startScreenShare();
      }
    },
    /**
     * Send broadcast message to all remote call participants.
     * The local participant updates their own message history
     * because they do no receive an app-message Daily event for their
     * own messages.
     */
    sendMessage(text) {
      // Attach the local participant's username to the message to be displayed in ChatTile.vue
      const local = this.callObject.participants().local;
      const message = { message: text, name: local?.user_name || "Guest" };
      this.messages.push(message);
      this.callObject.sendAppMessage(message, "*");
    },
    // leave call, destroy call object, and reset local state values
    leaveAndCleanUp() {
      if (this.screen?.local) {
        this.callObject.stopScreenShare();
      }
      this.callObject.leave().then(() => {
        this.callObject.destroy();

        this.participantWithScreenshare = null;
        this.screen = null;
        this.leaveCall();
      });
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Ropa+Sans&display=swap");
main {
  font-family: "Ropa Sans", sans-serif;
  background-image: url('../assets/bg-home-new.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center bottom;
  background-color: #9437B7;
  height: 100%;
  position: relative;
}
.wrapper {
  max-width: 1200px;
  margin: auto;
  padding: 0 16px;
  height: 100%;
}
.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
.tile-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.participants-container {
  height: 100vh;
  display: flex;
  margin: 0 -20px;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  width: 100%;
  height: inherit;
}
p {
  color: white;
}
.error-text {
  color: #e71115;
}
.full-height {
  height: 100vh;
}
.error-button {
  color: #fff;
  background-color: #9437B7;
  border: none;
  font-size: 12px;
  border: 1px solid #2b3f56;
  border-radius: 0;
  padding: 8px 12px;
  cursor: pointer;
}
</style>
