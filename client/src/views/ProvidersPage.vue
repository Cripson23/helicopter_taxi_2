<template>
    <div>
        <nav-bar/>
        <div class="container">
            <div class="d-flex justify-content-start mt-1 mb-5">
                <h1>ПОСТАВЩИКИ ТОПЛИВА</h1>
            </div>
            <alert :message="message" v-if="showMessage"></alert>
            <div class="input-group-sm col-md-3">
                <input placeholder="Поиск поставщиков" v-model="searchProviderName" type="text" class="form-control sm" aria-describedby="inputHelp">
                <div class="form-text">
                    Начните вводить наименование поставщика, номер телефона или ФИО директора
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
                    <th scope="col">Код поставщика</th>
                    <th scope="col">Наименование</th>
                    <th scope="col">Адрес</th>
                    <th scope="col">Номер телефона</th>
                    <th scope="col">ФИО директора</th>
                    <th scope="col">Филиал</th>
                    <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(provider, index) in sortedAndSearchProviders" :key="index">
                        <td>{{ provider.id }}</td>
                        <td>{{ provider.name }}</td>
                        <td>{{ provider.address }}</td>
                        <td>{{ provider.phone_number }}</td>
                        <td>{{ provider.fio_director }}</td>
                        <td>{{ getBranchName(provider.branch_id) }}</td>
                        <td>
                            <button
                                type="button"
                                class="btn btn-warning btn-sm me-3"
                                @click="onEditProvider(provider)">
                                Изменить
                            </button>
                            <button
                            type="button"
                            class="btn btn-danger btn-sm"
                            @click="onDeleteProvider(provider.id)">
                                Удалить
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div class="d-md-flex justify-content-md-end me-5 pb-3 pt-2">
                <button type="button" @click="show_add_provider_modal=true" style="margin-right: 22px" class="btn btn-success btn-sm">Добавить поставщика</button>
            </div>
            <b-modal
                centered
                title="Добавление поставщика топлива"
                v-model="show_add_provider_modal"
                hide-footer>
                <b-form @submit="onAddProviderSubmit" @reset="onAddProviderReset" class="w-100">
                    <b-form-group id="form-name-provider-group"
                                label="Наименование:"
                                label-for="form-name-provider-input">
                        <b-form-input id="form-name-provider-input"
                                        type="text"
                                        v-model="formData.name"
                                        required
                                        placeholder="Введите наименование поставщика">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-provider-address-group"
                                label="Адрес:"
                                label-for="form-provider-address-input">
                        <b-form-input id="form-provider-address-input"
                                        type="text"
                                        v-model="formData.address"
                                        required
                                        placeholder="Введите адрес поставщика">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-provider-address-group"
                                label="Номер телефона:"
                                label-for="form-phone-input">
                        <b-form-input id="form-phone-input"
                                        type="text"
                                        v-model="formData.phone_number"
                                        required
                                        placeholder="Введите номер телефона поставщика">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-fio-director-group"
                                label="ФИО директора:"
                                label-for="form-fio-director-input">
                        <b-form-input id="form-fio-director-input"
                                        type="text"
                                        v-model="formData.fio_director"
                                        required
                                        placeholder="Введите ФИО директора">
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
                title="Изменить поставщика топлива"
                v-model="show_edit_modal"
                centered
                @hide="onResetUpdate"
                hide-footer>
                <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
                    <b-form-group id="form-name-provider-group"
                                label="Наименование:"
                                label-for="form-name-provider-input">
                        <b-form-input id="form-name-provider-input"
                                        type="text"
                                        v-model="formData.name"
                                        required
                                        placeholder="Введите наименование поставщика">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-provider-address-group"
                                label="Адрес:"
                                label-for="form-provider-address-input">
                        <b-form-input id="form-provider-address-input"
                                        type="text"
                                        v-model="formData.address"
                                        required
                                        placeholder="Введите адрес поставщика">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-provider-address-group"
                                label="Номер телефона:"
                                label-for="form-phone-input">
                        <b-form-input id="form-phone-input"
                                        type="text"
                                        v-model="formData.phone_number"
                                        required
                                        placeholder="Введите номер телефона поставщика">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-fio-director-group"
                                label="ФИО директора:"
                                label-for="form-fio-director-input">
                        <b-form-input id="form-fio-director-input"
                                        type="text"
                                        v-model="formData.fio_director"
                                        required
                                        placeholder="Введите ФИО директора">
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
                {value: 'name', name: 'По наименованию'},
                {value: 'address', name: 'По адресу'},
                {value: 'phone_number', name: 'По номеру телефона'},
                {value: 'fio_director', name: 'По фамилии директора'},
                {value: 'branch_id', name: 'По филиалу'},
            ],
            selectedSortMethod: 'ascending',
            sortMethodOptions: [
                {value: 'ascending', name: 'По возрастанию'},
                {value: 'descending', name: 'По убыванию'},  
            ],
            providers: [],
            show_add_provider_modal: false,
            formData: {
                'id': null,
                'name': null,
                'address': null,
                'phone_number': null,
                'fio_director': null,
                'branch_id': null,
            },
            branch_options: [],
            show_edit_modal: false,
        }
    },
    computed: {
    searchProviders() {
        let providers = [];
        if (this.selectedSort === this.sortOptions[0].value) {
            providers = [...this.providers].sort((provider1, provider2) => provider1[this.selectedSort] - provider2[this.selectedSort]);
        }
        else {
            providers = [...this.providers].sort((provider1, provider2) => provider1[this.selectedSort]?.localeCompare(provider2[this.selectedSort]));
        }
        if (this.selectedSortMethod == 'ascending')
            return providers;
        else if (this.selectedSortMethod == 'descending') {
            return providers.reverse();
        }
    },
    sortedAndSearchProviders() {
            return this.searchProviders.filter(provider => provider.name.toLowerCase().includes(this.searchProviderName.toLowerCase()) || provider.fio_director.toLowerCase().includes(this.searchProviderName.toLowerCase()) || provider.phone_number.includes(this.searchProviderName));
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
        getBranchName: function(branch_id) {
            if(this.branch_options.length != 0) {
                return this.branch_options.find(branch => branch.value === branch_id).text;
            }
        },
        initForm() {
            this.formData.id = null;
            this.formData.name = null;
            this.formData.address = null;
            this.formData.phone_number = null;
            this.formData.fio_director = null;
            this.formData.branch_id = null;
        },
        onAddProviderSubmit(evt) {
            evt.preventDefault();

            const payload = {
                'name': this.formData.name,
                'address': this.formData.address,
                'phone_number': this.formData.phone_number,
                'fio_director': this.formData.fio_director,
                'branch_id': this.formData.branch_id
            }

            this.addProvider(payload);
            this.show_add_provider_modal = false;
            this.initForm();
        },
        addProvider(payload) {
            const path = `http://localhost:5000/providers`;
            axios.post(path, payload)
            .then(() => {
                this.fetchProviders();
                this.showMessageHandle('Поставщик топлива успешно добавлен');
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при добавлении поставщика!');
            })
        },
        onAddProviderReset(evt) {
            evt.preventDefault();
            this.show_add_provider_modal = false;
            this.initForm();
        },
        onDeleteProvider(provider_id) {
            this.removeProvider(provider_id);
        },
        removeProvider(providerID) {
            const path = `http://localhost:5000/providers/${providerID}`;
            axios.delete(path)
            .then(() => {
                this.showMessageHandle('Поставщик топлива успешно удалён');
                this.fetchProviders();    
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при удалении поставщика');
            })
        },
        onEditProvider(provider) {
            this.formData.id = provider.id;
            this.formData.name = provider.name;
            this.formData.address = provider.address;
            this.formData.phone_number = provider.phone_number;
            this.formData.fio_director = provider.fio_director;
            this.formData.branch_id = provider.branch_id;

            this.show_edit_modal = true;
        },
        onSubmitUpdate(evt) {
            evt.preventDefault();

            const payload = {
                'name': this.formData.name,
                'address': this.formData.address,
                'phone_number': this.formData.phone_number,
                'fio_director': this.formData.fio_director,
                'branch_id': this.formData.branch_id,
            };

            this.updateProvider(payload, this.formData.id);

            this.show_edit_modal = false;
            this.initForm();
        },
        updateProvider(payload, providerID) {
            const path = `http://localhost:5000/providers/${providerID}`;
            axios.put(path, payload)
            .then(() => {
                this.showMessageHandle('Поставщик успешно изменен');
                this.fetchProviders();
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при изменении поставщика!');
            })
        },
        onResetUpdate() {
            this.show_edit_modal = false;
            this.initForm();
        }
    },
    async created() {
        await this.fetchBranchOptions();
        await this.fetchProviders();
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