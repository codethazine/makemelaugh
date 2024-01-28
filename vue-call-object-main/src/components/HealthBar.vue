<script>
export default {
    data() {
        return {
            maxHealth: 100,
            currentHealth: 100,
            showTrail: false,
            trailWidth: 0,
            healthColor: '#4caf50',
            trailColor: '#ff0000',
        }
    },
    props: {
        health: {
            type: Number,
            default: 100,
        },
    },
    computed: {
        healthPercentage() {
            return (this.currentHealth / this.maxHealth) * 100;
        },
    },
    methods: {
        loseLife(amount) {
            this.showTrail = true;
            this.currentHealth -= amount;
            if (this.currentHealth < 0) {
                this.currentHealth = 0;
            }

            setTimeout(() => {
                this.showTrail = false;
                this.trailWidth = 0;
            }, 500);
        },
        handleLeftArrowKey() {
            this.loseLife(20);
        },
    },
    watch: {
        showTrail(newValue) {
            if (newValue) {
                this.trailWidth = Math.min((100 - this.healthPercentage) * 2, 100);
            }
        },

    },
    mounted() {
        document.addEventListener('keydown', this.handleKeyDown);
    }
}
</script>

<template>
    <div class="health-bar-container" @click="loseLife(10)" @keyup.enter="loseLife(20)">
        <div class="health-bar">
            <div class="health-remaining" :style="{ width: health + '%' }"></div>
        </div>
        <!--
        <button @click="loseLife(10)">Lose 10 Life</button>
        <button @click="loseLife(20)">Lose 20 Life</button>
        <p>Current Health: {{ currentHealth }}</p>
        -->
    </div>
</template>

<style scoped>
.health-bar-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
    z-index: 50;

}

.health-bar {
    position: relative;
    width: 100%;
    height: 30px;
    border: 1px solid #000;
    overflow: hidden;
    color: #cecece;
    background-color: #ffffff;
    border: 3px solid #228B22;
    text-shadow: 0 0 3px #000;
    box-shadow: 0 2px #006400;
}

.health-remaining {
    height: 100%;
    background-color: #4caf50;
    transition: width 0.5s ease-in-out;
}
</style>