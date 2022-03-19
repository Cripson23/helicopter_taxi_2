<template>
    <div>
        <nav v-if="$store.state.session.userType === 3" class="navbar navbar-expand-lg navbar-light bg-light">
            <div id="navbar-line" class="container px-4 pb-4">
                <div class="pe-3">
                    <router-link to="/employees">
                        <img src="../assets/logo-blue.png" class="mx-auto d-block" alt="Logo">
                    </router-link>
                </div>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNavDropdown">
                    <ul class="navbar-nav">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                Управление персоналом
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                                <li>
                                    <router-link
                                        to="/employees" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('employees') }" 
                                        aria-current="page"
                                    >
                                        Работа с сотрудниками
                                    </router-link>
                                </li>
                                <li>
                                    <router-link 
                                        to="/recertification" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('recertification'), disabled: isActive('recertification') }" 
                                        aria-current="page"
                                    >
                                        Переаттестация пилотов
                                    </router-link>
                                </li>
                            </ul>
                        </li>

                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                Управление продажами
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                                <li>
                                    <router-link 
                                        to="/clients" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('clients'), disabled: isActive('clients') }" 
                                        aria-current="page"
                                    >
                                        Работа с клиентами
                                    </router-link>
                                </li>
                                <li>
                                    <router-link 
                                        to="/orders" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('orders'), disabled: isActive('orders') }" 
                                        aria-current="page"
                                    >
                                        Работа с заказами
                                    </router-link>
                                </li>
                            </ul>
                        </li>

                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                Материально-техническое обеспечение
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                                <li>
                                    <router-link 
                                        to="/providers" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('providers'), disabled: isActive('providers') }" 
                                        aria-current="page"
                                    >
                                        Поставщики топлива
                                    </router-link>
                                </li>
                                <li>
                                    <router-link 
                                        to="/purchase" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('purchase'), disabled: isActive('purchase') }" 
                                        aria-current="page"
                                    >
                                        Закупки топлива
                                    </router-link>
                                </li>

                                <li class="dropdown-item">
                                    <a class="nav-link dropdown-toggle" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                        Учет рабочей техники
                                    </a>
                                    <ul class="dropdown-menu dropdown-submenu" aria-labelledby="navbarDropdownMenuLink">
                                        <li>
                                            <router-link
                                                to="/helicopter-models"
                                                class="dropdown-item"
                                                v-bind:class="{ active: isActive('helicopter-models'), disabled: isActive('helicopter-models') }" 
                                                aria-current="page"
                                            >
                                                Модели вертолётов
                                            </router-link>
                                        </li>
                                        <li>
                                            <router-link 
                                                to="/helicopters" 
                                                class="dropdown-item" 
                                                v-bind:class="{ active: isActive('helicopters'), disabled: isActive('helicopters') }" 
                                                aria-current="page"
                                            >
                                                Вертолёты
                                            </router-link>
                                        </li>
                                    </ul>
                                </li>
                            </ul>
                        </li>

                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                Отчётность
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                                <li>
                                    <router-link 
                                        to="/statistical-reports" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('statistical-reports'), disabled: isActive('statistical-reports') }" 
                                        aria-current="page"
                                    >
                                        Статистические отчёты
                                    </router-link>
                                </li>
                                <li>
                                    <router-link 
                                        to="/reporting-documentation" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('reporting-documentation'), disabled: isActive('reporting-documentation') }" 
                                        aria-current="page"
                                    >
                                        Отчётная документация
                                    </router-link>
                                </li>
                            </ul>
                        </li>

                        <li class="nav-item">
                            <router-link 
                                    to="/document-templates" 
                                    class="nav-link" 
                                    v-bind:class="{ active: isActive('document-templates'), disabled: isActive('document-templates') }" 
                                    aria-current="page"
                            >
                                Шаблоны документов
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <b-button @click="logOut" id="logout-button" variant="outline-primary">Выйти</b-button> 
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        <nav v-if="$store.state.session.userType === 1" class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container px-4 pb-4">
                <div class="pe-3">
                    <router-link to="/clients">
                        <img src="../assets/logo-blue.png" class="mx-auto d-block" alt="Logo">
                    </router-link>
                </div>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNavDropdown">
                    <ul class="navbar-nav">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                Управление продажами
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                                <li>
                                    <router-link
                                        to="/clients" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('clients') }" 
                                        aria-current="page"
                                    >
                                        Работа с клиентами
                                    </router-link>
                                </li>
                                <li>
                                    <router-link 
                                        to="/orders" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('orders'), disabled: isActive('orders') }" 
                                        aria-current="page"
                                    >
                                        Работа с заказами
                                    </router-link>
                                </li>
                            </ul>
                        </li>

                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                Информирование
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                                <li>
                                    <router-link 
                                        to="/dispetchers" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('dispetchers'), disabled: isActive('dispetchers') }" 
                                        aria-current="page"
                                    >
                                        Информация о диспетчерах
                                    </router-link>
                                </li>
                                <li>
                                    <router-link 
                                        to="/pilots" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('pilots'), disabled: isActive('pilots') }" 
                                        aria-current="page"
                                    >
                                        Информация о пилотах
                                    </router-link>
                                </li>
                                <li>
                                    <router-link 
                                        to="/helicopters" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('helicopters'), disabled: isActive('helicopters') }" 
                                        aria-current="page"
                                    >
                                        Информация о вертолётах
                                    </router-link>
                                </li>
                            </ul>
                        </li>
                        <li class="nav-item">
                            <router-link 
                                    to="/my-orders" 
                                    class="nav-link" 
                                    v-bind:class="{ active: isActive('my-orders'), disabled: isActive('my-orders') }" 
                                    aria-current="page"
                                >
                                    Мои принятые заказы
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link 
                                    to="/document-templates" 
                                    class="nav-link" 
                                    v-bind:class="{ active: isActive('document-templates'), disabled: isActive('document-templates') }" 
                                    aria-current="page"
                            >
                                Шаблоны документов
                            </router-link>
                        </li>

                        <b-button @click="logOut" id="logout-button-disp" variant="outline-primary">Выйти</b-button> 
                    </ul>
                </div>
            </div>
        </nav>
        <nav v-if="$store.state.session.userType === 2" class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container px-4 pb-4">
                <div class="pe-3">
                    <router-link to="/clients">
                        <img src="../assets/logo-blue.png" class="mx-auto d-block" alt="Logo">
                    </router-link>
                </div>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNavDropdown">
                    <ul class="navbar-nav">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                Информирование
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                                <li>
                                    <router-link 
                                        to="/orders" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('orders'), disabled: isActive('orders') }" 
                                        aria-current="page"
                                    >
                                        Информация о заказах
                                    </router-link>
                                </li>
                                <li>
                                    <router-link 
                                        to="/clients" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('clients'), disabled: isActive('clients') }" 
                                        aria-current="page"
                                    >
                                        Информация о клиентах
                                    </router-link>
                                </li>
                                <li>
                                    <router-link 
                                        to="/dispetchers" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('dispetchers'), disabled: isActive('dispetchers') }" 
                                        aria-current="page"
                                    >
                                        Информация о диспетчерах
                                    </router-link>
                                </li>
                                <li>
                                    <router-link 
                                        to="/pilots" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('pilots'), disabled: isActive('pilots') }" 
                                        aria-current="page"
                                    >
                                        Информация о пилотах
                                    </router-link>
                                </li>
                                <li>
                                    <router-link 
                                        to="/helicopters" 
                                        class="dropdown-item" 
                                        v-bind:class="{ active: isActive('helicopters'), disabled: isActive('helicopters') }" 
                                        aria-current="page"
                                    >
                                        Информация о вертолётах
                                    </router-link>
                                </li>
                            </ul>
                        </li>

                        <li class="nav-item">
                            <router-link 
                                    to="/my-orders" 
                                    class="nav-link" 
                                    v-bind:class="{ active: isActive('my-orders'), disabled: isActive('my-orders') }" 
                                    aria-current="page"
                            >
                                Мои выполненные заказы
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link 
                                    to="/my-recertification" 
                                    class="nav-link" 
                                    v-bind:class="{ active: isActive('recertification'), disabled: isActive('recertification') }" 
                                    aria-current="page"
                            >
                                Дата моей переаттестации
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <router-link 
                                    to="/document-templates" 
                                    class="nav-link" 
                                    v-bind:class="{ active: isActive('document-templates'), disabled: isActive('document-templates') }" 
                                    aria-current="page"
                            >
                                Шаблоны документов
                            </router-link>
                        </li>

                        <li class="nav-item">
                            <b-button @click="logOut" id="logout-button-plt" variant="outline-primary">Выйти</b-button> 
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </div>
</template>

