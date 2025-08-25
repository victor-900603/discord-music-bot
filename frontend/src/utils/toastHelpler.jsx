let addToast = null;

export const setToastFunction = (func) => {
    addToast = func;
}

export const toast = (message, type='info', duration=3000) => {
    if (addToast) {
        addToast(message, type, duration);
    }
}