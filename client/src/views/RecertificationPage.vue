<template>
  <div>
    <NavBar/>
    <div class="container">
        <div class="d-flex justify-content-start mt-1 mb-5">
            <h1>АТТЕСТАЦИЯ ПИЛОТОВ</h1>
        </div>
        <alert :message="message" v-if="showMessage"></alert>
        <div class="input-group-sm col-md-3">
            <input placeholder="Поиск аттестаций" v-model="searchRecertPilotSurname" type="text" class="form-control sm" aria-describedby="inputHelp">
            <div id="inputHelp" class="form-text">
                Начните вводить фамилию пилота
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
                <th scope="col">Код пилота</th>
                <th scope="col">Фамилия</th>
                <th scope="col">Имя</th>
                <th scope="col">Отчество</th>
                <th scope="col">Дата аттестации</th>
                <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(recert, index) in sortedAndSearchRecerts" :key="index">
                <td>{{ recert.pilot_id }}</td>
                <td>{{ recert.surname }}</td>
                <td>{{ recert.name }}</td>
                <td>{{ recert.patronymic }}</td>
                <td>{{ recert.recert_date }}</td>
                <td>
                    <button
                        type="button"
                        class="btn btn-warning btn-sm me-3"
                        @click="onEditRecert(recert)">
                        Изменить
                    </button>
                    <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="onDeleteRecert(recert)">
                        Удалить
                    </button>
                </td>
                </tr>
            </tbody>
        </table>
        <div class="d-md-flex justify-content-md-end me-5 pb-3 pt-2">
            <button type="button" @click="show_add_recert_modal=true" style="margin-right: 22px" class="btn btn-success btn-sm">Добавить аттестацию</button>
        </div>
        <b-modal
            centered
            title="Добавление аттестации"
            v-model="show_add_recert_modal"
            hide-footer>
            <b-form @submit="onAddRecertSubmit" @reset="onAddRecertReset" class="w-100">
                <b-form-group>
                Выберите пилота
                <b-form-select style="margin-top: 15px" v-model="selected_pilot" required>
                  <option
                    v-for="(pilot, idx) in pilots"
                    :key="idx"
                    :value="pilot.id"
                    >
                    {{ 'ID: ' + pilot.id + ' | ' + pilot.surname + ' ' + pilot.name + ' ' + pilot.patronymic }}
                  </option>      
                </b-form-select>
                </b-form-group>
                <b-form-group id="form-date-recert-group"
                            label="Дата аттестации:"
                            label-for="form-date-recert-input">
                <b-form-input id="form-date-recert-input"
                                type="date"
                                v-model="recert_date"
                                required
                                placeholder="Выберите дату">
                </b-form-input>
                </b-form-group>
                <b-button class="me-3" type="submit" variant="primary">Добавить</b-button>
                <b-button type="reset" variant="danger">Отмена</b-button>
            </b-form>
        </b-modal>
        <b-modal
            title="Изменить аттестацию"
            v-model="show_edit_modal"
            centered
            @hide="onResetUpdate"
            hide-footer>
            <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
                <b-form-group id="form-branch-group"
                            label="Пилот:"
                            label-for="form-branch-input"
                >
                    <b-form-select v-model="selected_pilot" required>
                        <option
                        v-for="(pilot, idx) in pilots"
                        :key="idx"
                        :value="pilot.id"
                        >
                        {{ "ID: " + pilot.id + " | " + pilot.surname + " " + pilot.name + " " + pilot.patronymic }}
                        </option>
                    </b-form-select>
                </b-form-group>
                <b-form-group id="form-date-recert-group"
                            label="Дата аттестации:"
                            label-for="form-date-recert-input">
                    <b-form-input id="form-date-recert-input"
                                    type="date"
                                    v-model="recert_date"
                                    required
                                    placeholder="Выберите дату">
                    </b-form-input>
                </b-form-group>
                <b-button class="me-3" type="submit" variant="primary">Сохранить</b-button>
                <b-button type="reset" variant="danger">Отмена</b-button>
            </b-form>
        </b-modal>
        <div class="d-flex justify-content-start mt-4 mb-4">
            <h2>ДАТА ПЕРЕАТТЕТСТАЦИИ ПИЛОТА</h2>
        </div>
        <b-form @submit="getRecertDate(selected_recert_pilot)" class="w-100 mb-3">
            <b-form-group>
            Выберите пилота
                <b-form-select class="w-25" style="margin-top: 15px" v-model="selected_recert_pilot" required >
                    <option
                    v-for="(pilot, idx) in pilots"
                    :key="idx"
                    :value="pilot.id"
                    >
                    {{ 'ID: ' + pilot.id + ' | ' + pilot.surname + ' ' + pilot.name + ' ' + pilot.patronymic }}
                    </option>      
                </b-form-select>
            </b-form-group>
            <b-button class="mb-5" type="submit" variant="primary">Получить дату</b-button>
        </b-form>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import Alert from '../components/Alert.vue';
import mySelect from '@/components/mySelect.vue';
import axios from 'axios';
import showMessage from '@/mixins/showMessage';

