<template>
  <div>
    <NavBar/>
    <b-card no-body>
      <b-tabs card>
        <b-tab title="Сотрудники" active>
          <b-card-text>
            <div class="container">
              <div class="d-flex justify-content-start mb-5">
                <h1>СОТРУДНИКИ</h1>
              </div>
              <alert :message="message" v-if="showMessage"></alert>
                <div class="input-group-sm col-md-3">
                  <input placeholder="Поиск сотрудника" v-model="searchSurname" type="text" class="form-control sm" aria-describedby="inputHelp">
                  <div id="inputHelp" class="form-text">
                    Начните вводить фамилию сотрудника
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
              <table class="table table-hover mt-2">
                <thead>
                  <tr>
                    <th scope="col">Код</th>
                    <th scope="col">Фамилия</th>
                    <th scope="col">Имя</th>
                    <th scope="col">Отчество</th>
                    <th scope="col">Дата окончания исп. срока</th>
                    <th scope="col">Дата трудоустройства</th>
                    <th scope="col">Филиал</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                    <tr v-for="(employee, index) in sortedAndSearchEmployees" :key="index">
                      <td>{{ employee.id }}</td>
                      <td>{{ employee.surname }}</td>
                      <td>{{ employee.name }}</td>
                      <td>{{ employee.patronymic }}</td>
                      <td>{{ employee.date_test_end }}</td>
                      <td>{{ employee.date_employment }}</td>
                      <td>{{ getBranchName(employee.branch_id) }}</td>
                      <td>
                        <button
                          type="button"
                          class="btn btn-warning btn-sm me-3"
                          @click="editEmployee(employee)">
                            Изменить
                        </button>
                        <button
                          type="button"
                          class="btn btn-danger btn-sm"
                          @click="onDeleteEmployee(employee)">
                            Удалить
                        </button>
                      </td>
                    </tr>
                </tbody>
              </table>
              <div class="d-md-flex justify-content-md-end me-5 pb-3 pt-2">
                <button type="button" @click="show_add_modal=true" style="margin-right: 9px" class="btn btn-success btn-sm">Добавить сотрудника</button>
              </div>
              <b-modal
                  centered
                  title="Добавление сотрудника"
                  v-model="show_add_modal"
                  @hide="onReset"
                  hide-footer>
                <b-form @submit="onSubmit" @reset="onReset" class="w-100">
                  <b-form-group id="form-surname-group"
                              label="Фамилия:"
                              label-for="form-surname-input">
                    <b-form-input id="form-surname-input"
                                  type="text"
                                  v-model="addEmployeeForm.surname"
                                  required
                                  placeholder="Введите фамилию">
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="form-name-group"
                              label="Имя:"
                              label-for="form-name-input">
                    <b-form-input id="form-name-input"
                                  type="text"
                                  v-model="addEmployeeForm.name"
                                  required
                                  placeholder="Введите имя">
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="form-patronymic-group"
                              label="Отчество:"
                              label-for="form-patronymic-input">
                    <b-form-input id="form-patronymic-input"
                                  type="text"
                                  v-model="addEmployeeForm.patronymic"
                                  required
                                  placeholder="Введите отчество">
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="form-date-probation-group"
                              label="Дата окончания исп. срока:"
                              label-for="form-date-probation-input">
                    <b-form-input id="form-date-probation-input"
                                  type="date"
                                  v-model="addEmployeeForm.date_test_end"
                                  placeholder="Выберите дату">
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="form-date-employment-group"
                              label="Дата трудоустройства:"
                              label-for="form-date-employment-input">
                    <b-form-input id="form-date-employment-input"
                                  type="date"
                                  v-model="addEmployeeForm.date_employment"
                                  required
                                  placeholder="Выберите дату">
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="form-branch-group"
                              label="Филиал:"
                              label-for="form-branch-input"
                  >
                    <b-form-select v-model="selected_branch" required>
                      <option
                        v-for="(option, idx) in branch_options"
                        :key="idx"
                        :value="option.value"
                      >
                        {{ option.text }}
                      </option>
                    </b-form-select>
                  </b-form-group>
                  <b-button class="me-3" type="submit" variant="primary">Добавить</b-button>
                  <b-button type="reset" variant="danger">Отмена</b-button>
                </b-form>
              </b-modal>

              <b-modal ref="editEmployeeModal"
                  id="edit-employee-modal"
                  title="Изменить сотрудника"
                  v-model="show_edit_modal"
                  centered
                  hide-footer>
                <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
                  <b-form-group id="form-surname-group"
                              label="Фамилия:"
                              label-for="form-surname-input">
                    <b-form-input id="form-surname-input"
                                  type="text"
                                  v-model="editEmployeeForm.surname"
                                  required
                                  placeholder="Введите фамилию">
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="form-name-group"
                              label="Имя:"
                              label-for="form-name-input">
                    <b-form-input id="form-name-input"
                                  type="text"
                                  v-model="editEmployeeForm.name"
                                  required
                                  placeholder="Введите имя">
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="form-patronymic-group"
                              label="Отчество:"
                              label-for="form-patronymic-input">
                    <b-form-input id="form-patronymic-input"
                                  type="text"
                                  v-model="editEmployeeForm.patronymic"
                                  required
                                  placeholder="Введите отчество">
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="form-date-probation-group"
                              label="Дата окончания исп. срока:"
                              label-for="form-date-probation-input">
                    <b-form-input id="form-date-probation-input"
                                  type="date"
                                  v-model="editEmployeeForm.date_test_end"
                                  placeholder="Выберите дату">
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="form-date-employment-group"
                              label="Дата трудоустройства:"
                              label-for="form-date-employment-input">
                    <b-form-input id="form-date-employment-input"
                                  type="date"
                                  v-model="editEmployeeForm.date_employment"
                                  required
                                  placeholder="Выберите дату">
                    </b-form-input>
                  </b-form-group>
                  <b-form-group id="form-branch-group"
                              label="Филиал:"
                              label-for="form-branch-input"
                  >
                    <b-form-select v-model="selected_branch" required>
                      <option
                        v-for="(option, idx) in branch_options"
                        :key="idx"
                        :value="option.value"
                      >
                        {{ option.text }}
                      </option>
                    </b-form-select>
                  </b-form-group>
                  <b-button class="me-3" type="submit" variant="primary">Сохранить</b-button>
                  <b-button type="reset" variant="danger">Отмена</b-button>
                </b-form>
              </b-modal>
            </div>
          </b-card-text>
        </b-tab>
        <b-tab title="Диспетчеры">
          <b-card-text>
            <div class="container">
              <div class="d-flex justify-content-start mt-1 mb-5">
                <h1>ДИСПЕТЧЕРЫ</h1>
              </div>
              <alert :message="message" v-if="showMessage"></alert>
              <div class="input-group-sm col-md-3">
                <input placeholder="Поиск диспетчера" v-model="searchDispetcherSurname" type="text" class="form-control sm" aria-describedby="inputHelp">
                <div id="inputHelp" class="form-text">
                  Начните вводить фамилию диспетчера
                </div>
              </div>
              <div class="d-md-flex justify-content-md-end me-5 pb-3 pt-2">
                  <my-select
                    v-model="selectedSortDispetchers"
                    :options="sortOptionsDispetchers"
                  />
                  <my-select
                    v-model="selectedSortDispetchersMethod"
                    :options="sortMethodDispetchersOptions"
                    style="margin-left: 20px"
                  />
              </div>
              <table class="table table-hover mt-4">
                <thead>
                  <tr>
                    <th scope="col">Код</th>
                    <th scope="col">Фамилия</th>
                    <th scope="col">Имя</th>
                    <th scope="col">Отчество</th>
                    <th scope="col">Филиал</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(dispetcher, index) in sortedAndSearchDispetcher" :key="index">
                    <td>{{ dispetcher.id }}</td>
                    <td>{{ dispetcher.surname }}</td>
                    <td>{{ dispetcher.name }}</td>
                    <td>{{ dispetcher.patronymic }}</td>
                    <td>{{ getBranchName(dispetcher.branch_id) }}</td>
                    <td>
                      <button
                        type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeleteDispetcher(dispetcher.id)">
                          Удалить
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div class="d-md-flex justify-content-md-end me-5 pb-3 pt-2">
                <button type="button" @click="show_add_dispetcher_modal=true" style="margin-right: 90px" class="btn btn-success btn-sm">Добавить диспетчера</button>
              </div>
              <b-modal
                  centered
                  title="Добавление диспетчера"
                  v-model="show_add_dispetcher_modal"
                  hide-footer>
                <b-form @submit="onAddDispetcherSubmit" @reset="onAddDispetcherReset" class="w-100">
                  <b-form-group>
                    Выберите сотрудника
                    <b-form-select style="margin-top: 15px" v-model="selected_employee" required>
                      <option
                        v-for="(employe, idx) in getEpmloyeesNotPosition()"
                        :key="idx"
                        :value="employe.id"
                      >
                        {{ 'ID: ' + employe.id + ' | ' + employe.surname + ' ' + employe.name + ' ' + employe.patronymic }}
                      </option>      
                    </b-form-select>
                  </b-form-group>
                  <b-button class="me-3" type="submit" variant="primary">Добавить</b-button>
                  <b-button type="reset" variant="danger">Отмена</b-button>
                </b-form>
              </b-modal>
            </div>
          </b-card-text>
        </b-tab>
        <b-tab title="Пилоты">
          <b-card-text>
            <div class="container">
              <div class="d-flex justify-content-start mt-1 mb-5">
                <h1>ПИЛОТЫ</h1>
              </div>
              <alert :message="message" v-if="showMessage"></alert>
              <div class="input-group-sm col-md-3">
                <input placeholder="Поиск пилота" v-model="searchPilotSurname" type="text" class="form-control sm" aria-describedby="inputHelp">
                <div id="inputHelp" class="form-text">
                  Начните вводить фамилию пилота
                </div>
              </div>
              <div class="d-md-flex justify-content-md-end me-5 pb-3 pt-2">
                  <my-select
                    v-model="selectedSortPilots"
                    :options="sortOptionsPilots"
                  />
                  <my-select
                    v-model="selectedSortPilotsMethod"
                    :options="sortMethodPilotsOptions"
                    style="margin-left: 20px"
                  />
              </div>
              <table class="table table-hover mt-4">
                <thead>
                  <tr>
                    <th scope="col">Код</th>
                    <th scope="col">Фамилия</th>
                    <th scope="col">Имя</th>
                    <th scope="col">Отчество</th>
                    <th scope="col">Дата продления лицензии</th>
                    <th scope="col">Филиал</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(pilot, index) in sortedAndSearchPilot" :key="index">
                    <td>{{ pilot.id }}</td>
                    <td>{{ pilot.surname }}</td>
                    <td>{{ pilot.name }}</td>
                    <td>{{ pilot.patronymic }}</td>
                    <td>{{ getLicenseRenewalDate(pilot.id) }}</td>
                    <td>{{ getBranchName(pilot.branch_id) }}</td>
                    <td>
                      <button
                        type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeletePilot(pilot.id)">
                          Удалить
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div class="d-md-flex justify-content-md-end me-5 pb-3 pt-2">
                <button type="button" @click="show_add_pilot_modal=true" style="margin-right: 22px" class="btn btn-success btn-sm">Добавить пилота</button>
              </div>
              <b-modal
                  centered
                  title="Добавление пилота"
                  v-model="show_add_pilot_modal"
                  hide-footer>
                <b-form @submit="onAddPilotSubmit" @reset="onAddPilotReset" class="w-100">
                  <b-form-group>
                    Выберите сотрудника
                    <b-form-select style="margin-top: 15px" v-model="selected_employee" required>
                      <option
                        v-for="(employe, idx) in getEpmloyeesNotPosition()"
                        :key="idx"
                        :value="employe.id"
                      >
                        {{ 'ID: ' + employe.id + ' | ' + employe.surname + ' ' + employe.name + ' ' + employe.patronymic }}
                      </option>      
                    </b-form-select>
                  </b-form-group>
                  <b-form-group id="form-date-renewal-licenses-group"
                              label="Дата продления лицензии:"
                              label-for="form-date-employment-input">
                    <b-form-input id="form-date-employment-input"
                                  type="date"
                                  v-model="license_renewal_date"
                                  required
                                  placeholder="Выберите дату">
                    </b-form-input>
                  </b-form-group>
                  <b-button class="me-3" type="submit" variant="primary">Добавить</b-button>
                  <b-button type="reset" variant="danger">Отмена</b-button>
                </b-form>
              </b-modal>
            </div> 
          </b-card-text>
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import mySelect from '../components/mySelect.vue';
import Alert from '../components/Alert.vue';
import axios from 'axios';
import showMessage from '@/mixins/showMessage';

