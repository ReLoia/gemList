declare global {
    interface Number {
        toShortString(): string;
    }
    interface String {
        capitalize(): string;
    }
    interface ImportMeta {
        env: {
            VITE_API_URL: string;
            BASE_URL: string;
        };
    }
}


String.prototype.capitalize = function () {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

Number.prototype.toShortString = function () {
    let num = +this;
    if (num < 1000) {
        return String(num);
    }
    const sizes = ['', 'k', 'M', 'B', 'T', 'Q', 'Qu', 'S', 'Se', 'O', 'N'];
    const i = Math.floor(Math.log(num) / Math.log(1000));
    return parseFloat((num / Math.pow(1000, i)).toFixed(1)) + sizes[i];
}