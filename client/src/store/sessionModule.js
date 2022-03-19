export const sessionModule = {
    state: () => ({
        userType: 0,
        auth: false,
    }),
    getters: {
        getMainPath(state) {
            switch(state.userType) {
                case 1: {
                  return 'clients';
                }
                case 2: {
                  return 'my-orders';
                }
                case 3: {
                  return 'employees'
                }
              }
        }
    },
    mutations: {
        setUserType(state, userType) {
            state.userType = userType;
        },
        setAuth(state, auth) {
            state.auth = auth;
        }
    },
    actions: {
    },
    namespaced: true
}