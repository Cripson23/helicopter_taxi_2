<template>
    <div>
      <NavBar/>
      <div class="container">
            <div class="d-flex justify-content-start mt-1 mb-5">
                <h1>ДАТА МОЕЙ ПЕРЕАТТЕСТАЦИИ</h1>
            </div>
      </div>
      <b-container class="mt-2 text-center" style="max-width: 25em">
          <b-form @submit="getMyRecert()">
              <b-form-group id="form-my-surname-group"
                          label="Фамилия"
                          label-for="form-my-surname-input"
                          label-cols-sm="3"
                          >
                  <b-form-input id="form-my-surname-input"
                          type="text"
                          v-model="my_surname"
                          required
                          placeholder="Введите свою фамилию">
                  </b-form-input>
              </b-form-group>
              <b-form-group id="form-my-name-group"
                          label="Имя"
                          label-for="form-my-name-input"
                          label-cols-sm="3">
                  <b-form-input id="form-my-name-input"
                          type="text"
                          v-model="my_name"
                          required
                          placeholder="Введите своё имя">
                  </b-form-input>
              </b-form-group>
              <button
                  type="submit"
                  class="btn btn-success btn-bg mt-2">
                  Получить дату
              </button>
          </b-form>
      </b-container>
    </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import axios from 'axios';

export default {
  components: { NavBar },
  name: 'MyRecertification',
  data() {
    return {
      my_surname: null,
      my_name: null,
    }
  },
  methods: {
    getMyRecert() {
      const payload = {
        'surname': this.my_surname,
        'name': this.my_name
      };
      const path = `http://localhost:5000/my-recertification`;
      axios.post(path, payload)
        .then((response) => {
          const date = response.data.date;
          if (date == 'Not found')
            alert('Информация не найдена');
          else {
            alert('Дата вашей следующей переаттестации: ' + date);
          }
        })
        .catch((error) => {
          console.log(error);
          alert('Ошибка при загрузке даты переаттестации');
        })
    }, 
  },
  mounted() {
      if (this.$store.state.session.userType != 2 || !this.$store.state.session.auth) {
        this.$router.push('/');
      }
  },
}
</script>

<style>

</style>