<template>
    <div>
        <nav-bar/>
        <div class="container">
            <div class="d-flex justify-content-start mb-5">
                <h1>ВЕРТОЛЕТЫ</h1>
            </div>
            <alert :message="message" v-if="showMessage"></alert>
            <div class="input-group-sm col-md-3">
                <input placeholder="Поиск вертолетов по модели" v-model="searchModelName" type="text" class="form-control sm" aria-describedby="inputHelp">
                <div class="form-text">
                    Начните вводить наименование модели вертолета
                </div>
            </div>
            <b-container class="bv-example-row mt-4">
                <b-row>
                    <b-col v-show="this.$store.state.session.userType == 3">
                        <b-form-group label="Фильтрация:" v-slot="{ ariaDescribedby }">
                            <b-form-radio v-model="selected_option" :aria-describedby="ariaDescribedby" name="some-radios" value="none">Отсутствует</b-form-radio>
                            <b-form-radio v-model="selected_option" :aria-describedby="ariaDescribedby" name="some-radios" value="recycling">Подлежат утилизации</b-form-radio>
                            <b-form-radio v-model="selected_option" :aria-describedby="ariaDescribedby" name="some-radios" value="inspection">Подлежат тех. осмотру</b-form-radio>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <div class="d-md-flex justify-content-md-end me-3 pb-3 pt-5 mt-4">
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
                    </b-col>
                </b-row>
            </b-container>
            <table class="table table-hover mt-4">
                <thead>
                    <tr>
                    <th scope="col">Код вертолета</th>
                    <th scope="col">Модель</th>
                    <th scope="col">Год выпуска</th>
                    <th scope="col">Дата последнего тех. осмотра</th>
                    <th scope="col">Код филиала</th>
                    <th v-show="this.$store.state.session.userType == 3"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(helicopter, index) in sortedAndSearchHelicopters" :key="index">
                        <td>{{ helicopter.id }}</td>
                        <td>{{ getModelInfo(helicopter.model_id) }}</td>
                        <td>{{ helicopter.year_issue }}</td>
                        <td>{{ helicopter.date_inspection }}</td>
                        <td>{{ getBranchName(helicopter.branch_id) }}</td>
                        <td v-if="this.$store.state.session.userType == 3">
                            <button
                                type="button"
                                class="btn btn-warning btn-sm me-3"
                                @click="onEditHelicopter(helicopter)">
                                Изменить
                            </button>
                            <button
                            type="button"
                            class="btn btn-danger btn-sm"
                            @click="onDeleteHelicopter(helicopter.id)">
                                Удалить
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-if="this.$store.state.session.userType == 3" class="d-md-flex justify-content-md-end me-5 pb-3 pt-2">
                <button type="button" @click="show_add_helicopter_modal=true" style="margin-right: 22px" class="btn btn-success btn-sm">Добавить вертолет</button>
                <button type="button" @click="show_delete_recycling_modal = true;" style="margin-right: 22px" class="btn btn-danger btn-sm">Удалить подлежащие утилизации</button>
            </div>
            <b-modal
                centered
                title="Добавление вертолета"
                v-model="show_add_helicopter_modal"
                hide-footer>
                <b-form @submit="onAddHelicopterSubmit" @reset="onAddHelicopterReset" class="w-100">
                    <b-form-group id="form-helicopter-model-group"
                              label="Модель вертолета:"
                              label-for="form-helicopter-model-select"
                    >
                        <b-form-select v-model="formData.model_id" required>
                            <option
                                v-for="(model, idx) in models"
                                :key="idx"
                                :value="model.id"
                            >
                                {{ getModelInfo(model.id) }}
                            </option>
                        </b-form-select>
                    </b-form-group>
                    <b-form-group id="form-year-release-group"
                                label="Год выпуска:"
                                label-for="form-year-release-input">
                        <b-form-input id="form-year-release-input"
                                type="number"
                                v-model="formData.year_issue"
                                required
                                placeholder="Введите год выпуска вертолета">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-date-inspection-group"
                                label="Дата последнего тех. осмотра:"
                                label-for="form-date-inspection-input">
                        <b-form-input id="form-date-inspection-input"
                                        type="date"
                                        v-model="formData.date_inspection"
                                        required
                                        placeholder="Выберите дату">
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
                title="Изменить вертолет"
                    v-model="show_edit_modal"
                    centered
                    @hide="onResetUpdate"
                    hide-footer>
                <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
                    <b-form-group id="form-helicopter-model-group"
                              label="Модель вертолета:"
                              label-for="form-helicopter-model-select"
                    >
                        <b-form-select v-model="formData.model_id" required>
                            <option
                                v-for="(model, idx) in models"
                                :key="idx"
                                :value="model.id"
                            >
                                {{ getModelInfo(model.id) }}
                            </option>
                        </b-form-select>
                    </b-form-group>
                    <b-form-group id="form-year-release-group"
                                label="Год выпуска:"
                                label-for="form-year-release-input">
                        <b-form-input id="form-year-release-input"
                                type="number"
                                v-model="formData.year_issue"
                                required
                                placeholder="Введите год выпуска вертолета">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-date-inspection-group"
                                label="Дата последнего тех. осмотра:"
                                label-for="form-date-inspection-input">
                        <b-form-input id="form-date-inspection-input"
                                        type="date"
                                        v-model="formData.date_inspection"
                                        required
                                        placeholder="Выберите дату">
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
            <b-modal
                centered
                title="Удаление вертолетов, подлежащих утилизации"
                v-model="show_delete_recycling_modal"
                hide-footer>
                <b-form-group>
                    <p>Вы действительно хотите удалить информацию о вертолетах, подлежащих утилизации?<br><br>
                    Восстановить данные будет невозможно.</p>
                </b-form-group>
                <b-form @submit="onDeleteRecyclingSubmit" @reset="show_delete_recycling_modal = false" class="w-100 text-center">
                    <b-button class="me-3" type="submit" variant="danger">Удалить</b-button>
                    <b-button type="reset" variant="primary">Отмена</b-button>
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
            searchModelName: '',
            selectedSort: 'id',
            selected_option: 'none',
            sortOptions: [
                {value: 'id', name: 'По коду'},
                {value: 'model_id', name: 'По модели'},
                {value: 'year_issue', name: 'По году выпуска'},
                {value: 'date_inspection', name: 'По дате тех. осмотра'},
                {value: 'branch_id', name: 'По филиалу'},
            ],
            selectedSortMethod: 'ascending',
            sortMethodOptions: [
                {value: 'ascending', name: 'По возрастанию'},
                {value: 'descending', name: 'По убыванию'},  
            ],
            models: [],
            helicopters: [],
            branch_options: [],
            show_add_helicopter_modal: false,
            show_delete_recycling_modal: false,
            formData: {
                'id': null,
                'model_id': null,
                'year_issue': null,
                'date_inspection': null,
                'branch_id': null,
            },
            show_edit_modal: false,
        }
    },
    computed: {
        searchHelicopter() {
            let helicopters = [];
            if (this.selectedSort === this.sortOptions[3].value) {
                helicopters = [...this.helicopters].sort((helicopter1, helicopter2) => helicopter1[this.selectedSort]?.localeCompare(helicopter2[this.selectedSort]));
            }
            else {
                helicopters = [...this.helicopters].sort((helicopter1, helicopter2) => helicopter1[this.selectedSort] - helicopter2[this.selectedSort]);
            }
            if (this.selectedSortMethod == 'ascending')
                return helicopters;
            else if (this.selectedSortMethod == 'descending') {
                return helicopters.reverse();
            }
        },
        sortedAndSearchHelicopters() {
            let helicopters = this.searchHelicopter.filter(helicopter => this.getModelInfo(helicopter.model_id).toLowerCase().includes(this.searchModelName.toLowerCase()));
            if (this.selected_option == 'recycling') {
                helicopters = helicopters.filter(helicopter => (helicopter.year_issue + 20 <= new Date().getFullYear()));
            } else if (this.selected_option == 'inspection') {
                helicopters = helicopters.filter(helicopter => (this.getInspectionDate(helicopter.date_inspection) < new Date()));
            }
            return helicopters;
        }
    },
    methods: {
        async fetchModels() {
            const path = `http://127.0.0.1:5000/helicopter-models`
            axios.get(path)
            .then((response) => {
                this.models = response.data;
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при загрузке моделей вертолётов');
            })
        },
        async fetchHelicopters() {
            const path = `http://127.0.0.1:5000/helicopters`
            axios.get(path)
            .then((response) => {
                this.helicopters = response.data;
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при загрузке вертолётов');
            })
        },
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
        initForm() {
            this.formData.id = null;
            this.formData.model_id = null;
            this.formData.year_issue = null;
            this.formData.date_inspection = null;
            this.formData.branch_id = null;
        },
        onAddHelicopterSubmit(evt) {
            evt.preventDefault();

            const payload = {
                'model_id': this.formData.model_id,
                'year_issue': this.formData.year_issue,
                'date_inspection': this.formData.date_inspection,
                'branch_id': this.formData.branch_id,
            }

            this.addHelicopter(payload);
            this.show_add_helicopter_modal = false;
            this.initForm();
        },
        addHelicopter(payload) {
            const path = `http://localhost:5000/helicopters`;
            axios.post(path, payload)
            .then(() => {
                this.fetchHelicopters();
                this.showMessageHandle('Вертолет успешно добавлен');
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при добавлении вертолета!');
            })
        },
        onAddHelicopterReset(evt) {
            evt.preventDefault();
            this.show_add_helicopter_modal = false;
            this.initForm();
        },
        onDeleteHelicopter(helicopter_id) {
            this.removeHelicopter(helicopter_id);
        },
        removeHelicopter(helicopterID) {
            const path = `http://localhost:5000/helicopters/${helicopterID}`;
            axios.delete(path)
            .then(() => {
                this.showMessageHandle('Вертолёт успешно удален');
                this.fetchHelicopters();
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при удалении вертолёта');
            })
        },
        onEditHelicopter(helicopter) {
            this.formData.id = helicopter.id;
            this.formData.model_id = helicopter.model_id;
            this.formData.year_issue = helicopter.year_issue;
            this.formData.date_inspection = helicopter.date_inspection;
            this.formData.branch_id = helicopter.branch_id;

            this.show_edit_modal = true;
        },
        onSubmitUpdate(evt) {
            evt.preventDefault();

            const payload = {
                'model_id': this.formData.model_id,
                'year_issue': this.formData.year_issue,
                'date_inspection': this.formData.date_inspection,
                'branch_id': this.formData.branch_id,
            };

            this.updateHelicopter(payload, this.formData.id);

            this.show_edit_modal = false;
            this.initForm();
        },
        updateHelicopter(payload, helicopterID) {
            const path = `http://localhost:5000/helicopters/${helicopterID}`;
            axios.put(path, payload)
            .then(() => {
                this.showMessageHandle('Вертолет успешно изменен');
                this.fetchHelicopters();
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при изменении вертолета!');
            })
        },
        onResetUpdate() {
            this.show_edit_modal = false;
            this.initForm();
        },
        getModelInfo(model_id) {
            const model = this.models.find(model => model.id === model_id);
            return model.name + ' (ID: ' + model.id + ')';
        },
        getBranchName: function(branch_code) {
            if(this.branch_options.length != 0) {
                return this.branch_options.find(branch => branch.value === branch_code).text;
            }
        },
        getInspectionDate(date_inspection) {
            let date = new Date(date_inspection);
            let year = date.getUTCFullYear()+1;
            date.setUTCFullYear(year);
            return date;
        },
        onDeleteRecyclingSubmit() {
            this.deleteRecyclingHelicopters();
            this.show_delete_recycling_modal = false;
        },
        deleteRecyclingHelicopters() {
            const path = `http://localhost:5000/deleteRecyclingHelicopters`
            axios.delete(path)
            .then(() => {
                this.fetchHelicopters();
                this.showMessageHandle('Все вертолеты, подлежащие утилизации, успешно удалены');
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при удалении вертолетов, подлежащих утилизации')
            })
        }
    },
    async created() {
        await this.fetchBranchOptions();
        setTimeout(this.fetchModels, 200);
        setTimeout(this.fetchHelicopters, 500);
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