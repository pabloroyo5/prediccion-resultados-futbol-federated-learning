<template>
  <v-container>
    <v-row class="justify-center">
      <v-col cols="3">
        <v-select
          v-model="selectedCountry"
          :items="countries"
          item-title="name"
          item-value="id"
          label="Selecciona el país"
          variant="solo"
        ></v-select>
      </v-col>
      <v-col cols="3">
        <v-select
          v-model="year"
          :items="seasons"
          item-title="name"
          item-value="id"
          label="Selecciona la temporada"
          variant="solo"
        ></v-select>
      </v-col>
      <v-col cols="3">
        <v-select
          :disabled="selectedCountry === null || year === null"
          v-model="stage"
          :items="stagesData"
          label="Selecciona la jornada"
          variant="solo"
        ></v-select>
      </v-col>
    </v-row>
    <v-row class="d-flex justify-center align-center mt-2">
      <v-btn v-if="currentMatch" @click="previousMatch" class="btn-arrow">
        <v-icon large>mdi-chevron-left</v-icon>
      </v-btn>
      <v-col cols="4" md="4">
        <TeamCard
          :key="0"
          :country="nameOfCountrySelected"
          :flag="flagsOfCountrySelected"
          :teamName="currentMatch ? currentMatch.home_team_name : ''"
          :logo="currentMatch ? currentMatch.home_team_logourl : ''"
          :logo1="currentMatch ? currentMatch.home_team_logourl1 : ''"
          :logo2="currentMatch ? currentMatch.home_team_logourl2 : ''"
          :att="currentMatch && currentMatch.L_VAL_MEDIA_DEL ? currentMatch.L_VAL_MEDIA_DEL : '?'"
          :mid="currentMatch && currentMatch.L_VAL_MEDIA_MC ? currentMatch.L_VAL_MEDIA_MC : '?'"
          :def="currentMatch && currentMatch.L_VAL_MEDIA_DEF ? currentMatch.L_VAL_MEDIA_DEF : '?'"
          :por="currentMatch && currentMatch.L_VAL_MEDIA_POR ? currentMatch.L_VAL_MEDIA_POR : '?'"
          :league="leagueName"
        />
      </v-col>
      <v-col cols="4" md="4">
        <TeamCard
          :key="1"
          :country="nameOfCountrySelected"
          :flag="flagsOfCountrySelected"
          :teamName="currentMatch ? currentMatch.away_team_name : ''"
          :logo="currentMatch ? currentMatch.away_team_logourl : ''"
          :logo1="currentMatch ? currentMatch.away_team_logourl1 : ''"
          :logo2="currentMatch ? currentMatch.away_team_logourl2 : ''"
          :att="currentMatch && currentMatch.A_VAL_MEDIA_DEL ? currentMatch.A_VAL_MEDIA_DEL : '?'"
          :mid="currentMatch && currentMatch.A_VAL_MEDIA_MC ? currentMatch.A_VAL_MEDIA_MC : '?'"
          :def="currentMatch && currentMatch.A_VAL_MEDIA_DEF ? currentMatch.A_VAL_MEDIA_DEF : '?'"
          :por="currentMatch && currentMatch.A_VAL_MEDIA_POR ? currentMatch.A_VAL_MEDIA_POR : '?'"
          :league="leagueName"
        />
      </v-col>
      <v-btn v-if="currentMatch" @click="nextMatch" class="btn-arrow">
        <v-icon large>mdi-chevron-right</v-icon>
      </v-btn>
    </v-row>
    <v-row class="justify-center mt-6" v-if="currentMatch">
      <v-btn color="success" outlined @click="predict">PREDECIR</v-btn>
    </v-row>
    <v-row class="justify-center" v-if="showPieChart">
      <v-col cols="6">
        <PieChart
          :probabilities="probabilities"
          :labels="[
            currentMatch ? currentMatch.home_team_name : 'Victoria local',
            'Empate',
            currentMatch ? currentMatch.away_team_name : 'Victoria visitante'
          ]"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import TeamPicker from "@/components/TeamPicker.vue";
import TeamCard from "@/components/TeamCard.vue";
import PieChart from "@/components/PieChart.vue";
import axios from "axios";