export default {
    mixins: [showMessage],
    components: { NavBar, Alert, mySelect },
    name: 'Recertification',
    data() {
      return {
        message: '',
        showMessage: false,
        searchRecertPilotSurname: '',
        show_add_recert_modal: false,
        selected_pilot: null,
        selected_recert_pilot: null,
        date_recert_selected_pilot: null,
        recert_date: null,
        recerts: [],
        pilots: [],
        show_edit_modal: false,
        last_pilot: null,
        last_recert_date: null,
        selectedSort: 'pilot_id',
        sortOptions: [
            {value: 'pilot_id', name: 'По коду'},
            {value: 'surname', name: 'По фамилии'},
            {value: 'name', name: 'По имени'},
            {value: 'patronymic', name: 'По отчеству'},
            {value: 'recert_date', name: 'По дате аттестации'},
        ],
        selectedSortMethod: 'ascending',
        sortMethodOptions: [
            {value: 'ascending', name: 'По возрастанию'},
            {value: 'descending', name: 'По убыванию'},  
        ],
      }
    },
    methods: {
        async fetchRecert() {
            const path = `http://localhost:5000/recertifications`
            axios.get(path)
            .then((response) => {
                this.recerts = response.data;
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при загрузке аттестаций');
            })
        },
        async fetchPilots() {
            const path = `http://localhost:5000/getPilots`
            axios.get(path)
            .then((response) => {
                this.pilots = response.data;
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при загрузке пилотов');
            })
        },
        onAddRecertSubmit(evt) {
            evt.preventDefault();
            this.addRecert(this.selected_pilot, this.recert_date);
            this.show_add_recert_modal = false;
            this.selected_pilot = null;
            this.recert_date = null;
        },
        addRecert(pilotID, recertDate) {
            const path = `http://localhost:5000/recertifications`
            axios.post(path, {'pilot_id': pilotID, 'recert_date': recertDate})
            .then(() => {
                this.fetchRecert();
                this.showMessageHandle('Аттестация успешно добавлена');
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при добавлении аттестации');
            })
        },
        onAddRecertReset(evt) {
            evt.preventDefault();
            this.selected_pilot = null;
            this.recert_date = null;
            this.show_add_recert_modal = false;
        },
        onDeleteRecert(recert) {
            this.removeRecert(recert.pilot_id, recert.recert_date);
        },
        removeRecert(recertID, recertDate) {
            const path = `http://localhost:5000/deleteRecert`;
            axios.post(path, {'id': recertID, 'recert_date': recertDate})
            .then(() => {
                this.fetchRecert();
                this.showMessageHandle('Аттестация успешно удалена');
            })
            .catch((error) => {
                console.error(error);
                alert('Ошибка при удалении аттестации!')
                this.fetchRecert();
            })
        },
        onEditRecert(recert) {
            this.show_edit_modal = true;
            this.selected_pilot = recert.pilot_id;
            this.recert_date = recert.recert_date;
            this.last_pilot = recert.pilot_id;
            this.last_recert_date = recert.recert_date;
        },
        onSubmitUpdate(evt) {
            evt.preventDefault();
            if (this.last_pilot === this.selected_pilot && this.last_recert_date === this.recert_date) {
                return alert('Вы не изменили данные!');
            }
            this.updateRecent(this.last_pilot, this.last_recert_date, this.selected_pilot, this.recert_date);
            this.show_edit_modal = false;
            this.selected_pilot = null;
            this.recert_date = null;
        },
        updateRecent(lastPilotID, lastRecertDate, pilotID, recertDate) {
            const path = `http://localhost:5000/recertifications`
            axios.put(path, {'last_pilot_id': lastPilotID, 'last_recert_date': lastRecertDate, 'pilot_id': pilotID, 'recert_date': recertDate})
            .then(() => {
                this.fetchRecert();
                this.showMessageHandle('Аттестация успешно изменена');
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при изменении аттестации!');
            })
        },
        onResetUpdate() {
            this.show_edit_modal = false;
            this.selected_pilot = null;
            this.recert_date = null;
        },
        getRecertDate(pilotID) {
            const path = `http://localhost:5000/recertifications/date/${pilotID}`
            axios.get(path)
            .then((res) => {
                alert('Дата следующей переаттестации: ' + res.data.date);
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при получении даты переаттестации!');
            })
        }
    },
    computed: {
        sortRecerts() {
            let recerts = [];
            if (this.selectedSort === this.sortOptions[0].value) {
                recerts = [...this.recerts].sort((recert1, recert2) => recert1[this.selectedSort] - recert2[this.selectedSort]);
            }
            else {
                recerts = [...this.recerts].sort((recert1, recert2) => recert1[this.selectedSort]?.localeCompare(recert2[this.selectedSort]));
            }
            if (this.selectedSortMethod == 'ascending')
                return recerts;
            else if (this.selectedSortMethod == 'descending') {
                return recerts.reverse();
            }
        },
        sortedAndSearchRecerts() {
            return this.sortRecerts.filter(recert => recert.surname.toLowerCase().includes(this.searchRecertPilotSurname.toLowerCase()))
        }
    },
    async created() {
        await this.fetchRecert();
        await this.fetchPilots();
    },
    mounted() {
        if (this.$store.state.session.userType < 3 || !this.$store.state.session.auth) {
            this.$router.push('/');
        }
    },
}
</script>

<style>
    .container {
        padding-top: 30px;
    }
</style>