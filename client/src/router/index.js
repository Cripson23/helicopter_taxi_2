import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import EmployeesPage from '../views/EmployeesPage.vue'
import RecertificationPage from '../views/RecertificationPage.vue'
import MyOrders from '../views/MyOrdersPage.vue'
import ClientsPage from '../views/ClientsPage.vue'
import OrdersPage from '../views/OrdersPage.vue'
import ProvidersPage from '../views/ProvidersPage.vue'
import PurchasePage from '../views/PurchasePage.vue'
import HelicopterModelsPage from '../views/HelicopterModelsPage.vue'
import HelicoptersPage from '../views/HelicoptersPage.vue'
import StatisticalReportsPage from '../views/StatisticalReportsPage.vue'
import ReportingDocumentationPage from '../views/ReportingDocumentationPage.vue'
import DocumentTemplatesPage from '../views/DocumentTemplatesPage.vue'
import DispetchersPage from '../views/DispetchersPage.vue'
import PilotsPage from '../views/PilotsPage.vue'
import MyRecertificationPage from '../views/MyRecertificationPage.vue'


const routes = [
  {
    path: '/',
    name: 'LoginPage',
    component: LoginPage
  },
  {
    path: '/employees',
    name: 'EmployeesPage',
    component: EmployeesPage
  },
  {
    path: '/recertification',
    name: 'RecertificationPage',
    component: RecertificationPage
  },
  {
    path: '/my-orders',
    name: 'MyOrdersPage',
    component: MyOrders
  },
  {
    path: '/clients',
    name: 'ClientsPage',
    component: ClientsPage
  },
  {
    path: '/orders',
    name: 'OrdersPage',
    component: OrdersPage
  },
  {
    path: '/providers',
    name: 'ProvidersPage',
    component: ProvidersPage
  },
  {
    path: '/purchase',
    name: 'PurchasePage',
    component: PurchasePage
  },
  {
    path: '/helicopter-models',
    name: 'HelicopterModelsPage',
    component: HelicopterModelsPage
  },
  {
    path: '/helicopters',
    name: 'HelicoptersPage',
    component: HelicoptersPage
  },
  {
    path: '/statistical-reports',
    name: 'StatisticalReportsPage',
    component: StatisticalReportsPage
  },
  {
    path: '/reporting-documentation',
    name: 'ReportingDocumentationPage',
    component: ReportingDocumentationPage
  },
  {
    path: '/document-templates',
    name: 'DocumentTemplatesPage',
    component: DocumentTemplatesPage
  },
  {
    path: '/dispetchers',
    name: 'DispetchersPage',
    component: DispetchersPage
  },
  {
    path: '/pilots',
    name: 'PilotsPage',
    component: PilotsPage
  },
  {
    path: '/my-recertification',
    name: 'MyRecertification',
    component: MyRecertificationPage
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
