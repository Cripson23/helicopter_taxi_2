
export default {
    data() {
        return {
            message: '',
            showMessage: false,
        }
    },
    methods: {
        showMessageHandle(message) {
            this.message = message;
            this.showMessage = true;
            setTimeout(() => {
              this.showMessage = false;
              this.message = '';
            }, 3000);
        },
    }
}