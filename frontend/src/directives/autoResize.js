import { onMounted, onUnmounted } from "vue";

export default {
    mounted(el) {        
        const resizeText = () => {
            let parentWidth = el.parentElement.clientWidth - parseInt(window.getComputedStyle(el.parentElement).paddingInline) * 2;
            let fontSize = 34;

            el.style.fontSize = fontSize + "px";
            while (el.scrollWidth > parentWidth && fontSize > 10) {
                fontSize--;
                el.style.fontSize = fontSize + "px";
            }
        };

        const observer = new MutationObserver(resizeText);
        observer.observe(el, { characterData: true, childList: true, subtree: true });
        
        resizeText()
        
        onMounted(resizeText);
        onUnmounted(() => observer.disconnect());

        el.__observer__ = observer;
    },
    unmounted(el) {
        if (el.__observer__) {
            el.__observer__.disconnect();
        }el.parentElement.clientWidth
    }
};