export default {
  name: "HomeView",
  components: {
    TeamPicker,
    TeamCard,
    PieChart,
  },
  data() {
    return {
      selectedCountry: null,
      countries: [],
      seasons: [
        { id: 2015, name: "2015/2016" },
      ],
      year: null,
      stage: null,
      stagesData: [],
      leagueName: "Unknown",
      matchesData: [],
      currentMatch: null,
      currentMatchIndex: 0,
      probabilities: [0, 0, 0],
      showPieChart: false,
    };
  },
  computed: {
    nameOfCountrySelected() {
      if (this.selectedCountry) {
        const country = this.countries.find((country) => country.id === this.selectedCountry);
        return country ? country.name : "Unknown";
      }
      return "Unknown";
    },
    flagsOfCountrySelected() {
      if (this.selectedCountry) {
        const country = this.countries.find((country) => country.id === this.selectedCountry);
        return country ? country.flag : "Unknown";
      }
      return "Unknown";
    }
  },
  methods: {
    async fetchLeague() {
      try {
        const response = await axios.get(`http://localhost:5000/api/leagues/${this.selectedCountry}`);
        this.leagueName = response.data[0].name;
      } catch (error) {
        console.error("There was an error fetching the league!", error);
        this.leagueName = "Unknown";
      }
    },
    async fetchStages() {
      if (this.year) {
        try {
          const response = await axios.get(`http://localhost:5000/api/stages/${this.selectedCountry}/${this.year}`);
          console.log([response.data]);
          this.stagesData = [response.data];

        } catch (error) {
          console.error("There was an error fetching the stages!", error);
          this.stagesData = [];
        }
      }
    },
    async fetchCountries() {
      try {
        const response = await axios.get("http://localhost:5000/api/countries");
        this.countries = response.data;
      } catch (error) {
        console.error("There was an error fetching the countries!", error);
        this.countries = [];
      }
    },
    async fetchMatches() {
      if (this.stage) {
        try {
          const response = await axios.get(`http://localhost:5000/api/matches/${this.selectedCountry}/${this.year}/${this.stage}`);
          this.matchesData = response.data;
          this.currentMatchIndex = 0; // Reset the index when new matches are fetched
          this.currentMatch = this.matchesData[this.currentMatchIndex];
        } catch (error) {
          console.error("There was an error fetching the matches!", error);
        }
      }
    },
    previousMatch() {
      this.showPieChart = false;
      if (this.matchesData.length > 0) {
        this.currentMatchIndex =
          this.currentMatchIndex === 0
            ? this.matchesData.length - 1
            : this.currentMatchIndex - 1;
        this.currentMatch = this.matchesData[this.currentMatchIndex];
      }
    },
    nextMatch() {
      this.showPieChart = false;
      if (this.matchesData.length > 0) {
        this.currentMatchIndex =
          this.currentMatchIndex === this.matchesData.length - 1
            ? 0
            : this.currentMatchIndex + 1;
        this.currentMatch = this.matchesData[this.currentMatchIndex];
        console.log(this.matchesData.length);
      }
    },
    async predict() {
      if (this.currentMatch) {
        this.showPieChart = false;

        try {
          const response = await axios.get(`http://localhost:5000/api/predict/${this.currentMatch.match_api_id}`);
          this.probabilities = response.data;
          this.showPieChart = true;
        } catch (error) {
          console.error("There was an error fetching the prediction!", error);
          this.showPieChart = false;
        }
      }
    },
  },
  watch: {
    selectedCountry(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.fetchLeague();
        this.fetchStages();
        this.stage = null;
        this.currentMatch = null;
        this.currentMatchIndex = 0;
        this.showPieChart = false;
        this.matchesData = [];
      }
    },
    year(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.fetchStages();
        this.stage = null;
        this.currentMatch = null;
        this.currentMatchIndex = 0;
        this.showPieChart = false;
        this.matchesData = [];
      }
    },
    stage(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.fetchMatches();
        this.showPieChart = false;

      }
    },
  },
  created() {
    this.fetchCountries();
  }
};
</script>

<style scoped>
.v-container {
  margin-top: 20px;
}

.btn-arrow {
  margin-top: 10px; /* Espacio entre los botones y los TeamCards */
  font-size: 24px; /* Tamaño de la fuente de los botones */
}
</style>
