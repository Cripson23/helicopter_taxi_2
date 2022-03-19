<template>
    <div>
        <NavBar/>
        <div class="container">
            <div class="d-flex justify-content-start mt-1">
                <h1>ОТЧЁТНАЯ ДОКУМЕНТАЦИЯ</h1>
            </div>
            <b-container class="mt-2 text-center" style="max-width: 20em">
                <b-form @submit="formationDocuments()">
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
                        Сформировать документацию
                    </button>
                </b-form>
            </b-container>
            <b-container v-show="formation_documents">
                <b-container>
                    <div class="d-flex justify-content-center mt-5 bg-light p-3 rounded-3">
                        <h2>ПРИНЯТО ЗАКАЗОВ КАЖДЫМ ДИСПЕТЧЕРОМ</h2>
                    </div>
                    <table v-if="dispetchers.length > 0" class="table table-hover mt-4">
                        <thead>
                            <tr>
                                <th scope="col">Код</th>
                                <th scope="col">Фамилия</th>
                                <th scope="col">Имя</th>
                                <th scope="col">Количество принятых заказов</th>
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
                <b-container>
                    <div class="d-flex justify-content-center mt-5 bg-light p-3 rounded-3">
                        <h2>ВЫПОЛНЕНО ЗАКАЗОВ КАЖДЫМ ПИЛОТОМ</h2>
                    </div>
                    <table v-if="pilots.length > 0" class="table table-hover mt-4">
                        <thead>
                            <tr>
                                <th scope="col">Код</th>
                                <th scope="col">Фамилия</th>
                                <th scope="col">Имя</th>
                                <th scope="col">Количество выполненых заказов</th>
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
                <b-container>
                    <div class="d-flex justify-content-center mt-5 bg-light p-3 rounded-3">
                        <h2>ВЫПОЛНЕНО ЗАКАЗОВ НА КАЖДОМ ВЕРТОЛЕТЕ</h2>
                    </div>
                    <table v-if="helicopters.length > 0" class="table table-hover mt-4">
                        <thead>
                            <tr>
                                <th scope="col">Код вертолета</th>
                                <th scope="col">Наименование модели</th>
                                <th scope="col">Количество заказов</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(helicopter, idx) in helicopters" :key="idx">
                                <td>{{ helicopter.id }}</td>
                                <td>{{ helicopter.model_name }}</td>
                                <td>{{ helicopter.orders_count }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div v-else class="d-flex justify-content-center mt-2">
                        <h3>Заказы за указанный период времени не найдены</h3>
                    </div>
                </b-container>
                <b-container class="mb-5">
                    <div class="d-flex justify-content-center mt-5 bg-light p-3 rounded-3">
                        <h2>ЗАТРАТЫ НА ЗАКУПКУ ТОПЛИВА</h2>
                    </div>
                    <table v-if="purchase_cost.length > 0" class="table table-hover mt-4">
                        <thead>
                            <tr>
                                <th scope="col">Общие затраты (руб.)</th>
                                <th scope="col">Общий объём закупки (л.)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(purchase, idx) in purchase_cost" :key="idx">
                                <td>{{ purchase.cost }}</td>
                                <td>{{ purchase.volume }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div v-else class="d-flex justify-content-center mt-2">
                        <h3>Затраты за указанный период времени не найдены</h3>
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
            purchase_cost: [],
            helicopters: [],
            pilots: [],
            dispetchers: [],
            date_end: null,
            date_start: null,
            formation_documents: false,
        }
    },
    methods: {
        async fetchDispetchersCountOrders(payload) {
            const path = `http://localhost:5000/dispetchers/count-orders`;
            axios.post(path, payload)
            .then((response) => {
                this.dispetchers = response.data;
            })
            .catch((err) => {
                console.log(err);
                alert('Ошибка при загрузке заказов диспетчеров');
            })
        },
        async fetchPilotsCountOrders(payload) {
            const path = `http://localhost:5000/pilots/count-orders`;
            axios.post(path, payload)
            .then((response) => {
                this.pilots = response.data;
            })
            .catch((err) => {
                console.log(err);
                alert('Ошибка при загрузке заказов пилотов');
            })
        },
        async fetchHelicoptersCountOrders(payload) {
            const path = `http://localhost:5000/helicopters/count-orders`;
            axios.post(path, payload)
            .then((response) => {
                this.helicopters = response.data;
            })
            .catch((err) => {
                console.log(err);
                alert('Ошибка при загрузке заказов вертолетов');
            })
        },
        async fetchPurchaseCost(payload) {
            const path = `http://localhost:5000/purchases/cost`;
            axios.post(path, payload)
            .then((response) => {
                this.purchase_cost = response.data;
            })
            .catch((err) => {
                console.log(err);
                alert('Ошибка при загрузке затрат на закупку топлива');
            })
        },
        formationDocuments() {
            if (this.date_start > this.date_end) {
                return alert('Дата начала периода не должна быть позднее даты окончания!');
            }
            const payload = {
                'date_start': this.date_start,
                'date_end': this.date_end,
            }
            this.fetchDispetchersCountOrders(payload);
            setTimeout(() => { this.fetchPilotsCountOrders(payload) }, 100);
            setTimeout(() => { this.fetchHelicoptersCountOrders(payload) }, 500);
            setTimeout(() => { this.fetchPurchaseCost(payload) }, 1000);
            this.formation_documents = true;
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