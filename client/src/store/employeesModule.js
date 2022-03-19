import axios from 'axios';

export const employeesModule = {
    state: () => ({
        employees_list: [],
        selectedSort: '',
        searchSurname: '',
    }),
    getters: {
        sortedEmployees(state) {
            console.log(state.selectedSort);
            return [...state.employees_list].sort((employee1, employee2) => employee1[state.selectedSort]?.localeCompare(employee2[state.selectedSort]))
        },
        sortedAndSearchEmployees(state, getters) {
            return getters.sortedEmployees.filter(employee => employee.surname.toLowerCase().includes(state.searchSurname.toLowerCase()))
        }
    },
    mutations: {
        setEmployees(state, employees) {
            state.employees_list = employees;
        },
        setSelectSort(state, selectSort) {
            state.selectedSort = selectSort;
        },
        setSearchSurname(state, searchSurname) {
            state.searchSurname = searchSurname;
        },
    },
    actions: {
        async fetchEmployees({ state, commit }) {
            try {
                const response = await axios.get('http://127.0.0.1:5000/employees');
                commit('setEmployees', response.data);
            } catch (e) {
                alert('Ошибка');
            }
        }
    },
    namespaced: true
}