<template>
    <div>
        <nav-bar/>
        <b-container>
            <div class="d-flex justify-content-start mt-1 mb-4">
                <h1>ШАБЛОНЫ ДОКУМЕНТОВ</h1>
            </div>
            <h4>Выберите шаблон документа</h4>
            <b-form-select class="w-25" v-model="selectedForm">
                <option :value="f" v-for="(f, idx) in forms" :key="idx">{{ f }}</option>
            </b-form-select>
            <b-button class="mt-3" v-if="htmlForm" @click="onDownloadClick">Загрузить документ</b-button>
            <b-container class="mb-5">
                <component ref="htmlFormComponent" v-if="htmlForm" :is="formComponent"></component>
            </b-container>
        </b-container>
    </div>
</template>

<script>
import axios from 'axios';
import NavBar from '../components/NavBar.vue';

export default {
    components: { NavBar },
    
    data() {
        return {
            forms: [],
            selectedForm: null,
            htmlForm: null,
        }
    },
    methods: {
        async fetchForms() {
            const path = 'http://localhost:5000/api/forms';
            axios.get(path)
            .then((res) => {
                this.forms = res.data.forms;
            })
            .catch((err) => {
                console.log(err);
                alert('Ошибка при загрузке форм');
            })
        },
        onDownloadClick () {
        let data = this.$refs.htmlFormComponent.$refs;

        // формируем строку параметров get запроса
        let params = Object.keys(data).map(function (key) {
            return [key, data[key].value].map(encodeURIComponent).join("=");
        }).join("&");

        // формируем url, передавать параметры get запросом не очень хорошая идея,
        // но для тестового приложения пойдет
        let url = `http://localhost:5000/api/form/print/${this.selectedForm}?${params}`;
            window.open(url);
        }
    },
    async created() {
        await this.fetchForms();
    },
    computed: {
        formComponent() {
            return {
                template: `<div>${this.htmlForm}</div>`,
            }
        },
    },
    watch: {
        selectedForm() {
            const path = `http://localhost:5000/api/form/${this.selectedForm}`;
            console.log(path);
            axios.get(path).then(response => {
                let html = response.data.html.replace(
                    /\{\{ (\w+) \}\}/g,
                    '<input ref="$1" placeholder="$1">'
                );
                this.htmlForm = html;
            }).catch((error) => {
                console.log(error);
            })
        }
    }
}
</script>

<style>

</style>