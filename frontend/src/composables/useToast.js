import { inject } from 'vue';

export function useToast() {
    const toast = inject('toast');

    return {
        success: (message) => toast.value?.addToast(message, 'success'),
        error: (message) => toast.value?.addToast(message, 'error'),
        warning: (message) => toast.value?.addToast(message, 'warning'),
        info: (message) => toast.value?.addToast(message, 'info'),
    };
}

export function useConfirm() {
    const confirm = inject('confirm');

    return {
        show: (options) => confirm.value?.show(options),
    };
}
