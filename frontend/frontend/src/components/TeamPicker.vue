<template>
  <v-row class="justify-center">
    <v-col cols="12" md="6">
      <v-card class="pa-4">
        <v-row>
          <v-col class="text-center">
            <h2>ENGLAND</h2>
          </v-col>
          <v-col class="text-center">
            <h2>FRANCE</h2>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="text-center">
            <p>ATT: 85 | MID: 83 | DEF: 83</p>
          </v-col>
          <v-col class="text-center">
            <p>ATT: 88 | MID: 84 | DEF: 86</p>
          </v-col>
        </v-row>
        <v-row class="justify-center">
          <v-btn class="mx-2" outlined>VS</v-btn>
        </v-row>
        <v-row class="justify-center">
          <v-btn class="mx-2" outlined>LIVE FORM</v-btn>
        </v-row>
        <v-row>
          <v-col class="text-center">
            <h4>Premier League</h4>
          </v-col>
          <v-col class="text-center">
            <h4>Ligue 1 Uber Eats</h4>
          </v-col>
        </v-row>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "TeamPicker",
};
</script>
