<template>
    <div>
        <nav-bar/>
        <div class="container">
            <div class="d-flex justify-content-start mt-1 mb-5">
                <h1>ДИСПЕТЧЕРЫ</h1>
            </div>
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
            <table class="table table-hover mt-4 mb-5">
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
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import mySelect from '../components/mySelect.vue';
import axios from 'axios';

export default {
    components: { NavBar, mySelect },
    data() {
        return {
            dispetchers: [],
            branch_options: [],
            employees_list: [],
            selectedSortDispetchersMethod: 'ascending',
            sortMethodDispetchersOptions: [
                {value: 'ascending', name: 'По возрастанию'},
                {value: 'descending', name: 'По убыванию'},  
            ],
            selectedSortDispetchers: 'id',
            sortOptionsDispetchers: [
                {value: 'id', name: 'По коду'},
                {value: 'surname', name: 'По фамилии'},
                {value: 'name', name: 'По имени'},
                {value: 'patronymic', name: 'По отчеству'},
                {value: 'branch_id', name: 'По филиалу'},
            ],
            searchDispetcherSurname: '',
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
        getBranchName: function(branch_code) {
            if(this.branch_options.length != 0) {
                return this.branch_options.find(branch => branch.value === branch_code).text;
            }
        },
    },
    computed: {
        sortDispetcher() {
            let dispetchers = [];
            if (this.selectedSortDispetchers == this.sortOptionsDispetchers[0].value) {
                dispetchers = [...this.employees_list].filter(e => this.dispetchers.some(j => j.id == e.id)).sort((employee1, employee2) => employee1[this.selectedSortDispetchers] - employee2[this.selectedSortDispetchers]);  
            }
            else {
                dispetchers = [...this.employees_list].filter(e => this.dispetchers.some(j => j.id == e.id)).sort((employee1, employee2) => employee1[this.selectedSortDispetchers]?.localeCompare(employee2[this.selectedSortDispetchers]));
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
    },
    async created() {
        await this.fetchEmployees();
        setTimeout(this.fetchBranchOptions, 100);
        setTimeout(this.fetchDispetchers, 300);
    },
    mounted() {
        if (this.$store.state.session.userType == 3 || !this.$store.state.session.auth) {
            this.$router.push('/');
        }
    },
}
</script>

<style>

</style>