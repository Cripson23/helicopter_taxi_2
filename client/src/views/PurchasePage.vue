<template>
    <div>
        <nav-bar/>
        <div class="container">
            <div class="d-flex justify-content-start mt-1 mb-5">
                <h1>ЗАКУПКИ ТОПЛИВА</h1>
            </div>
            <alert :message="message" v-if="showMessage"></alert>
            <div class="input-group-sm col-md-3">
                <input placeholder="Поиск закупок топлива" v-model="searchProviderName" type="text" class="form-control sm" aria-describedby="inputHelp">
                <div class="form-text">
                    Начните вводить наименование поставщика
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
            <table class="table table-hover mt-4">
                <thead>
                    <tr>
                    <th scope="col">Код закупки</th>
                    <th scope="col">Поставщик</th>
                    <th scope="col">Объём закупки</th>
                    <th scope="col">Дата закупки</th>
                    <th scope="col">Стоимость топлива (за 1л.)</th>
                    <th scope="col">Стоимость закупки (руб.)</th>
                    <th scope="col">Филиал</th>
                    <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(purchase, index) in sortedAndSearchPurchase" :key="index">
                        <td>{{ purchase.id }}</td>
                        <td>{{ getProviderName(purchase.provider_id) }}</td>
                        <td>{{ purchase.volume }}</td>
                        <td>{{ purchase.date }}</td>
                        <td>{{ purchase.price }}</td>
                        <td>{{ purchase.volume * purchase.price }}</td>
                        <td>{{ getBranchName(purchase.branch_id) }}</td>
                        <td>
                            <button
                                type="button"
                                class="btn btn-warning btn-sm me-3"
                                @click="onEditPurchase(purchase)">
                                Изменить
                            </button>
                            <button
                            type="button"
                            class="btn btn-danger btn-sm"
                            @click="onDeletePurchase(purchase.id)">
                                Удалить
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div class="d-md-flex justify-content-md-end me-5 pb-3 pt-2">
                <button type="button" @click="show_add_purchase_modal=true" style="margin-right: 22px" class="btn btn-success btn-sm">Добавить закупку</button>
            </div>
            <b-modal
                centered
                title="Добавление закупки топлива"
                v-model="show_add_purchase_modal"
                hide-footer>
                <b-form @submit="onAddPurchaseSubmit" @reset="onAddPurchaseReset" class="w-100">
                    <b-form-group id="form-provider-group"
                                    label="Поставщик топлива:"
                                    label-for="form-provider-input"
                    >
                        <b-form-select v-model="formData.provider_id" required>
                            <option
                            v-for="(provider, idx) in providers"
                            :key="idx"
                            :value="provider.id"
                            >
                            {{ provider.name }}
                            </option>
                        </b-form-select>
                    </b-form-group>
                    <b-form-group id="form-volume-group"
                                label="Объём закупки:"
                                label-for="form-volume-input">
                        <b-form-input id="form-volume-input"
                                type="number"
                                v-model="formData.volume"
                                required>
                        </b-form-input>
                        <b-form-input id="form-volume-input"
                                type="range"
                                min="1" 
                                max="500"
                                v-model="formData.volume"
                                required>
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-date-group"
                              label="Дата закупки:"
                              label-for="form-date-input">
                        <b-form-input id="form-date-input"
                                    type="date"
                                    v-model="formData.date"
                                    required
                                    placeholder="Выберите дату">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-price-group"
                                label="Стоимость топлива (за 1л.):"
                                label-for="form-price-input">
                        <b-form-input id="form-price-input"
                                type="number"
                                v-model="formData.price"
                                required>
                        </b-form-input>
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
                    <b-button class="me-3" type="submit" variant="primary">Добавить</b-button>
                    <b-button type="reset" variant="danger">Отмена</b-button>
                </b-form>
            </b-modal>
            <b-modal
                title="Изменить закупку топлива"
                v-model="show_edit_modal"
                centered
                @hide="onResetUpdate"
                hide-footer>
                <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
                    <b-form-group id="form-provider-group"
                                    label="Поставщик топлива:"
                                    label-for="form-provider-input"
                    >
                        <b-form-select v-model="formData.provider_id" required>
                            <option
                            v-for="(provider, idx) in providers"
                            :key="idx"
                            :value="provider.id"
                            >
                            {{ provider.name }}
                            </option>
                        </b-form-select>
                    </b-form-group>
                    <b-form-group id="form-volume-group"
                                label="Объём закупки:"
                                label-for="form-volume-input">
                        <b-form-input id="form-volume-input"
                                type="number"
                                v-model="formData.volume"
                                required>
                        </b-form-input>
                        <b-form-input id="form-volume-input"
                                type="range"
                                min="1" 
                                max="500"
                                v-model="formData.volume"
                                required>
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-date-group"
                              label="Дата закупки:"
                              label-for="form-date-input">
                        <b-form-input id="form-date-input"
                                    type="date"
                                    v-model="formData.date"
                                    required
                                    placeholder="Выберите дату">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-price-group"
                                label="Стоимость топлива (за 1л.):"
                                label-for="form-price-input">
                        <b-form-input id="form-price-input"
                                type="number"
                                v-model="formData.price"
                                required>
                        </b-form-input>
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
                    <b-button class="me-3" type="submit" variant="primary">Сохранить</b-button>
                    <b-button type="reset" variant="danger">Отмена</b-button>
                </b-form>
            </b-modal>
        </div>
    </div>
</template>

<script>
import Alert from '@/components/Alert.vue';
import NavBar from '@/components/NavBar.vue';
import mySelect from '../components/mySelect.vue';
import showMessage from '@/mixins/showMessage';
import axios from 'axios';

