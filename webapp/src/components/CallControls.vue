<template>
  <!--
  <div class="controls">
    
    <div class="devices">
      <button @click="handleAudioClick">
        <template v-if="participant.audio">
          <img class="icon" :src="micOn" alt="" />
        </template>
        <template v-else>
          <img class="icon" :src="micOff" alt="" />
        </template>
      </button>

      <button @click="handleVideoClick">
        <template v-if="participant.video">
          <img class="icon" :src="videoOn" alt="" />
        </template>
        <template v-else>
          <img class="icon" :src="videoOff" alt="" />
        </template>
      </button>

      <template v-if="supportsScreenshare">
        <button :disabled="disableScreenShare" @click="handleScreenshareClick">
          <img class="icon" :src="screenShare" alt="" />
        </button>
      </template>
    </div>
  </div>
  -->
  <button class="leave" @click="leaveCall">
    <img class="icon" alt="" src="../assets/logo.png" />
  </button>
</template>

<script>
import daily from "@daily-co/daily-js";

import leave from "../assets/leave_call.svg";
import micOff from "../assets/mic_off.svg";
import micOn from "../assets/mic_on.svg";
import screenShare from "../assets/screenshare.svg";
import videoOff from "../assets/vid_off.svg";
import videoOn from "../assets/vid_on.svg";

export default {
  name: "CallControls",
  props: [
    "participant",
    "handleVideoClick",
    "handleAudioClick",
    "handleScreenshareClick",
    "leaveCall",
    "disableScreenShare",
  ],
  data() {
    return {
      leave,
      micOn,
      micOff,
      screenShare,
      videoOn,
      videoOff,
      supportsScreenshare: false,
    };
  },
  mounted() {
    // Only show the screen share button if the browser supports it
    this.supportsScreenshare = daily.supportedBrowser().supportsScreenShare;
  },
};
</script>

<style scoped>
.controls {
  position: absolute;
  bottom: 12px;
  left: 8px;
  justify-content: space-between;
  display: flex;
  width: calc(100% - 16px);
}

.devices {
  border-radius: 0;
  background-color: #9437B7;
  opacity: 0.85;
  padding: 14px 10px 15px;
}
button {
  background-color: transparent;
  border: none;
  cursor: pointer;
}
button:not(.leave) {
  margin: 0 4px;
  width: 72px;
  height: 52px;
}
button.leave {
  background-color: transparent;
  opacity: 0.85;
  padding: 0;
  border-radius: 0;
}
button:disabled {
  cursor: not-allowed;
  opacity: 0.4;
}
.icon {
  width: 148px;
  height: 72px;
}
</style>
