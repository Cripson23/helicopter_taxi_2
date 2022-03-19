<template>
  <div>
    <NavBar/>
    <div class="container">
        <div class="d-flex justify-content-start mt-1 mb-5">
            <h1>ЗАКАЗЫ</h1>
        </div>
        <div id="loading" v-show="printLoading"></div>
        <alert :message="message" v-if="showMessage"></alert>
        <div class="input-group-sm col-md-3">
            <input placeholder="Поиск заказов клиента" v-model="searchOrderClientStr" type="text" class="form-control sm" aria-describedby="inputHelp">
            <div class="form-text">
                Начните вводить номер телефона или почту клиента
            </div>
        </div>
        <div class="d-md-flex justify-content-md-end me-3 pb-3 pt-2">
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
                <th scope="col">Клиент</th>
                <th scope="col">Адрес заказа</th>
                <th scope="col">Адрес доставки</th>
                <th scope="col">Дата поступления</th>
                <th scope="col">Дата выполнения</th>
                <th scope="col">Время аренды</th>
                <th scope="col">Способ оплаты</th>
                <th scope="col">Филиал</th>
                <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(order, index) in sortedAndSearchOrders" :key="index">
                    <td>{{ order.id }}</td>
                    <td>{{ getClientPhoneEmail(order.client_id) }}</td>
                    <td>{{ order.order_address }}</td>
                    <td>{{ order.delivery_address }}</td>
                    <td>{{ order.date_completion }}</td>
                    <td>{{ order.date_receipt }}</td>
                    <td>{{ order.rental_time }}</td>
                    <td>{{ order.payment_method }}</td>
                    <td>{{ getBranchName(order.branch_id) }}</td>
                    <td v-if="this.$store.state.session.userType != 2">
                    <button
                        type="button"
                        class="btn btn-success btn-sm me-3"
                        @click="showAllInfo(order)"
                        >
                        Подробнее
                    </button>    
                    <button
                        type="button"
                        class="btn btn-warning btn-sm me-3"
                        style="margin-top: 16px;"
                        @click="onChangeOrder(order)"
                        >
                        Изменить
                    </button>
                    <button
                        type="button"
                        class="btn btn-danger btn-sm"
                        style="margin-top: 16px; margin-right: 10px"
                        @click="onDeleteOrder(order.id)"
                        >
                        Удалить
                    </button>
                    <button 
                        type="button"
                        class="btn btn-primary btn-sm mt-3"
                        v-print="printObj"
                        @click="printReceipt(order)">
                        Печать квитанции
                    </button>
                    </td>
                </tr>
            </tbody>
        </table>
        <div v-if="this.$store.state.session.userType != 2" class="d-md-flex justify-content-md-end me-5 mb-4 pb-3 pt-2">
            <button type="button" @click="show_add_modal=true" class="btn btn-success btn-bg">Добавить заказ</button>    
        </div>
        <b-modal
            centered
            title="Добавление заказа"
            v-model="show_add_modal"
            @hide="onReset"
            hide-footer>
            <b-form @submit="onSubmit" @reset="onReset" class="w-100">
                <div class="row">
                    <div class="col-md-6">
                        <b-form-group id="form-dispetcher-group"
                                    label="Диспетчер:"
                                    label-for="form-dispetcher-input"
                        >
                            <b-form-select v-model="formData.selected_dispetcher" required>
                                <option
                                v-for="(dispetcher, idx) in dispetchers"
                                :key="idx"
                                :value="dispetcher.id"
                                >
                                {{ getEmployeeInfo(dispetcher.id) }}
                                </option>
                            </b-form-select>
                        </b-form-group>
                        <b-form-group id="form-pilot-group"
                                    label="Пилот:"
                                    label-for="form-pilot-input"
                        >
                            <b-form-select v-model="formData.selected_pilot" required>
                                <option
                                v-for="(pilot, idx) in pilots"
                                :key="idx"
                                :value="pilot.id"
                                >
                                {{ getEmployeeInfo(pilot.id) }}
                                </option>
                            </b-form-select>
                        </b-form-group>
                        <b-form-group id="form-client-group"
                                    label="Клиент:"
                                    label-for="form-client-input"
                        >
                            <b-form-select v-model="formData.selected_client" required>
                                <option
                                v-for="(client, idx) in clients"
                                :key="idx"
                                :value="client.client_id"
                                >
                                {{ getClientPhoneEmail(client.client_id) + ' | ' + getClientFIO(client.client_id) }}
                                </option>
                            </b-form-select>
                        </b-form-group>
                        <b-form-group id="form-helicopter-group"
                                    label="Вертолет:"
                                    label-for="form-helicopter-input"
                        >
                            <b-form-select v-if="helicopter_models.length > 0" v-model="formData.selected_helicopter" required>
                                <option
                                v-for="(helicopter, idx) in helicopters"
                                :key="idx"
                                :value="helicopter.id"
                                >
                                {{ getHelicopterInfo(helicopter.id) }}
                                </option>
                            </b-form-select>
                        </b-form-group>
                        <b-form-group id="form-order-address-group"
                                    label="Адрес заказа:"
                                    label-for="form-order-address-input">
                            <b-form-input id="form-order-address-input"
                                            type="text"
                                            v-model="formData.order_address"
                                            required
                                            placeholder="Введите адрес заказа">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-delivery-address-group"
                                    label="Адрес доставки:"
                                    label-for="form-delivery-address-input">
                            <b-form-input id="form-delivery-address-input"
                                            type="text"
                                            v-model="formData.delivery_address"
                                            required
                                            placeholder="Введите адрес доставки">
                            </b-form-input>
                        </b-form-group>
                    </div>
                    <div class="col-md-6">
                        <b-form-group id="form-date-receipt-group"
                                    label="Дата поступления:"
                                    label-for="form-date-receipt-input">
                            <b-form-input id="form-date-receipt-input"
                                            type="date"
                                            v-model="formData.date_receipt"
                                            required
                                            placeholder="Выберите дату">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-date-completion-group"
                                    label="Дата выполнения:"
                                    label-for="form-date-completion-input">
                            <b-form-input id="form-date-completion-input"
                                            type="date"
                                            v-model="formData.date_completion"
                                            required
                                            placeholder="Выберите дату">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-rental-time-group"
                                    label="Время аренды (в часах):"
                                    label-for="form-rental-time-input">
                            <b-form-input id="form-rental-time-input"
                                            type="number"
                                            v-model="formData.rental_time"
                                            required>
                            </b-form-input>
                            <b-form-input id="form-rental-time-input"
                                            type="range"
                                            min="1" 
                                            max="24"
                                            v-model="formData.rental_time"
                                            required>
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-payment-method-group"
                                    label="Способ оплаты:"
                                    label-for="form-payment-method-input"
                        >
                            <b-form-select v-model="formData.payment_method" required>
                                <option
                                value="Наличные"
                                >
                                    Наличные
                                </option>
                                <option
                                value="Безналичный расчет"
                                >
                                    Безналичный расчет
                                </option>
                            </b-form-select>
                        </b-form-group>
                        <b-form-group id="form-branch-group"
                                    label="Филиал:"
                                    label-for="form-branch-input"
                        >
                            <b-form-select v-model="formData.branch_id" required>
                            <option
                                v-for="(option, idx) in branch_options"
                                :key="idx"
                                :value="option.value"
                            >
                                {{ option.text }}
                            </option>
                            </b-form-select>
                        </b-form-group>
                    </div>
                </div>
                <b-button class="me-3" type="submit" variant="primary">Добавить</b-button>
                <b-button type="reset" variant="danger">Отмена</b-button>
            </b-form>
        </b-modal>
        <b-modal
            centered
            title="Изменение заказа"
            v-model="show_edit_modal"
            @hide="onEditReset"
            hide-footer>
            <b-form @submit="onEditSubmit" @reset="onEditReset" class="w-100">
                <div class="row">
                    <div class="col-md-6">
                        <b-form-group id="form-dispetcher-group"
                                    label="Диспетчер:"
                                    label-for="form-dispetcher-input"
                        >
                            <b-form-select v-model="formData.selected_dispetcher" required>
                                <option
                                v-for="(dispetcher, idx) in dispetchers"
                                :key="idx"
                                :value="dispetcher.id"
                                >
                                {{ getEmployeeInfo(dispetcher.id) }}
                                </option>
                            </b-form-select>
                        </b-form-group>
                        <b-form-group id="form-pilot-group"
                                    label="Пилот:"
                                    label-for="form-pilot-input"
                        >
                            <b-form-select v-model="formData.selected_pilot" required>
                                <option
                                v-for="(pilot, idx) in pilots"
                                :key="idx"
                                :value="pilot.id"
                                >
                                {{ getEmployeeInfo(pilot.id) }}
                                </option>
                            </b-form-select>
                        </b-form-group>
                        <b-form-group id="form-client-group"
                                    label="Клиент:"
                                    label-for="form-client-input"
                        >
                            <b-form-select v-model="formData.selected_client" required>
                                <option
                                v-for="(client, idx) in clients"
                                :key="idx"
                                :value="client.client_id"
                                >
                                {{ getClientPhoneEmail(client.client_id) + ' | ' + getClientFIO(client.client_id) }}
                                </option>
                            </b-form-select>
                        </b-form-group>
                        <b-form-group id="form-helicopter-group"
                                    label="Вертолет:"
                                    label-for="form-helicopter-input"
                        >
                            <b-form-select v-if="helicopter_models.length > 0" v-model="formData.selected_helicopter" required>
                                <option
                                v-for="(helicopter, idx) in helicopters"
                                :key="idx"
                                :value="helicopter.id"
                                >
                                {{ getHelicopterInfo(helicopter.id) }}
                                </option>
                            </b-form-select>
                        </b-form-group>
                        <b-form-group id="form-order-address-group"
                                    label="Адрес заказа:"
                                    label-for="form-order-address-input">
                            <b-form-input id="form-order-address-input"
                                            type="text"
                                            v-model="formData.order_address"
                                            required
                                            placeholder="Введите адрес заказа">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-delivery-address-group"
                                    label="Адрес доставки:"
                                    label-for="form-delivery-address-input">
                            <b-form-input id="form-delivery-address-input"
                                            type="text"
                                            v-model="formData.delivery_address"
                                            required
                                            placeholder="Введите адрес доставки">
                            </b-form-input>
                        </b-form-group>
                    </div>
                    <div class="col-md-6">
                        <b-form-group id="form-date-receipt-group"
                                    label="Дата поступления:"
                                    label-for="form-date-receipt-input">
                            <b-form-input id="form-date-receipt-input"
                                            type="date"
                                            v-model="formData.date_receipt"
                                            required
                                            placeholder="Выберите дату">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-date-completion-group"
                                    label="Дата выполнения:"
                                    label-for="form-date-completion-input">
                            <b-form-input id="form-date-completion-input"
                                            type="date"
                                            v-model="formData.date_completion"
                                            required
                                            placeholder="Выберите дату">
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-rental-time-group"
                                    label="Время аренды (в часах):"
                                    label-for="form-rental-time-input">
                            <b-form-input id="form-rental-time-input"
                                            type="number"
                                            v-model="formData.rental_time"
                                            required>
                            </b-form-input>
                            <b-form-input id="form-rental-time-input"
                                            type="range"
                                            min="1" 
                                            max="24"
                                            v-model="formData.rental_time"
                                            required>
                            </b-form-input>
                        </b-form-group>
                        <b-form-group id="form-payment-method-group"
                                    label="Способ оплаты:"
                                    label-for="form-payment-method-input"
                        >
                            <b-form-select v-model="formData.payment_method" required>
                                <option
                                value="Наличные"
                                >
                                    Наличные
                                </option>
                                <option
                                value="Безналичный расчет"
                                >
                                    Безналичный расчет
                                </option>
                            </b-form-select>
                        </b-form-group>
                        <b-form-group id="form-branch-group"
                                    label="Филиал:"
                                    label-for="form-branch-input"
                        >
                            <b-form-select v-model="formData.branch_id" required>
                            <option
                                v-for="(option, idx) in branch_options"
                                :key="idx"
                                :value="option.value"
                            >
                                {{ option.text }}
                            </option>
                            </b-form-select>
                        </b-form-group>
                    </div>
                </div>
                <b-button class="me-3" type="submit" variant="primary">Сохранить</b-button>
                <b-button type="reset" variant="danger">Отмена</b-button>
            </b-form>
        </b-modal>
        <b-modal
            title="Подробная информация о заказе"
            v-model="show_all_info_modal"
            centered
            hide-footer>
            <b-list-group v-if="selected_order != null">
                <b-list-group-item><b>Номер заказа:</b> {{ selected_order.id }}</b-list-group-item>
                <b-list-group-item><b>Диспетчер:</b> {{ getEmployeeInfo(selected_order.dispetcher_id) }}</b-list-group-item>
                <b-list-group-item><b>Пилот:</b> {{ getEmployeeInfo(selected_order.pilot_id) }}</b-list-group-item>
                <b-list-group-item><b>Клиент:</b> {{ getClientPhoneEmail(selected_order.client_id) }}</b-list-group-item>
                <b-list-group-item><b>Вертолет:</b> {{ getHelicopterInfo(selected_order.helicopter_id) }}</b-list-group-item>
                <b-list-group-item><b>Адрес заказа:</b> {{ selected_order.order_address }}</b-list-group-item>
                <b-list-group-item><b>Адрес доставки:</b> {{ selected_order.delivery_address }}</b-list-group-item>
                <b-list-group-item><b>Дата поступления:</b> {{ selected_order.date_completion }}</b-list-group-item>
                <b-list-group-item><b>Дата выполнения:</b> {{ selected_order.date_receipt }}</b-list-group-item>
                <b-list-group-item><b>Время аренды:</b> {{ selected_order.rental_time }}</b-list-group-item>
                <b-list-group-item><b>Итоговая стоимость:</b> {{ getOrderPrice(selected_order) }} рублей</b-list-group-item>
                <b-list-group-item><b>Способ оплаты:</b> {{ selected_order.payment_method }}</b-list-group-item>
                <b-list-group-item><b>Филиал:</b> {{ getBranchName(selected_order.branch_id) }}</b-list-group-item>
            </b-list-group>
        </b-modal>
        <div v-if="selected_order != null" id="printMe" :hidden="onPrint">
            <h1>Квитанция на оплату заказа</h1>
            <table class="table table-hover mt-2">
                <thead>
                <tr>
                    <th scope="col">Адрес заказа</th>
                    <th scope="col">Адрес доставки</th>
                    <th scope="col">Дата поступления</th>
                    <th scope="col">Дата выполнения</th>
                    <th scope="col">Способ оплаты</th>
                </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{{ selected_order.order_address }}</td>
                        <td>{{ selected_order.delivery_address }}</td>
                        <td>{{ selected_order.date_completion }}</td>
                        <td>{{ selected_order.date_receipt }}</td>
                        <td>{{ selected_order.payment_method }}</td>
                    </tr>
                </tbody>
            </table>
            <br><br>Клиент:&nbsp;&nbsp;<b>{{ getClientFIO(selected_order.client_id) }}</b><br>
            Номер телефона: <b>{{ getClientPhone(selected_order.client_id) }}</b><br>
            Сумма к оплате (в рублях):&nbsp;&nbsp;<b>{{ getOrderPrice(selected_order) }}</b>
            <br><br><br><div style="float:right; margin-right: 200px"><b>Подпись клиента:</b></div><br><br><br>
            <div style="float:right; margin-right: 200px"><b>Подпись менеджера:</b></div>
        </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import Alert from '../components/Alert.vue';