export default {
    mixins: [showMessage],
    components: {
        Alert,
        NavBar,
        mySelect,
    },
    data() {
        return {
            message: '',
            showMessage: false,
            searchProviderName: '',
            selectedSort: 'id',
            sortOptions: [
                {value: 'id', name: 'По коду'},
                {value: 'provider_id', name: 'По поставщику'},
                {value: 'volume', name: 'По объёму'},
                {value: 'date', name: 'По дате'},
                {value: 'price', name: 'По стоимости топлива'},
                {value: 'branch_id', name: 'По филиалу'},
            ],
            selectedSortMethod: 'ascending',
            sortMethodOptions: [
                {value: 'ascending', name: 'По возрастанию'},
                {value: 'descending', name: 'По убыванию'},  
            ],
            providers: [],
            purchases: [],
            show_add_purchase_modal: false,
            formData: {
                'id': null,
                'provider_id': null,
                'volume': null,
                'date': null,
                'price': null,
                'branch_id': null,
            },
            branch_options: [],
            show_edit_modal: false,
        }
    },
    computed: {
        searchPurchase() {
            let purchases = [];
            if (this.selectedSort === this.sortOptions[3].value) {
                purchases = [...this.purchases].sort((purchase1, purchase2) => purchase1[this.selectedSort]?.localeCompare(purchase2[this.selectedSort]));
            }
            else {
                purchases = [...this.purchases].sort((purchase1, purchase2) => purchase1[this.selectedSort] - purchase2[this.selectedSort]);
            }
            if (this.selectedSortMethod == 'ascending')
                return purchases;
            else if (this.selectedSortMethod == 'descending') {
                return purchases.reverse();
            }
        },
        sortedAndSearchPurchase() {
                return this.searchPurchase.filter(purchase => this.getProviderName(purchase.provider_id).toLowerCase().includes(this.searchProviderName.toLowerCase()));
            }
        },
    methods: {
        async fetchBranchOptions() {
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
        async fetchProviders() {
            const path = `http://127.0.0.1:5000/providers`
            axios.get(path)
            .then((response) => {
                this.providers = response.data;
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при загрузке поставщиков');
            })
        },
        async fetchPurchases() {
            const path = `http://127.0.0.1:5000/purchases`
            axios.get(path)
            .then((response) => {
                this.purchases = response.data;
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при загрузке закупок топлива');
            })
        },
        getBranchName: function(branch_id) {
            if(this.branch_options.length != 0) {
                return this.branch_options.find(branch => branch.value === branch_id).text;
            }
        },
        getProviderName(provider_id) {
            if(this.providers.length != 0) {
                const provider = this.providers.find(provider => provider.id === provider_id);
                if (provider != undefined)
                    return provider.name;
            }
        },
        initForm() {
            this.formData.id = null;
            this.formData.provider_id = null;
            this.formData.volume = null;
            this.formData.date = null;
            this.formData.price = null;
            this.formData.branch_id = null;
        },
        onAddPurchaseSubmit(evt) {
            evt.preventDefault();

            const payload = {
                'provider_id': this.formData.provider_id,
                'volume': this.formData.volume,
                'date': this.formData.date,
                'price': this.formData.price,
                'branch_id': this.formData.branch_id,
            }

            this.addPurchase(payload);
            this.show_add_purchase_modal = false;
            this.initForm();
        },
        addPurchase(payload) {
            const path = `http://localhost:5000/purchases`;
            axios.post(path, payload)
            .then(() => {
                this.fetchPurchases();
                this.showMessageHandle('Закупка топлива успешно добавлена');
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при добавлении закупки топлива!');
            })
        },
        onAddPurchaseReset(evt) {
            evt.preventDefault();
            this.show_add_purchase_modal = false;
            this.initForm();
        },
        onDeletePurchase(purchase_id) {
            this.removePurchase(purchase_id);
        },
        removePurchase(purchaseID) {
            const path = `http://localhost:5000/purchases/${purchaseID}`;
            axios.delete(path)
            .then(() => {
                this.showMessageHandle('Закупка топлива успешно удалена');
                this.fetchPurchases();    
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при удалении закупки топлива');
            })
        },
        onEditPurchase(purchase) {
            this.formData.id = purchase.id;
            this.formData.provider_id = purchase.provider_id;
            this.formData.volume = purchase.volume;
            this.formData.date = purchase.date;
            this.formData.price = purchase.price;
            this.formData.branch_id = purchase.branch_id;

            this.show_edit_modal = true;
        },
        onSubmitUpdate(evt) {
            evt.preventDefault();

            const payload = {
                'provider_id': this.formData.provider_id,
                'volume': this.formData.volume,
                'date': this.formData.date,
                'price': this.formData.price,
                'branch_id': this.formData.branch_id,
            };

            this.updatePurchase(payload, this.formData.id);

            this.show_edit_modal = false;
            this.initForm();
        },
        updatePurchase(payload, purchaseID) {
            const path = `http://localhost:5000/purchases/${purchaseID}`;
            axios.put(path, payload)
            .then(() => {
                this.showMessageHandle('Закупка топлива успешно изменена');
                this.fetchPurchases();
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при изменении закупки топлива!');
            })
        },
        onResetUpdate() {
            this.show_edit_modal = false;
            this.initForm();
        }
    },
    async created() {
        await this.fetchPurchases();
        await this.fetchBranchOptions();
        setTimeout(this.fetchProviders, 200);
    },
    mounted() {
        if (this.$store.state.session.userType != 3 || !this.$store.state.session.auth) {
            this.$router.push('/');
        }
    },
}
</script>

<style>

</style>