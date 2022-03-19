<template>
    <div>
      <NavBar/>
      <div class="container">
            <div class="d-flex justify-content-start mt-1 mb-5">
                <h1>МОИ ЗАКАЗЫ</h1>
            </div>
      </div>
      <b-container class="mt-2 text-center" style="max-width: 25em">
          <b-form @submit="loadMyOrders()">
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
                  Показать мои заказы
              </button>
          </b-form>
      </b-container>
      <b-container v-show="get_my_orders">
        <b-container>
            <table v-if="my_orders.length > 0" class="table table-hover mt-4 mb-5">
                <thead>
                    <tr>
                        <th scope="col">Код</th>
                        <th scope="col">Диспетчер</th>
                        <th scope="col">Пилот</th>
                        <th scope="col">Клиент</th>
                        <th scope="col">Вертолёт</th>
                        <th scope="col">Адрес заказа</th>
                        <th scope="col">Адрес доставки</th>
                        <th scope="col">Дата поступления</th>
                        <th scope="col">Дата выполнения</th>
                        <th scope="col">Время аренды</th>
                        <th scope="col">Способ оплаты</th>
                        <th scope="col">Филиал</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(order, idx) in my_orders" :key="idx">
                        <td>{{ order.id }}</td>
                        <td>{{ order.dispetcher }}</td>
                        <td>{{ order.pilot }}</td>
                        <td>{{ order.client }}</td>
                        <td>{{ order.helicopter }}</td>
                        <td>{{ order.order_address }}</td>
                        <td>{{ order.delivery_address }}</td>
                        <td>{{ order.date_receipt }}</td>
                        <td>{{ order.date_completion }}</td>
                        <td>{{ order.rental_time }}</td>
                        <td>{{ order.payment_method }}</td>
                        <td>{{ getBranchName(order.branch_id) }}</td>
                    </tr>
                </tbody>
            </table>
            <div v-else-if="my_orders.answer == 'Not founded'" class="d-flex justify-content-center mt-2 mb-5">
                <h3>Сотрудник не найден</h3>
            </div>
            <div v-else class="d-flex justify-content-center mt-2 mb-5">
                <h3>Заказы не найдены</h3>
            </div>
        </b-container>
      </b-container>
    </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import axios from 'axios';

export default {
  components: { NavBar },
  name: 'MyOrders',
  data() {
    return {
      my_surname: null,
      my_name: null,
      my_orders: [],
      get_my_orders: false,
    }
  },
  methods: {
    loadMyOrders() {
      let userType = null;
      if (this.$store.state.session.userType == 1) {
        userType = "dispetcher";
      }
      else if (this.$store.state.session.userType == 2) {
        userType = "pilot";
      }
      const payload = {
        'surname': this.my_surname,
        'name': this.my_name
      };
      const path = `http://localhost:5000/my-orders/${userType}`;
      axios.post(path, payload)
        .then((response) => {
          this.my_orders = response.data;
          this.get_my_orders = true;
        })
        .catch((error) => {
          console.log(error);
          alert('Ошибка при загрузке заказов');
        })
    },
    getBranchName: function(branch_code) {
      if(this.branch_options.length != 0) {
          return this.branch_options.find(branch => branch.value === branch_code).text;
      }
    },
    async fetchBranchOptions() {
        try {
            const response = await axios.get('http://127.0.0.1:5000/branchOptions');
            this.branch_options = response.data;
        } catch (e) {
            alert('Возникла ошибка при получении Филиалов');
        }
    },
  },
  async created() {
    this.fetchBranchOptions(); 
  },
  mounted() {
      if (this.$store.state.session.userType > 2 || this.$store.state.session.userType < 1 || !this.$store.state.session.auth) {
        this.$router.push('/');
      }
  },
}
</script>

<style>

</style>