<script>
export default {
    name: 'navbar',
    data () {
        return {
            path: window.location.pathname
        }
    },
    methods: {
      isActive (page) {
        return this.currentPage === page;
      },
      logOut() {
        this.$store.commit('session/setUserType', 0);
        this.$store.commit('session/setAuth', false);
        this.$router.push('/');
      }
    },
    computed: {
      currentPage () {
        if (this.path.length === 1) return ''
        const endIndex = this.path.indexOf('/', 1)
        return (endIndex === -1)
          ? this.path.substring(1)
          : this.path.substring(1, endIndex)
      }
    }
}
</script>
    
<style>
.dropdown-menu li {
  position: relative;
}
.dropdown-menu .dropdown-submenu {
  display: none;
  position: absolute;
  left: 100%;
  top: -7px;
}
.dropdown-menu .dropdown-submenu-left {
  right: 100%;
  left: auto;
}
.dropdown-menu > li:hover > .dropdown-submenu {
  display: block;
}
.nav-item {
    margin-left: 10px;
}
#logout-button {
    margin-left: 80px;
}
#logout-button-disp {
    margin-left: 250px;
}
#logout-button-plt {
    margin-left: 240px;
}
.nav-item {
    white-space: nowrap
}
#navbar-line {
    margin-left: 225px;
}
</style>