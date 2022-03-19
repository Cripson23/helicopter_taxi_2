<template>
    <div>
        <nav-bar/>
        <div class="container">
            <div class="d-flex justify-content-start mb-5">
                <h1>МОДЕЛИ ВЕРТОЛЕТОВ</h1>
            </div>
            <alert :message="message" v-if="showMessage"></alert>
            <div class="input-group-sm col-md-3">
                <input placeholder="Поиск моделей" v-model="searchModelName" type="text" class="form-control sm" aria-describedby="inputHelp">
                <div class="form-text">
                    Начните вводить наименование модели вертолетов
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
                    <th scope="col">Код модели</th>
                    <th scope="col">Наименование</th>
                    <th scope="col">Вместимость</th>
                    <th scope="col">Скорость</th>
                    <th scope="col">Дальность</th>
                    <th scope="col">Стоимость 1 часа аренды</th>
                    <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(model, index) in sortedAndSearchModels" :key="index">
                        <td>{{ model.id }}</td>
                        <td>{{ model.name }}</td>
                        <td>{{ model.capacity }}</td>
                        <td>{{ model.speed }}</td>
                        <td>{{ model.range }}</td>
                        <td>{{ model.price }}</td>
                        <td>
                            <button
                                type="button"
                                class="btn btn-warning btn-sm me-3"
                                @click="onEditModel(model)">
                                Изменить
                            </button>
                            <button
                            type="button"
                            class="btn btn-danger btn-sm"
                            @click="onDeleteModel(model.id)">
                                Удалить
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div class="d-md-flex justify-content-md-end me-5 pb-3 pt-2">
                <button type="button" @click="show_add_model_modal=true" style="margin-right: 22px" class="btn btn-success btn-sm">Добавить модель</button>
            </div>
            <b-modal
                centered
                title="Добавление модели вертолетов"
                v-model="show_add_model_modal"
                hide-footer>
                <b-form @submit="onAddModelSubmit" @reset="onAddModelReset" class="w-100">
                    <b-form-group id="form-name-group"
                                label="Наименование:"
                                label-for="form-name-input">
                        <b-form-input id="form-name-input"
                                        type="text"
                                        v-model="formData.name"
                                        required
                                        placeholder="Введите наименование модели">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-capacity-group"
                                label="Вместимость:"
                                label-for="form-capacity-input">
                        <b-form-input id="form-capacity-input"
                                type="number"
                                v-model="formData.capacity"
                                required
                                placeholder="Введите вместимость модели вертолетов">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-speed-group"
                                label="Скорость:"
                                label-for="form-speed-input">
                        <b-form-input id="form-speed-input"
                                type="number"
                                v-model="formData.speed"
                                required
                                placeholder="Введите скорость модели вертолетов">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-range-group"
                                label="Дальность:"
                                label-for="form-range-input">
                        <b-form-input id="form-range-input"
                                type="number"
                                v-model="formData.range"
                                required
                                placeholder="Введите дальность модели вертолетов">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-price-group"
                                label="Стоимость одного часа аренды:"
                                label-for="form-price-input">
                        <b-form-input id="form-price-input"
                                type="number"
                                v-model="formData.price"
                                required
                                placeholder="Введите стоимость одного часа аренды модели">
                        </b-form-input>
                    </b-form-group>
                    <b-button class="me-3" type="submit" variant="primary">Добавить</b-button>
                    <b-button type="reset" variant="danger">Отмена</b-button>
                </b-form>
            </b-modal>
            <b-modal
                title="Изменить модель вертолетов"
                    v-model="show_edit_modal"
                    centered
                    @hide="onResetUpdate"
                    hide-footer>
                <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
                    <b-form-group id="form-name-group"
                                label="Наименование:"
                                label-for="form-name-input">
                        <b-form-input id="form-name-input"
                                        type="text"
                                        v-model="formData.name"
                                        required
                                        placeholder="Введите наименование модели">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-capacity-group"
                                label="Вместимость:"
                                label-for="form-capacity-input">
                        <b-form-input id="form-capacity-input"
                                type="number"
                                v-model="formData.capacity"
                                required
                                placeholder="Введите вместимость модели вертолетов">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-speed-group"
                                label="Скорость:"
                                label-for="form-speed-input">
                        <b-form-input id="form-speed-input"
                                type="number"
                                v-model="formData.speed"
                                required
                                placeholder="Введите скорость модели вертолетов">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-range-group"
                                label="Дальность:"
                                label-for="form-range-input">
                        <b-form-input id="form-range-input"
                                type="number"
                                v-model="formData.range"
                                required
                                placeholder="Введите дальность модели вертолетов">
                        </b-form-input>
                    </b-form-group>
                    <b-form-group id="form-price-group"
                                label="Стоимость одного часа аренды:"
                                label-for="form-price-input">
                        <b-form-input id="form-price-input"
                                type="number"
                                v-model="formData.price"
                                required
                                placeholder="Введите стоимость одного часа аренды модели">
                        </b-form-input>
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
            searchModelName: '',
            selectedSort: 'id',
            sortOptions: [
                {value: 'id', name: 'По коду'},
                {value: 'name', name: 'По наименованию'},
                {value: 'capacity', name: 'По вместимости'},
                {value: 'speed', name: 'По скорости'},
                {value: 'range', name: 'По дальности'},
                {value: 'price', name: 'По стоимости'},
            ],
            selectedSortMethod: 'ascending',
            sortMethodOptions: [
                {value: 'ascending', name: 'По возрастанию'},
                {value: 'descending', name: 'По убыванию'},  
            ],
            models: [],
            show_add_model_modal: false,
            formData: {
                'id': null,
                'name': null,
                'capacity': null,
                'speed': null,
                'range': null,
                'price': null,
            },
            show_edit_modal: false,
        }
    },
    computed: {
        searchModels() {
            let models = [];
            if (this.selectedSort === this.sortOptions[1].value) {
                models = [...this.models].sort((model1, model2) => model1[this.selectedSort]?.localeCompare(model2[this.selectedSort]));
            }
            else {
                models = [...this.models].sort((model1, model2) => model1[this.selectedSort] - model2[this.selectedSort]);
            }
            if (this.selectedSortMethod == 'ascending')
                return models;
            else if (this.selectedSortMethod == 'descending') {
                return models.reverse();
            }
        },
        sortedAndSearchModels() {
            return this.searchModels.filter(model => model.name.toLowerCase().includes(this.searchModelName.toLowerCase()));
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
        initForm() {
            this.formData.id = null;
            this.formData.name = null;
            this.formData.capacity = null;
            this.formData.speed = null;
            this.formData.range = null;
            this.formData.price = null;
        },
        onAddModelSubmit(evt) {
            evt.preventDefault();

            const payload = {
                'name': this.formData.name,
                'capacity': this.formData.capacity,
                'speed': this.formData.speed,
                'range': this.formData.range,
                'price': this.formData.price
            }

            this.addModel(payload);
            this.show_add_model_modal = false;
            this.initForm();
        },
        addModel(payload) {
            const path = `http://localhost:5000/helicopter-models`;
            axios.post(path, payload)
            .then(() => {
                this.fetchModels();
                this.showMessageHandle('Модель вертолетов успешно добавлена');
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при добавлении модели вертолетов!');
            })
        },
        onAddModelReset(evt) {
            evt.preventDefault();
            this.show_add_model_modal = false;
            this.initForm();
        },
        onDeleteModel(model_id) {
            this.removeModel(model_id);
        },
        removeModel(modelID) {
            const path = `http://localhost:5000/helicopter-models/${modelID}`;
            axios.delete(path)
            .then(() => {
                this.showMessageHandle('Модель вертолёта успешно удалена');
                this.fetchModels();
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при удалении модели вертолёта');
            })
        },
        onEditModel(model) {
            this.formData.id = model.id;
            this.formData.name = model.name;
            this.formData.capacity = model.capacity;
            this.formData.speed = model.speed;
            this.formData.range = model.range;
            this.formData.price = model.price;

            this.show_edit_modal = true;
        },
        onSubmitUpdate(evt) {
            evt.preventDefault();

            const payload = {
                'name': this.formData.name,
                'capacity': this.formData.capacity,
                'speed': this.formData.speed,
                'range': this.formData.range,
                'price': this.formData.price,
            };

            this.updateModel(payload, this.formData.id);

            this.show_edit_modal = false;
            this.initForm();
        },
        updateModel(payload, modelID) {
            const path = `http://localhost:5000/helicopter-models/${modelID}`;
            axios.put(path, payload)
            .then(() => {
                this.showMessageHandle('Модель успешно изменена');
                this.fetchModels();
            })
            .catch((error) => {
                console.log(error);
                alert('Ошибка при изменении модели!');
            })
        },
        onResetUpdate() {
            this.show_edit_modal = false;
            this.initForm();
        }
    },
    async created() {
        await this.fetchModels();
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