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
            loading: false
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
        }
    }

})
