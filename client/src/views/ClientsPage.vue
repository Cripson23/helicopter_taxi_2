<template>
    <div>
      <NavBar/>
      <div class="container">
        <div class="d-flex justify-content-start mt-1 mb-5">
          <h1>КЛИЕНТЫ</h1>
        </div>
        <alert :message="message" v-if="showMessage"></alert>
        <div class="input-group-sm col-md-3">
            <input placeholder="Поиск клиента" v-model="searchClientStr" type="text" class="form-control sm" aria-describedby="inputHelp">
            <div id="inputHelp" class="form-text">
                Начните вводить номер телефона или почту
            </div>
        </div>
        <div class="d-md-flex justify-content-md-end me-5 pb-3 pt-2">
            <my-select
              v-model="selectedSort"
              :options="sortOptions"
            />
            <my-select
                v-model="selectedSortMethod"
                :options="sortMethodOptions"
                style="margin-left: 20px"
            />
        </div>
        <table class="table table-hover mt-4">
            <thead>
                <tr>
                <th scope="col">Код клиента</th>
                <th scope="col">Имя</th>
                <th scope="col">Отчество</th>
                <th scope="col">Номер телефона</th>
                <th scope="col">Электронная почта</th>
                <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(client, index) in sortedAndSearchClients" :key="index">
                <td>{{ client.client_id }}</td>
                <td>{{ client.name }}</td>
                <td>{{ client.patronymic }}</td>
                <td>{{ client.phone_number }}</td>
                <td>{{ client.email }}</td>
                <td>
                    <div v-if="$store.state.session.userType === 1 || $store.state.session.userType === 3">
                      <button
                          type="button"
                          class="btn btn-warning btn-sm me-3"
                          @click="onEditClient(client)">
                          Изменить
                      </button>
                      <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="onDeleteClient(client.client_id)">
                          Удалить
                      </button>
                    </div>
                </td>
                </tr>
            </tbody>
        </table>
        <div class="d-md-flex justify-content-md-end me-5 pb-3 pt-2" v-if="$store.state.session.userType === 1 || $store.state.session.userType === 3">
            <button type="button" @click="show_add_client_modal=true" style="margin-right: 22px" class="btn btn-success btn-sm">Добавить клиента</button>
        </div>
      </div>
      <b-modal
          centered
          title="Добавление клиента"
          v-model="show_add_client_modal"
          hide-footer>
          <b-form @submit="onAddClientSubmit" @reset="onAddClientReset" class="w-100">
              <b-form-group id="form-name-client-group"
                          label="Имя:"
                          label-for="form-name-client-input">
                <b-form-input id="form-name-client-input"
                                type="text"
                                v-model="formData.name"
                                required
                                placeholder="Введите имя">
                </b-form-input>
              </b-form-group>
              <b-form-group id="form-patronymic-client-group"
                          label="Отчество:"
                          label-for="form-patronymic-client-input">
                <b-form-input id="form-patronymic-client-input"
                                type="text"
                                v-model="formData.patronymic"
                                required
                                placeholder="Введите отчество">
                </b-form-input>
              </b-form-group>
              <b-form-group id="form-phone-client-group"
                          label="Номер телефона:"
                          label-for="form-phone-client-input">
                <b-form-input id="form-phone-client-input"
                                type="text"
                                v-model="formData.phone_number"
                                required
                                placeholder="Введите номер телефона">
                </b-form-input>
              </b-form-group>
              <b-form-group id="form-email-client-group"
                          label="Электронная почта:"
                          label-for="form-email-client-input">
                <b-form-input id="form-email-client-input"
                                type="text"
                                v-model="formData.email"
                                required
                                placeholder="Введите электронную почту">
                </b-form-input>
              </b-form-group>
              <b-button class="me-3" type="submit" variant="primary">Добавить</b-button>
              <b-button type="reset" variant="danger">Отмена</b-button>
          </b-form>
      </b-modal>
      <b-modal
          title="Изменить клиента"
          v-model="show_edit_modal"
          centered
          @hide="onResetUpdate"
          hide-footer>
          <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
              <b-form-group id="form-name-client-group"
                          label="Имя:"
                          label-for="form-name-client-input">
                <b-form-input id="form-name-client-input"
                                type="text"
                                v-model="formData.name"
                                required
                                placeholder="Введите имя">
                </b-form-input>
              </b-form-group>
              <b-form-group id="form-patronymic-client-group"
                          label="Отчество:"
                          label-for="form-patronymic-client-input">
                <b-form-input id="form-patronymic-client-input"
                                type="text"
                                v-model="formData.patronymic"
                                required
                                placeholder="Введите отчество">
                </b-form-input>
              </b-form-group>
              <b-form-group id="form-phone-client-group"
                          label="Номер телефона:"
                          label-for="form-phone-client-input">
                <b-form-input id="form-phone-client-input"
                                type="text"
                                v-model="formData.phone_number"
                                required
                                placeholder="Введите номер телефона">
                </b-form-input>
              </b-form-group>
              <b-form-group id="form-email-client-group"
                          label="Электронная почта:"
                          label-for="form-email-client-input">
                <b-form-input id="form-email-client-input"
                                type="text"
                                v-model="formData.email"
                                required
                                placeholder="Введите электронную почту">
                </b-form-input>
              </b-form-group>
              <b-button class="me-3" type="submit" variant="primary">Сохранить</b-button>
              <b-button type="reset" variant="danger">Отмена</b-button>
          </b-form>
      </b-modal>
    </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import Alert from '../components/Alert.vue';
