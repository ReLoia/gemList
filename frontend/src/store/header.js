import {defineStore} from 'pinia'

export const useHeaderStore = defineStore('header', {
    state: () => {
        /** @type {{
         * expanded: boolean,
         * backgroundImage: string,
         * title: string,
         * description: string,
         * type: string,
         * content: {
         *     component: () => JSX.Element,
         *     props: Record<string, unknown>
         * }
         }} */
        return {
            expanded: false,
            backgroundImage: '',
            type: '',
            content: {
                component: () => null,
                props: {}
            },
            loading: false,
            emits: {}
        }
    },

    actions: {
        setHeader(header) {
            this.expanded = header.expanded;
            this.backgroundImage = header.backgroundImage;
            this.type = header.type;
            this.content = header.content;
        },
        setExpanded(expanded) {
            this.expanded = expanded;
        },
        setContent(content) {
            this.content = content;
        },
        setLoading(loading) {
            this.loading = loading;
        },
        setBackgroundImage(backgroundImage) {
            this.backgroundImage = backgroundImage;
        },

        setEmits(emits) {
            this.emits = emits;
        },

        emit(emit, ...args) {
            if (this.emits[emit]) {
                this.emits[emit](...args);
            }
        },

        resetHeader() {
            this.expanded = false;
            this.backgroundImage = '';
            this.content = {
                component: () => null,
                props: {}
            };
            this.loading = false;
            this.emits = {};
        },
    }

})
