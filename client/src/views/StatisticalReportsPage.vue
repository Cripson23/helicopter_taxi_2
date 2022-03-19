<template>
    <div>
        <NavBar/>
        <div class="container">
            <div class="d-flex justify-content-start mt-1">
                <h1>СТАТИСТИЧЕСКИЕ ОТЧЁТЫ</h1>
            </div>
            <b-container class="mt-2 text-center" style="max-width: 20em">
                <b-form @submit="formationReports()">
                    <b-form-group id="form-start-date-group"
                                label="Дата начала периода"
                                label-for="form-start-date-input"
                                label-cols-sm="10"
                                >
                        <b-form-input id="form-start-date-input"
                                type="date"
                                v-model="date_start"
                                required
                                placeholder="Выберите дату">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-end-date-group"
                                label="Дата окончания периода"
                                label-for="form-end-date-input"
                                label-cols-sm="10">
                        <b-form-input id="form-end-date-input"
                                type="date"
                                v-model="date_end"
                                required
                                placeholder="Выберите дату">
                        </b-form-input>
                    </b-form-group>
                    <button
                        type="submit"
                        class="btn btn-success btn-bg mt-2">
                        Сформировать отчёты
                    </button>
                </b-form>
            </b-container>
            <b-container v-show="formation_reports">
                <b-container>
                    <div class="d-flex justify-content-center mt-5 bg-light p-3 rounded-3">
                        <h2>САМЫЙ ВЫГОДНЫЙ ПОСТАВЩИК</h2>
                    </div>
                    <table v-if="providers.length > 0" class="table table-hover mt-4">
                        <thead>
                            <tr>
                                <th scope="col">Код</th>
                                <th scope="col">Наименование</th>
                                <th scope="col">Кол-во закупок</th>
                                <th scope="col">Общий объём закупок</th>
                                <th scope="col">Средняя цена за 1л.</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(provider, idx) in providers" :key="idx">
                                <td>{{ provider.id }}</td>
                                <td>{{ provider.name }}</td>
                                <td>{{ provider.purchase_count }}</td>
                                <td>{{ provider.volume_count }}</td>
                                <td>{{ provider.avg_price }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div v-else class="d-flex justify-content-center mt-2">
                        <h3>Поставки за указанный период времени не найдены</h3>
                    </div>
                </b-container>
                <b-container>
                    <div class="d-flex justify-content-center mt-5 bg-light p-3 rounded-3">
                        <h2>САМЫЙ АКТИВНЫЙ КЛИЕНТ</h2>
                    </div>
                    <table v-if="clients.length > 0" class="table table-hover mt-4">
                        <thead>
                            <tr>
                                <th scope="col">Код</th>
                                <th scope="col">Имя</th>
                                <th scope="col">Номер телефона</th>
                                <th scope="col">Количество заказов</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(client, idx) in clients" :key="idx">
                                <td>{{ client.id }}</td>
                                <td>{{ client.name }}</td>
                                <td>{{ client.phone_number }}</td>
                                <td>{{ client.orders_count }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div v-else class="d-flex justify-content-center mt-2">
                        <h3>Заказы за указанный период времени не найдены</h3>
                    </div>
                </b-container>
                <b-container>
                    <div class="d-flex justify-content-center mt-5 bg-light p-3 rounded-3">
                        <h2>САМЫЙ АКТИВНЫЙ ПИЛОТ</h2>
                    </div>
                    <table v-if="pilots.length > 0" class="table table-hover mt-4">
                        <thead>
                            <tr>
                                <th scope="col">Код</th>
                                <th scope="col">Фамилия</th>
                                <th scope="col">Имя</th>
                                <th scope="col">Количество заказов</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(pilot, idx) in pilots" :key="idx">
                                <td>{{ pilot.id }}</td>
                                <td>{{ pilot.surname }}</td>
                                <td>{{ pilot.name }}</td>
                                <td>{{ pilot.orders_count }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div v-else class="d-flex justify-content-center mt-2">
                        <h3>Заказы за указанный период времени не найдены</h3>
                    </div>
                </b-container>
                <b-container class="mb-5">
                    <div class="d-flex justify-content-center mt-5 bg-light p-3 rounded-3">
                        <h2>САМЫЙ АКТИВНЫЙ ДИСПЕТЧЕР</h2>
                    </div>
                    <table v-if="dispetchers.length > 0" class="table table-hover mt-4">
                        <thead>
                            <tr>
                                <th scope="col">Код</th>
                                <th scope="col">Фамилия</th>
                                <th scope="col">Имя</th>
                                <th scope="col">Количество заказов</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(dispetcher, idx) in dispetchers" :key="idx">
                                <td>{{ dispetcher.id }}</td>
                                <td>{{ dispetcher.surname }}</td>
                                <td>{{ dispetcher.name }}</td>
                                <td>{{ dispetcher.orders_count }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div v-else class="d-flex justify-content-center mt-2">
                        <h3>Заказы за указанный период времени не найдены</h3>
                    </div>
                </b-container>
            </b-container>
            
        </div>
    </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import axios from 'axios';

export default {
    components: { NavBar },
    data() {
        return {
            providers: [],
            clients: [],
            pilots: [],
            dispetchers: [],
            date_end: null,
            date_start: null,
            formation_reports: false,
        }
    },
    methods: {
        async fetchProvidersProfitable(payload) {
            const path = `http://localhost:5000/providers/most-profitable`;
            axios.post(path, payload)
            .then((response) => {
                this.providers = response.data;
            })
            .catch((err) => {
                console.log(err);
                alert('Ошибка при загрузке поставщиков');
            })
        },
        async fetchClientsActive(payload) {
            const path = `http://localhost:5000/clients/most-active`;
            axios.post(path, payload)
            .then((response) => {
                this.clients = response.data;
            })
            .catch((err) => {
                console.log(err);
                alert('Ошибка при загрузке клиентов');
            })
        },
        async fetchPilotsActive(payload) {
            const path = `http://localhost:5000/pilots/most-active`;
            axios.post(path, payload)
            .then((response) => {
                this.pilots = response.data;
            })
            .catch((err) => {
                console.log(err);
                alert('Ошибка при загрузке пилотов');
            })
        },
        async fetchDispetchersActive(payload) {
            const path = `http://localhost:5000/dispetchers/most-active`;
            axios.post(path, payload)
            .then((response) => {
                this.dispetchers = response.data;
            })
            .catch((err) => {
                console.log(err);
                alert('Ошибка при загрузке диспетчеров');
            })
        },
        formationReports() {
            if (this.date_start > this.date_end) {
                return alert('Дата начала периода не должна быть позднее даты окончания!');
            }
            const payload = {
                'date_start': this.date_start,
                'date_end': this.date_end,
            }
            this.fetchProvidersProfitable(payload);
            setTimeout(() => { this.fetchClientsActive(payload) }, 100);
            setTimeout(() => { this.fetchPilotsActive(payload) }, 500);
            setTimeout(() => { this.fetchDispetchersActive(payload) }, 1000);
            this.formation_reports = true;
        },
    },
    mounted() {
        if (this.$store.state.session.userType != 3 || !this.$store.state.session.auth) {
            this.$router.push('/');
        }
    },
}
</script>

<style>
    h2 {
        color: rgb(80, 80, 80)
    }
    h3 {
        color:indianred
    }
</style>