export default {
  mixins: [showMessage],
  components: { NavBar, mySelect, Alert },
  name: 'EmployeesPage',
  data() {
    return {
      dispetchers: [],
      branch_options: [],
      employees_list: [],
      pilots: [],
      selectedSort: 'id',
      selectedSortMethod: 'ascending',
      sortMethodOptions: [
        {value: 'ascending', name: 'По возрастанию'},
        {value: 'descending', name: 'По убыванию'},  
      ],
      selectedSortDispetchersMethod: 'ascending',
      sortMethodDispetchersOptions: [
        {value: 'ascending', name: 'По возрастанию'},
        {value: 'descending', name: 'По убыванию'},  
      ],
      selectedSortPilotsMethod: 'ascending',
      sortMethodPilotsOptions: [
        {value: 'ascending', name: 'По возрастанию'},
        {value: 'descending', name: 'По убыванию'},  
      ],
      searchSurname: '',
      show_add_modal: false,
      show_edit_modal: false,
      show_add_dispetcher_modal: false,
      show_add_pilot_modal: false,
      selected_branch: null,
      license_renewal_date: null,
      selected_employee: null,
      addEmployeeForm: {
        surname: '',
        name: '',
        patronymic: '',
        date_test_end: '',
        date_employment: '',
        branch: null
      },
      editEmployeeForm: {
        id: '',
        surname: '',
        name: '',
        patronymic: '',
        date_test_end: '',
        date_employment: '',
        branch: null
      },
      searchDispetcherSurname: '',
      searchPilotSurname: '',
      sortOptions: [
        {value: 'id', name: 'По коду'},
        {value: 'surname', name: 'По фамилии'},
        {value: 'name', name: 'По имени'},
        {value: 'patronymic', name: 'По отчеству'},
        {value: 'date_probation', name: 'По дате окончания исп. срока'},
        {value: 'date_employment', name: 'По дате трудоустройства'},
        {value: 'branch_id', name: 'По филиалу'},
      ],
      selectedSortDispetchers: 'id',
      sortOptionsDispetchers: [
        {value: 'id', name: 'По коду'},
        {value: 'surname', name: 'По фамилии'},
        {value: 'name', name: 'По имени'},
        {value: 'patronymic', name: 'По отчеству'},
        {value: 'branch_id', name: 'По филиалу'},
      ],
      selectedSortPilots: 'id',
      sortOptionsPilots: [
        {value: 'id', name: 'По коду'},
        {value: 'surname', name: 'По фамилии'},
        {value: 'name', name: 'По имени'},
        {value: 'patronymic', name: 'По отчеству'},
        {value: 'license_renewal_date', name: 'По дате продления лицензии'},
        {value: 'branch_id', name: 'По филиалу'},
      ]
    }
  },
  methods: {
    async fetchEmployees() {
        try {
            const response = await axios.get('http://127.0.0.1:5000/employees');
            this.employees_list = response.data;
        } catch (e) {
            alert('Возникла ошибка при получении Сотрудников');
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
    async fetchDispetchers() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/dispetchers');
        this.dispetchers = response.data;
      } catch (e) {
        alert('Возникла ошибка при получении Диспетчеров');
      }
    },
    onSubmit(evt) {
      evt.preventDefault();

      if (this.selected_branch == null) {
        return alert('Необходимо выбрать филиал!');
      }

      this.show_add_modal = false;

      const payload = {
        surname: this.addEmployeeForm.surname,
        name: this.addEmployeeForm.name,
        patronymic: this.addEmployeeForm.patronymic,
        date_test_end: this.addEmployeeForm.date_test_end,
        date_employment: this.addEmployeeForm.date_employment,
        branch_id: this.selected_branch
      };

      this.initForm();
      this.addEmployee(payload);
    },
    async addEmployee(employee) {
      try {
          await axios.post('http://127.0.0.1:5000/addEmployee', employee);
          this.showMessageHandle('Сотрудник добавлен');
          this.fetchEmployees();
      } catch (e) {
          alert('Возникла ошибка');
      }
    },
    onReset() {
      this.show_add_modal = false;
      this.initForm();
    },
    initForm() {
      this.addEmployeeForm.surname = '';
      this.addEmployeeForm.name = '';
      this.addEmployeeForm.patronymic = '';
      this.addEmployeeForm.date_test_end = '';
      this.addEmployeeForm.date_employment = '';
      this.addEmployeeForm.branch_code = null;
      this.selected_branch = null;
    },
    getBranchName: function(branch_code) {
      if(this.branch_options.length != 0) {
        return this.branch_options.find(branch => branch.value === branch_code).text;
      }
    },
    getLicenseRenewalDate: function(pilot_id) {
      let employee = this.employees_list.find(employee => employee.id === pilot_id);
      employee.license_renewal_date = this.pilots.find(pilot => pilot.id === pilot_id).license_renewal_date;
      return this.pilots.find(pilot => pilot.id === pilot_id).license_renewal_date;
    },
    editEmployee(employee) {
      this.show_edit_modal = true;
      this.editEmployeeForm = employee;
      this.selected_branch = employee.branch_id;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      
      const payload = {
        surname: this.editEmployeeForm.surname,
        name: this.editEmployeeForm.name,
        patronymic: this.editEmployeeForm.patronymic,
        date_test_end: this.editEmployeeForm.date_test_end,
        date_employment: this.editEmployeeForm.date_employment,
        branch_id: this.selected_branch,
      };
      this.updateEmployee(payload, this.editEmployeeForm.id);

      this.show_edit_modal = false;
      this.selected_branch = null;
    },
    updateEmployee(payload, employeeID) {
      const path = `http://localhost:5000/employees/${employeeID}`;
      axios.put(path, payload)
        .then(() => {
          this.fetchEmployees();
          this.showMessageHandle('Сотрудник успешно изменен');
        })
        .catch((error) => {
          console.error(error);
          alert('Ошибка при изменении сотрудника');
          this.fetchEmployees();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.show_edit_modal = false;
      this.selected_branch = null;
      this.initForm();
    },
    onDeleteEmployee(employee) {
      this.removeEmployee(employee.id);
    },
    removeEmployee(employeeID) {
      const path = `http://localhost:5000/employees/${employeeID}`;
      axios.delete(path)
        .then(() => {
          this.fetchEmployees();
          this.showMessageHandle('Сотрудник удален');
        })
        .catch((error) => {
          console.error(error);
          alert('Ошибка при удалении сотрудника!')
          this.fetchEmployees();
        });
    },
    getEpmloyeesNotPosition: function() {
      return this.employees_list.filter(e => !this.dispetchers.some(j => j.id == e.id) && !this.pilots.some(d => d.id == e.id));
    },
    onAddDispetcherSubmit(evt) {
      evt.preventDefault();
      this.addDispetcher(this.selected_employee);
      this.show_add_dispetcher_modal = false;
      this.selected_employee = null;
    },
    addDispetcher(employeeID) {
      const path = `http://localhost:5000/dispetchers/${employeeID}`
      axios.post(path)
        .then(() => {
          this.fetchDispetchers();
          this.showMessageHandle('Диспетчер добавлен');
        })
        .catch((error) => {
          console.error(error);
          alert('Ошибка при добавлении диспетчера!')
          this.fetchDispetchers();
        });
    },
    onAddDispetcherReset(evt) {
      evt.preventDefault();
      this.show_add_dispetcher_modal = false;
      this.selected_employee = null;  
    },
    onDeleteDispetcher(dispetcherID) {
      this.removeDispetcher(dispetcherID);
    },
    removeDispetcher(dispetcherID) {
      const path = `http://localhost:5000/dispetchers/${dispetcherID}`
      axios.delete(path)
        .then(() => {
          this.showMessageHandle('Диспетчер успешно удален');
          this.fetchDispetchers();
        })
        .catch(() => {
          console.error(error);
          alert('Ошибка при удалении диспетчера!')
          this.fetchDispetchers();
        })
    },
    onAddPilotSubmit(evt) {
      evt.preventDefault();
      this.addPilot(this.selected_employee, this.license_renewal_date);
      this.show_add_pilot_modal = false;
      this.selected_employee = null;
    },
    addPilot(pilotID, license_renewal_date) {
      const path = `http://localhost:5000/pilots/${pilotID}`
      axios.post(path, {'license_renewal_date': license_renewal_date})
        .then(() => {
          this.showMessageHandle('Пилот успешно добавлен');
          this.fetchPilots();
        })
        .catch((error) => {
          console.error(error);
          alert('Ошибка при добавлении пилота!')
          this.fetchPilots();  
        })
    },
    onAddPilotReset(evt) {
      evt.preventDefault();
      this.show_add_pilot_modal = false;
      this.selected_employee = null;  
    },
    onDeletePilot(pilotID) {
      this.removePilot(pilotID);
    },
    removePilot(pilotID) {
      const path = `http://localhost:5000/pilots/${pilotID}`
      axios.delete(path)
        .then(() => {
          this.showMessageHandle('Пилот успешно удален');
          this.fetchPilots();
        })
        .catch((error) => {
          console.error(error);
          alert('Ошибка при удалении пилота!')
          this.fetchPilots();
        })
    },
    async fetchPilots() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/pilots');
        this.pilots = response.data;
      } catch (e) {
        console.log(e);
        alert('Возникла ошибка при получении Пилотов');
      }
    },
  },
  computed: {
    sortedEmployees() {
      let employees = [];
      if (this.selectedSort == this.sortOptions[0].value) {
        employees = [...this.employees_list].sort((employee1, employee2) => employee1[this.selectedSort] - employee2[this.selectedSort]);  
      }
      else {
        employees = [...this.employees_list].sort((employee1, employee2) => employee1[this.selectedSort]?.localeCompare(employee2[this.selectedSort]));
      }
      if (this.selectedSortMethod == 'ascending')
          return employees;
      else if (this.selectedSortMethod == 'descending') {
        return employees.reverse();
      }
    },
    sortedAndSearchEmployees() {
        return this.sortedEmployees.filter(employee => employee.surname.toLowerCase().includes(this.searchSurname.toLowerCase()))
    },
    sortDispetcher() {
      let dispetchers = [];
      if (this.selectedSortDispetchers == this.sortOptionsDispetchers[0].value) {
        dispetchers = [...this.employees_list].filter(e => this.dispetchers.some(j => j.id == e.id)).sort((employee1, employee2) => employee1[this.selectedSortDispetchers] - employee2[this.selectedSortDispetchers]);  
      }
      else {
        dispetchers = [...this.employees_list].filter(e => this.dispetchers.some(j => j.id == e.id)).sort((employee1, employee2) => employee1[this.selectedSortDispetchers]?.localeCompare(employee2[this.selectedSortDispetchers]))
      }
      if (this.selectedSortDispetchersMethod == 'ascending')
          return dispetchers;
      else if (this.selectedSortDispetchersMethod == 'descending') {
        return dispetchers.reverse();
      }
    },
    sortedAndSearchDispetcher() {
        return this.sortDispetcher.filter(dispetcher => dispetcher.surname.toLowerCase().includes(this.searchDispetcherSurname.toLowerCase()))
    },
    sortedPilot() {
      let pilots = [];
      if (this.selectedSortPilots == this.sortOptionsPilots[0].value) {
        pilots = [...this.employees_list].filter(e => this.pilots.some(j => j.id == e.id)).sort((employee1, employee2) => employee1[this.selectedSortPilots] - employee2[this.selectedSortPilots])
      }
      else {
        pilots = [...this.employees_list].filter(e => this.pilots.some(j => j.id == e.id)).sort((employee1, employee2) => employee1[this.selectedSortPilots]?.localeCompare(employee2[this.selectedSortPilots]))
      }
      if (this.selectedSortPilotsMethod == 'ascending')
          return pilots;
      else if (this.selectedSortPilotsMethod == 'descending') {
        return pilots.reverse();
      }
    },
    sortedAndSearchPilot() {
      return this.sortedPilot.filter(pilot => pilot.surname.toLowerCase().includes(this.searchPilotSurname.toLowerCase()))
    },
  },
  async created() {
    await this.fetchBranchOptions();
    await this.fetchEmployees();
    await this.fetchDispetchers();
    await this.fetchPilots();
  },
  mounted() {
    if (this.$store.state.session.userType != 3 || !this.$store.state.session.auth) {
      this.$router.push('/');
    }
  },
}
</script>

<style>
.card-text {
  margin-top: 20px;
}
</style>