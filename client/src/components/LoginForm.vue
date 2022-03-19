<template>
 <div>
    <b-modal 
      centered
      ref="modal"
      v-model="showed"
      @hide="closeLoginForm"
      title="Авторизация"
      hide-footer
    >
      <b-row class="my-1 justify-content-md-center text-center">
        <p class="my-2">Введите пароль от учетной записи {{ getUserTypeName }}</p>
      </b-row>
      <b-row class="my-1 justify-content-md-center text-center">
        <p class="my-2 text-danger" v-if="wrongPassword">Неверный пароль!</p>
      </b-row>
      <b-row class="my-1 justify-content-md-center text-center">
        <div class="my-1 justify-content-md-center text-center">
          <form ref="form" @submit.prevent="handleSubmit">
            <b-form-group
              :state="passwordState"
              size="lg"
            >
              <b-form-input
                id="password-input"
                v-model="password"
                :state="passwordState"
                size="lg"
                type="password"
                required
              ></b-form-input>
              <div class="d-flex justify-content-center">
                <b-button-group class="mt-4" size="lg">
                        <b-button class="btn-sbmt" type="sumbit" variant="outline-primary">Войти</b-button> 
                        <b-button @click="closeLoginForm" variant="outline-secondary">Отмена</b-button>
                </b-button-group>
              </div>
            </b-form-group>
          </form>
        </div>
      </b-row>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    showed: { 
      type: Boolean,
      default: false,
      required: true
    },
    userType: {
      type: Number,
      default: 0,
      required: true
    }
  },
  data() {
    return {
      password: '',
      passwordState: null,
      wrongPassword: false,
      auth: false,
    }
  },
  name: 'LoginForm',
  computed: {
    getUserTypeName: function () {
      let userTypeName = null;
      switch(this.userType) {
        case 1: {
          userTypeName = 'Диспетчера';
          break;
        }
        case 2: {
          userTypeName = 'Пилота';
          break;
        }
        case 3: {
          userTypeName = 'Менеджера';
          break;
        }
      }
      return userTypeName;
    }
  },
  emits: ['onCloseLoginForm'],
  methods: {
    async handleSubmit() {
      await this.Authorization(this.userType, this.password).then(auth => this.auth = auth);
      if (this.auth) {
        this.$emit('onCloseLoginForm');
        this.$store.commit('session/setUserType', this.userType);
        this.$store.commit('session/setAuth', this.auth);
        switch(this.userType) {
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
      else {
        this.wrongPassword = true;
        setTimeout(() => {
          this.wrongPassword = false;
        }, 2000);
      }
    },
    closeLoginForm() {
      this.wrongPassword = false;
      this.$emit('onCloseLoginForm')
    },
    async Authorization(userType, password) {
      try {
        const response = await axios.post("http://127.0.0.1:5000/userAuth", {
          userCode: userType,
          inputPassword: password
        })
        if (response.data['auth'] == 'success')
          return true;
        else
          return false;
      } catch(e) {
        console.log(e);
      }
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .btn-sbmt {
    margin-right: 2em;
  }
</style>
