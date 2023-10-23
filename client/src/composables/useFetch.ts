import { ref, Ref, toRef } from 'vue'
import { AxiosError } from 'axios'

import { sendReqCookie, sendReqWoCookie } from "@/utils/axiosInstances"

const useFetchObject = async<T> (url: string, authenthicated: boolean) => {
    const obj = ref<T | undefined>()
    const error = ref<string>()

    if (authenthicated) {
        try {
            const { data } = await sendReqCookie.get(url)
                if (data?.success) {
                    obj.value = data.data as T
                }
        } catch (err) {
            error.value = (err as AxiosError).message
        }
    } else {
        try {
            const { data } = await sendReqWoCookie.get(url)
                if (data?.success) {
                    obj.value = data.data as T
                }
        } catch (err) {
            error.value = (err as AxiosError).message
        }
    }

    return { obj, error }
}

const useFetchList = async<T> (url: string, authenthicated: boolean) => {
    const list: Ref<T[]> = toRef(ref([]))
    const error = ref<string>()

    if (authenthicated) {
        try {
            const { data } = await sendReqCookie.get(url)
                if (data?.success) {
                    list.value = data.data as T[]
                }
        } catch (err) {
            error.value = (err as AxiosError).message
        }
    } else {
        try {
            const { data } = await sendReqWoCookie.get(url)
                if (data?.success) {
                    list.value = data.data as T[]
                }
        } catch (err) {
            error.value = (err as AxiosError).message
        }
    }

    return { list, error }
}

export { useFetchObject, useFetchList }