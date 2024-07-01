<template>
    <v-card class="team-card">
        <v-card-title class="title">
            <v-row justify="space-between">
                <v-col cols="4">
                </v-col>
                <v-col cols="4" class="text-center">
                    <span>{{ country }}</span>
                </v-col>
                <v-col cols="4" class="text-right">
                    <v-img :src="flag" class="flag" />
                </v-col>
            </v-row>
        </v-card-title>

        <v-card-text class="text-center">
            <v-img :src="currentLogo" class="logo" @error="onLogoError" />
            <div class="team-name">{{ teamName }}</div>
            <div class="stats">
                <div class="stat">
                    <span>POR</span>
                    <span class="value">{{ por }}</span>
                </div>
                <div class="stat">
                    <span>DEF</span>
                    <span class="value">{{ def }}</span>
                </div>
                <div class="stat">
                    <span>MC</span>
                    <span class="value">{{ mid }}</span>
                </div>
                <div class="stat">
                    <span>DEL</span>
                    <span class="value">{{ att }}</span>
                </div>
            </div>
            <div class="league">{{ league }}</div>
        </v-card-text>
    </v-card>
</template>

<script>
export default {
    name: "TeamCard",
    props: {
        country: {
            type: String,
            default: "Unknown",
        },
        flag: {
            type: String,
            default: "default_flag.png",
        },
        teamName: {
            type: String,
            default: "Unnamed Team",
        },
        logo: {
            type: String,
            default: "https://www.espn.com/i/teamlogos/soccer/500/default-team-logo-500.png?h=100&w=100",
        },
        logo1: {
            type: String,
            default: "https://www.espn.com/i/teamlogos/soccer/500/default-team-logo-500.png?h=100&w=100",
        },
        logo2: {
            type: String,
            default: "https://www.espn.com/i/teamlogos/soccer/500/default-team-logo-500.png?h=100&w=100",
        },
        att: {
            type: Number,
            default: 0,
        },
        attDown: {
            type: Boolean,
            default: false,
        },
        mid: {
            type: Number,
            default: 0,
        },
        por: {
            type: Number,
            default: 0,
        },
        midUp: {
            type: Boolean,
            default: false,
        },
        def: {
            type: Number,
            default: 0,
        },
        defUp: {
            type: Boolean,
            default: false,
        },
        league: {
            type: String,
            default: "Unknown League",
        },
    },

    data() {
        return {
            currentLogo: this.logo,
            logoFallbacks: [this.logo1, this.logo2],
            logoFallbackIndex: 0,
            defaultLogo: "https://www.espn.com/i/teamlogos/soccer/500/default-team-logo-500.png?h=100&w=100",
        };
    },
    watch: {
        logo(newLogo) {
            this.resetLogoState(newLogo, this.logo1, this.logo2);
        },
        logo1(newLogo1) {
            this.logoFallbacks[0] = newLogo1;
        },
        logo2(newLogo2) {
            this.logoFallbacks[1] = newLogo2;
        }
    },
    methods: {
        resetLogoState(logo, logo1, logo2) {
            this.currentLogo = logo;
            this.logoFallbacks = [logo1, logo2];
            this.logoFallbackIndex = 0;
        },
        onLogoError() {
            if (this.logoFallbackIndex < this.logoFallbacks.length) {
                this.currentLogo = this.logoFallbacks[this.logoFallbackIndex];
                this.logoFallbackIndex++;
            } else {
                this.currentLogo = this.defaultLogo;
            }
        },
    },

};
</script>

<style scoped>
.team-card {
    max-width: 500px;
    margin: auto;
    min-height: 500px;
}

.title {
    background-color: #37474f;
    color: white;
    padding: 10px;
}

.flag {
    width: 35px;
    height: 35px;
}

.logo {
    width: 250px;
    height: 250px;
    margin: auto;
}

.team-name {
    font-size: 24px;
    margin: 10px 0;
}

.stars {
    display: flex;
    justify-content: center;
    margin: 10px 0;
}

.star {
    font-size: 24px;
}

.stats {
    display: flex;
    justify-content: space-around;
    margin: 10px 0;
}

.stat {
    text-align: center;
}

.value {
    display: block;
    font-size: 30px;
}

.red {
    color: red;
}

.green {
    color: green;
}

.league {
    background-color: #37474f;
    color: white;
    padding: 5px;
    margin-top: 10px;
}
</style>
