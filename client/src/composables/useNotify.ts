import { ref } from "vue"

const useNotify = (category: 'success' | 'error', msg: string) => {
    const notification = ref<{
        isNotified: boolean,
        category: 'success' | 'error' | undefined | null
        msg: string
    }>({
        isNotified: false,
        category: undefined,
        msg: ''
    })

    notification.value.isNotified = true
    notification.value.category = category
    notification.value.msg = msg

    setTimeout(() => {
        notification.value.isNotified = false
        notification.value.category = null
        notification.value.msg = ''
    }, 3000)

    return notification
}

export default useNotify