import mySelect from '../components/mySelect.vue';
import showMessage from '@/mixins/showMessage';
import axios from 'axios';

export default {
    components: {
        NavBar,
        Alert,
        mySelect
    },
    mixins: [showMessage],
    data() {
        return {
            selected_order: null,
            onPrint: true,
            show_print_receipt: false,
            orders: [],
            dispetchers: [],
            pilots: [],
            employees: [],
            clients: [],
            helicopters: [],
            branch_options: [],
            helicopter_models: [],
            show_all_info_modal: false,
            show_edit_modal: false,
            printLoading: true,
            searchOrderClientStr: '',
            selectedSort: 'id',
            selectedSortMethod: 'ascending',
            sortMethodOptions: [
                {value: 'ascending', name: 'По возрастанию'},
                {value: 'descending', name: 'По убыванию'},  
            ],
            sortOptions: [
                {value: 'id', name: 'По коду'},
                {value: 'date_completion', name: 'По дате выполнения'},
                {value: 'date_receipt', name: 'По дате поступления'},
            ],
            show_add_modal: false,
            formData: {
                order_id: null,
                selected_dispetcher: null,
                selected_pilot: null,
                selected_client: null,
                selected_helicopter: null,
                order_address: null,
                delivery_address: null,
                date_completion: null,
                date_receipt: null,
                rental_time: null,
                payment_method: null,
                branch_id: null,
            },
            printObj: {
                id: "printMe",
                popTitle: 'Квитанция на оплату',
                extraCss: "https://cdn.bootcdn.net/ajax/libs/animate.css/4.1.1/animate.compat.css, https://cdn.bootcdn.net/ajax/libs/hover.css/2.3.1/css/hover-min.css",
                extraHead: '<meta http-equiv="Content-Language"content="ru"/>',
                beforeOpenCallback (vue) {
                    vue.printLoading = true
                },
                openCallback (vue) {
                    vue.printLoading = false
                },
                closeCallback (vue) {
                }
            },
        }
    },
    methods: {
        printReceipt(order) {
            this.selected_order = order;
            this.onPrint = false;
            setTimeout(() => {
                this.onPrint = true;
            }, 100);
        },
        fetchDispetchers() {
            const path = `http://localhost:5000/dispetchers`
            axios.get(path)
            .then((response) => {
                this.dispetchers = response.data;
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при загрузке диспетчеров');
            })
        },
        fetchEmployees() {
            const path = `http://localhost:5000/employees`
            axios.get(path)
            .then((response) => {
                this.employees = response.data;
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при загрузке сотрудников');
            })
        },
        fetchPilots() {
            const path = `http://localhost:5000/pilots`
            axios.get(path)
            .then((response) => {
                this.pilots = response.data;
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при загрузке пилотов');
            })
        },
        fetchClients() {
            const path = `http://localhost:5000/clients`
            axios.get(path)
            .then((response) => {
                this.clients = response.data;
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при загрузке клиентов');
            })
        },
        fetchHelicopters() {
            const path = `http://localhost:5000/helicopters`
            axios.get(path)
            .then((response) => {
                this.helicopters = response.data;
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при загрузке вертолётов');
            })
        },
        fetchOrders() {
            const path = `http://localhost:5000/orders`
            axios.get(path)
            .then((response) => {
                this.orders = response.data;
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при загрузке заказов');
            })
        },
        fetchBranchOptions() {
            const path = `http://127.0.0.1:5000/branchOptions`
            axios.get(path)
            .then((response) => {
                this.branch_options = response.data;
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при загрузке филиалов');
            })
        },
        getBranchName: function(branch_code) {
            if(this.branch_options.length != 0) {
                return this.branch_options.find(branch => branch.value === branch_code).text;
            }
        },
        getClientPhoneEmail(client_id) {
            if (this.clients.length != 0) {
                let client = this.clients.find(client => client.client_id === client_id);
                return 'ID: ' + client.client_id + ' | Номер телефона: ' + client.phone_number + " | Почта: " + client.email;
            }
        },
        getClientPhone(client_id) {
            if (this.clients.length != 0) {
                let client = this.clients.find(client => client.client_id === client_id);
                return client.phone_number;
            }
        },
        getClientFIO(client_id) {
            if (this.clients.length != 0) {
                let client = this.clients.find(client => client.client_id === client_id);
                return client.name + ' ' + client.patronymic;
            }
        },
        getEmployeeInfo(employee_id) {
            const employee = this.employees.find(employee => employee.id === employee_id);
            if (employee != undefined)
                return 'ID: ' + employee.id + ' | ' + employee.surname + ' ' + employee.name + ' ' + employee.patronymic;
        },
        getHelicopterInfo(helicopter_id) {
            const helicopter = this.helicopters.find(helicopter => helicopter.id === helicopter_id);
            if (helicopter != undefined) {
                if (this.helicopter_models != undefined) {
                    const helicopter_model = this.helicopter_models.find(model => model.id === helicopter.model_id);
                    return 'ID: ' + helicopter.id + ' | Модель: ' + helicopter_model.name;
                }
            }
        },
        fetchHelicopterModels() {
            const path = `http://localhost:5000/helicopter-models`;
            axios.get(path)
                .then((response) => {
                    this.helicopter_models = response.data;
                })
                .catch((error) => {
                console.error(error);
                alert('Ошибка при получении информации о модели вертолёта');
            });
        },
        showAllInfo(order) {
            this.show_all_info_modal = true;
            this.selected_order = order;
        },
        getOrderPrice(selected_order) {
            const rent_hourse = selected_order.rental_time;
            const helicopter = this.helicopters.find(helicopter => helicopter.id === selected_order.helicopter_id);
            if (helicopter != undefined) {
                const helicopter_model = this.helicopter_models.find(model => model.id === helicopter.model_id);
                return rent_hourse * helicopter_model.price;
            }
        },
        onReset() {
            this.show_add_modal = false;
            this.formInit();
        },
        onSubmit(evt) {
            evt.preventDefault();

            const payload = {
                'dispetcher_id': this.formData.selected_dispetcher,
                'pilot_id': this.formData.selected_pilot,
                'client_id': this.formData.selected_client,
                'helicopter_id': this.formData.selected_helicopter,
                'order_address': this.formData.order_address,
                'delivery_address': this.formData.delivery_address,
                'date_completion': this.formData.date_completion,
                'date_receipt': this.formData.date_receipt,
                'rental_time': this.formData.rental_time,
                'payment_method': this.formData.payment_method,
                'branch_id': this.formData.branch_id
            };

            this.addOrder(payload);

            this.show_add_modal = false;
            this.formInit();
        },
        addOrder(payload) {
            const path = `http://localhost:5000/orders`
            axios.post(path, payload)
            .then(() => {
                this.fetchOrders();
                this.showMessageHandle('Заказ успешно добавлен');
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при добавлении заказа');
            })
        },
        onDeleteOrder(order_id) {
            this.removeOrder(order_id);
        },
        removeOrder(orderID) {
            const path = `http://localhost:5000/orders/${orderID}`;
            axios.delete(path)
            .then(() => {
                this.fetchOrders();
                this.showMessageHandle('Заказ успешно удален');
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при удаленииз заказа');
            })
        },
        onChangeOrder(order) { 
            this.formData.selected_dispetcher = order.dispetcher_id;
            this.formData.selected_pilot = order.pilot_id;
            this.formData.selected_client = order.client_id;
            this.formData.selected_helicopter = order.helicopter_id;
            this.formData.order_address = order.order_address;
            this.formData.delivery_address = order.delivery_address;
            this.formData.date_completion = order.date_completion;
            this.formData.date_receipt = order.date_receipt;
            this.formData.rental_time = order.rental_time;
            this.formData.payment_method = order.payment_method;
            this.formData.branch_id = order.branch_id;
            this.formData.order_id = order.id;
            this.show_edit_modal = true;
        },
        onEditReset() {
            this.show_edit_modal = false;
            this.formInit();
        },
        onEditSubmit() {
            const payload = {
                'dispetcher_id': this.formData.selected_dispetcher,
                'pilot_id': this.formData.selected_pilot,
                'client_id': this.formData.selected_client,
                'helicopter_id': this.formData.selected_helicopter,
                'order_address': this.formData.order_address,
                'delivery_address': this.formData.delivery_address,
                'date_completion': this.formData.date_completion,
                'date_receipt': this.formData.date_receipt,
                'rental_time': this.formData.rental_time,
                'payment_method': this.formData.payment_method,
                'branch_id': this.formData.branch_id,
            }
            this.changeOrder(payload, this.formData.order_id);
            this.show_edit_modal = false;
            this.formInit();
        },
        changeOrder(payload, orderID) {
            const path = `http://localhost:5000/orders/${orderID}`;
            axios.put(path, payload)
            .then(() => {
                this.showMessageHandle('Заказ успешно изменен');
                this.fetchOrders();
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при изменении заказа');
            })
        },
        formInit() {
            this.formData.selected_dispetcher = null;
            this.formData.selected_pilot = null;
            this.formData.selected_client = null;
            this.formData.selected_helicopter = null;
            this.formData.order_address = null;
            this.formData.delivery_address = null;
            this.formData.date_completion = null;
            this.formData.date_receipt = null;
            this.formData.rental_time = null;
            this.formData.payment_method = null;
            this.formData.branch_id = null;
            this.formData.order_id = null;
        }
    },
    computed: {
        searchOrders() {
            let orders = [];
            if (this.selectedSort === this.sortOptions[0].value) {
                orders = [...this.orders].sort((order1, order2) => order1[this.selectedSort] - order2[this.selectedSort]);
            }
            else {
                orders = [...this.orders].sort((order1, order2) => order1[this.selectedSort]?.localeCompare(order2[this.selectedSort]));
            }
            if (this.selectedSortMethod == 'ascending')
                return orders;
            else if (this.selectedSortMethod == 'descending') {
                return orders.reverse();
            }
        },
        sortedAndSearchOrders() {
            if (this.clients.length > 0)
                return this.searchOrders.filter(order => 
                    this.clients.find(client => client.client_id === order.client_id).phone_number.includes(this.searchOrderClientStr) || this.clients.find(client => client.client_id === order.client_id).email.toLowerCase().includes(this.searchOrderClientStr.toLowerCase())
                )
        }
    },
    created() {
        this.fetchClients();
        setTimeout(this.fetchOrders, 100);
        setTimeout(this.fetchBranchOptions, 200);
        setTimeout(this.fetchEmployees, 2200);
        setTimeout(this.fetchDispetchers, 3200);
        setTimeout(this.fetchPilots, 4200);
        setTimeout(this.fetchHelicopters, 5200);
        setTimeout(this.fetchHelicopterModels, 6200);
    },
    mounted() {
        if (!this.$store.state.session.auth) {
            this.$router.push('/');
        }
    },
}
</script>

<style>

</style>