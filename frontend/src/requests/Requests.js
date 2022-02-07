import axiosInstance from "./AxiosInstance";


export const searchToken = async (token) => 
    await axiosInstance.get("token/search?query=" + token)

export const createOrder = async (data) => 
    await axiosInstance.post("order/", data)

export const ordersGet = async () => 
    await axiosInstance.get('order/')

export const orderDelete = async (data) =>
    await axiosInstance.post(`order/destroy_order/`, data)

export const stopOrder = async (data) =>
    await axiosInstance.post(`order/stop_task/`, data)

export const startOrder = async (data) =>
    await axiosInstance.post(`order/start_task/`, data)

export const orderPricesGET = async (order_id) =>
    await axiosInstance.get(`order/${order_id}/order_prices/`)


export const orderTxsGET = async (order_id) =>
    await axiosInstance.get(`order/${order_id}/order_txs/`)