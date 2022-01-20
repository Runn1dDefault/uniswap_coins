import {axiosInstance} from "./AxiosInstance";


export const searchToken = async (token) => 
    await axiosInstance.get("token/search?query=" + token)

export const createOrder = async (data) => 
    await axiosInstance.post("order/", data)

export const ordersGet = async () => 
    await axiosInstance.get('order/')

export const orderDelete = async (order_id) =>
    await axiosInstance.delete(`order/${order_id}`)

export const stopOrder = async (order_id) =>
    await axiosInstance.get(`order/${order_id}/stop_task/`)

export const startOrder = async (order_id, data) =>
    await axiosInstance.post(`order/${order_id}/start_task/`, data)

export const orderPricesGET = async (order_id) =>
    await axiosInstance.get(`order/${order_id}/order_prices/`)
