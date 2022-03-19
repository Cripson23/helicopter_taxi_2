<template>
    <div>
        <nav-bar/>
        <div class="container">
            <div class="d-flex justify-content-start mt-1 mb-5">
                <h1>ПИЛОТЫ</h1>
            </div>
            <div class="input-group-sm col-md-3">
                <input placeholder="Поиск пилота" v-model="searchPilotsSurname" type="text" class="form-control sm" aria-describedby="inputHelp">
                <div id="inputHelp" class="form-text">
                    Начните вводить фамилию пилота
                </div>
            </div>
            <div class="d-md-flex justify-content-md-end me-5 pb-3 pt-2">
                <my-select
                v-model="selectedSortPilots"
                :options="sortOptionsPilots"
                />
                <my-select
                v-model="selectedSortPilotsMethod"
                :options="sortMethodPilotsOptions"
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
                    <tr v-for="(pilot, index) in sortedAndSearchPilot" :key="index">
                    <td>{{ pilot.id }}</td>
                    <td>{{ pilot.surname }}</td>
                    <td>{{ pilot.name }}</td>
                    <td>{{ pilot.patronymic }}</td>
                    <td>{{ getBranchName(pilot.branch_id) }}</td>
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
            pilots: [],
            branch_options: [],
            employees_list: [],
            selectedSortPilotsMethod: 'ascending',
            sortMethodPilotsOptions: [
                {value: 'ascending', name: 'По возрастанию'},
                {value: 'descending', name: 'По убыванию'},  
            ],
            selectedSortPilots: 'id',
            sortOptionsPilots: [
                {value: 'id', name: 'По коду'},
                {value: 'surname', name: 'По фамилии'},
                {value: 'name', name: 'По имени'},
                {value: 'patronymic', name: 'По отчеству'},
                {value: 'branch_id', name: 'По филиалу'},
            ],
            searchPilotsSurname: '',
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
        async fetchPilots() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/pilots');
                this.pilots = response.data;
            } catch (e) {
                alert('Возникла ошибка при получении Пилотов');
            }
        },
        getBranchName: function(branch_code) {
            if(this.branch_options.length != 0) {
                return this.branch_options.find(branch => branch.value === branch_code).text;
            }
        },
    },
    computed: {
        sortPilot() {
            let pilots = [];
            if (this.selectedSortPilots == this.sortOptionsPilots[0].value) {
                pilots = [...this.employees_list].filter(e => this.pilots.some(j => j.id == e.id)).sort((employee1, employee2) => employee1[this.selectedSortPilots] - employee2[this.selectedSortPilots]);  
            }
            else {
                pilots = [...this.employees_list].filter(e => this.pilots.some(j => j.id == e.id)).sort((employee1, employee2) => employee1[this.selectedSortPilots]?.localeCompare(employee2[this.selectedSortPilots]))
            }
            if (this.selectedSortPilotsMethod == 'ascending')
                return pilots;
            else if (this.selectedSortPilotsMethod == 'descending') {
                return pilots.reverse();
            }
        },
        sortedAndSearchPilot() {
            return this.sortPilot.filter(pilot => pilot.surname.toLowerCase().includes(this.searchPilotsSurname.toLowerCase()))
        },
    },
    async created() {
        await this.fetchEmployees();
        setTimeout(this.fetchBranchOptions, 100);
        setTimeout(this.fetchPilots, 500);
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