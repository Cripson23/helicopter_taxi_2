<template>
  <div>
    <div class="login-form">
      <LoginForm 
        :showed="showed"
        :userType="userType"
        @onCloseLoginForm="closeLoginForm"
      />
    </div>
    <b-container>
      <b-row class="select-category-row text-center" align-v="center">
        <div class="title">
          <h1>ВЫБЕРИТЕ ТИП УЧЕТНОЙ ЗАПИСИ ДЛЯ АВТОРИЗАЦИИ</h1>
        </div>
        <b-col>
          <div @click="selectUserType(1)" class="select-category col-sm-6 col-lg-4">
            <h3>ДИСПЕТЧЕР</h3>
            <img src="../assets/dispatcher.png" class="img-fluid mx-auto d-block" alt="Диспетчер">
          </div>
        </b-col>
        <b-col>
          <div @click="selectUserType(2)" class="select-category col-sm-6 col-lg-4 text-center">
            <h3>ПИЛОТ</h3>
            <img src="../assets/pilot.png" class="img-fluid mx-auto d-block" alt="Пилот">
          </div>
        </b-col>
        <b-col>
          <div @click="selectUserType(3)" class="select-category col-sm-6 col-lg-4 text-center">
            <h3>МЕНЕДЖЕР</h3>
            <img src="../assets/manager.png" class="img-fluid mx-auto d-block" alt="Менеджер">
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>

import LoginForm from '@/components/LoginForm.vue'

export default {
  name: 'LoginPage',
  mounted() {
      if (this.$store.state.session.userType > 0 && this.$store.state.session.auth) {
        switch(this.$store.state.session.userType) {
          case 1: {
            this.$router.push('clients');
            break;
          }
          case 2: {
            this.$router.push('my-orders');
            break;
          }
          case 3: {
            this.$router.push('employees');
            break;
          }
        }
      }
  },
  data() {
    return {
      showed: false,
      userType: 0,
    }
  },
  components: {
    LoginForm
  },
  methods: {
    closeLoginForm() {
      this.showed = false;
    },
    selectUserType(type) {
      this.userType = type;
      this.showLoginForm();
    },
    showLoginForm() {
      this.showed = true;
    }
  },
  
}
</script>

<style scoped>
  h3 {
    color: grey;
  }
  .select-category {
    width: 300px;
    height: 300px;
    border-radius: 20px;
    margin: auto;
    margin-bottom: 30px;
    margin-top: 30px;
    background-color: lightgoldenrodyellow;
    padding-top: 1em;
    color:rgb(90, 90, 90);
  }
  .select-category img {
    max-width: 80%;
    max-height: 80%;
    padding-top: 1em;
  }
  .select-category:hover {
    border: 3px solid;
    border-color: rgb(252, 137, 137);
    cursor: pointer;
  }
  .title {
    margin-top: 400px;
  }
  .select-category-row {
    margin-top: -20em;
  }
</style>