import mySelect from '../components/mySelect.vue';
import axios from 'axios';
import showMessage from '@/mixins/showMessage';

export default {
  mixins: [showMessage],
  components: { NavBar, Alert, mySelect },
  name: 'ClientsPage',
  data() {
    return {
      searchClientStr: '',
      show_add_client_modal: false,
      clients: [],
      formData: {
        'id': null,
        'name': null,
        'patronymic': null,
        'phone_number': null,
        'email': null,
      },
      show_edit_modal: false,
      selectedSortMethod: 'ascending',
      sortMethodOptions: [
          {value: 'ascending', name: 'По возрастанию'},
          {value: 'descending', name: 'По убыванию'},  
      ],
      selectedSort: 'id',
      sortOptions: [
        {value: 'id', name: 'По коду'},
        {value: 'name', name: 'По имени'},
        {value: 'patronymic', name: 'По отчеству'},
        {value: 'phone_number', name: 'По номеру телефона'},
        {value: 'email', name: 'По почте'},
      ],
    }
  },
  methods: {
    fetchClients() {
      const path = `http://localhost:5000/clients`;
      axios.get(path)
      .then((response) => {
        this.clients = response.data;
      })
      .catch((error) => {
        console.log(error);
        alert('Произошла ошибка при получении клиентов!');
      })
    },
    initForm() {
      this.formData.id = null;
      this.formData.name = null;
      this.formData.patronymic = null;
      this.formData.phone_number = null;
      this.formData.email = null;
    },
    onAddClientSubmit(evt) {
      evt.preventDefault();
      const payload = {
        'name': this.formData.name,
        'patronymic': this.formData.patronymic,
        'phone_number': this.formData.phone_number,
        'email': this.formData.email
      }
      this.addClient(payload);
    },
    addClient(payload) {
      const path = `http://localhost:5000/clients`;
      axios.post(path, payload)
      .then(() => {
        this.fetchClients();
        this.show_add_client_modal = false;
        this.initForm();
        this.showMessageHandle('Клиент успешно добавлен');
      })
      .catch((error) => {
        console.log(error);
        alert('Ошибка при добавлении клиента!');
      })
    },
    onAddClientReset(evt) {
      evt.preventDefault();
      this.show_add_client_modal = false;
      this.initForm();
    },
    onDeleteClient(clientID) {
      this.removeClient(clientID);
    },
    removeClient(clientID) {
      const path = `http://localhost:5000/clients/${clientID}`;
      axios.delete(path)
      .then(() => {
        this.fetchClients();
        this.showMessageHandle('Клиент успешно удален');
      })
      .catch((error) => {
        console.log(error);
        alert('Ошибка при удалении клиента!');
      })
    },
    onEditClient(client) {
      this.formData.id = client.client_id;
      this.formData.name = client.name;
      this.formData.patronymic = client.patronymic;
      this.formData.phone_number = client.phone_number;
      this.formData.email = client.email;
      this.show_edit_modal = true;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      const payload = {
        'name': this.formData.name,
        'patronymic': this.formData.patronymic,
        'phone_number': this.formData.phone_number,
        'email': this.formData.email
      };
      this.updateClient(payload, this.formData.id);
    },
    updateClient(payload, clientID) {
      const path = `http://localhost:5000/clients/${clientID}`;
      axios.put(path, payload)
      .then(() => {
        this.fetchClients();
        this.show_edit_modal = false;
        this.initForm();
        this.showMessageHandle('Клиент успешно изменен');
      })
      .catch((error) => {
        console.log(error);
        alert('Ошибка при изменении клиента!');
      })
    },
    onResetUpdate() {
      this.show_edit_modal = false;
      this.initForm();
    },
  },
  computed: {
    searchClients() {
        let clients = [];
        if (this.selectedSort === this.sortOptions[0].value) {
            clients = [...this.clients].sort((client1, client2) => client1[this.selectedSort] - client2[this.selectedSort]);
        }
        else {
            clients = [...this.clients].sort((client1, client2) => client1[this.selectedSort]?.localeCompare(client2[this.selectedSort]));
        }
        if (this.selectedSortMethod == 'ascending')
          return clients;
        else if (this.selectedSortMethod == 'descending') {
          return clients.reverse();
        }
    },
    sortedAndSearchClients() {
        return this.searchClients.filter(client => client.phone_number.includes(this.searchClientStr) || client.email.toLowerCase().includes(this.searchClientStr.toLowerCase()))
    }
  },
  async created() {
    await this.fetchClients();
  },
  mounted() {
      if (this.$store.state.session.userType < 1 || !this.$store.state.session.auth) {
        this.$router.push('/');
      }
  },
}
</script>

<style>

</style>